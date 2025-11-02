from flask import Blueprint, request, jsonify
from models.db import db, Contract, VerificationReport, User, ClauseTemplate
from models.schemas import DashboardMetrics
from sqlalchemy import func
from datetime import datetime, timedelta
import json

bp = Blueprint('dashboard', __name__)

@bp.route('/metrics', methods=['GET'])
def get_metrics():
    """Get dashboard metrics"""
    try:
        user_id = request.headers.get('X-User-Id', 1)
        
        # Counts
        contract_count = Contract.query.filter_by(user_id=user_id).count()
        verification_count = VerificationReport.query.filter_by(user_id=user_id).count()
        
        # Risk histogram (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        recent_reports = VerificationReport.query.filter(
            VerificationReport.user_id == user_id,
            VerificationReport.created_at >= thirty_days_ago
        ).all()
        
        risk_histogram = []
        risk_ranges = [(0, 30), (31, 50), (51, 70), (71, 85), (86, 100)]
        for low, high in risk_ranges:
            count = sum(1 for r in recent_reports if low <= (r.risk_score or 0) <= high)
            risk_histogram.append({'range': f'{low}-{high}', 'count': count})
        
        # Top missing clauses (from findings)
        all_findings = []
        for report in recent_reports:
            if report.findings_json:
                try:
                    findings = json.loads(report.findings_json)
                    all_findings.extend([f.get('clause', '') for f in findings])
                except:
                    pass
        
        # Count clause occurrences
        clause_counts = {}
        for clause in all_findings:
            clause_counts[clause] = clause_counts.get(clause, 0) + 1
        
        top_missing = sorted(clause_counts.items(), key=lambda x: x[1], reverse=True)[:5]
        top_missing_clauses = [clause for clause, count in top_missing]
        
        # Compliance scores (simplified - average risk score by month)
        compliance_scores = []
        current_date = datetime.utcnow()
        for i in range(6):  # Last 6 months
            month_start = current_date.replace(day=1) - timedelta(days=30*i)
            month_reports = VerificationReport.query.filter(
                VerificationReport.user_id == user_id,
                VerificationReport.created_at >= month_start
            ).all()
            
            if month_reports:
                avg_score = sum(r.risk_score or 0 for r in month_reports) / len(month_reports)
                compliance_scores.append({
                    'month': month_start.strftime('%Y-%m'),
                    'avg_risk_score': round(avg_score, 2)
                })
        
        return jsonify({
            'counts': {
                'contracts': contract_count,
                'verifications': verification_count
            },
            'risk_histogram': risk_histogram,
            'top_missing_clauses': top_missing_clauses,
            'compliance_scores': compliance_scores
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/templates/list', methods=['GET'])
def list_templates():
    """List available clause templates"""
    jurisdiction = request.args.get('jurisdiction', 'IN')
    templates = ClauseTemplate.query.filter_by(jurisdiction=jurisdiction).all()
    
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'jurisdiction': t.jurisdiction,
        'category': t.category,
        'risk_level': t.risk_level,
        'is_mandatory': t.is_mandatory
    } for t in templates]), 200


