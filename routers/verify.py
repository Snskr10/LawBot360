import json
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models.db import db, VerificationReport, AuditEvent
from models.schemas import VerificationRequest, VerificationResponse, Finding
from config import Config

bp = Blueprint('verify', __name__)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/document', methods=['POST'])
def verify_document():
    """Verify an uploaded contract document"""
    try:
        from services.verifier import DocumentVerifier
        verifier = DocumentVerifier()
        
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Allowed: PDF, DOCX'}), 400
        
        # Get parameters
        jurisdiction = request.form.get('jurisdiction', 'IN')
        language = request.form.get('language', 'en')
        user_id = request.headers.get('X-User-Id', 1)
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        upload_dir = Path(current_app.config.get('UPLOAD_FOLDER', Config.UPLOAD_FOLDER))
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / f"{uuid4().hex}_{filename}"
        file.save(str(file_path))
        
        # Verify document
        result = verifier.verify(
            file_path=str(file_path),
            jurisdiction=jurisdiction,
            language=language
        )
        
        # Save report
        report = VerificationReport(
            user_id=user_id,
            uploaded_file_path=str(file_path),
            risk_score=result.get('risk_score', 0),
            findings_json=json.dumps(result.get('findings', [])),
            suggestions_json=json.dumps(result.get('suggestions', [])),
            summary_pdf_path=result.get('summary_pdf_path')
        )
        db.session.add(report)
        db.session.commit()
        
        # Create audit event
        audit = AuditEvent(
            user_id=user_id,
            action='verify_document',
            metadata_json=json.dumps({
                'report_id': report.id,
                'risk_score': result.get('risk_score', 0)
            })
        )
        db.session.add(audit)
        db.session.commit()
        
        # Format findings
        findings = [Finding(**f) for f in result.get('findings', [])]
        
        return jsonify({
            'report_id': report.id,
            'risk_score': result.get('risk_score', 0),
            'findings': [f.dict() for f in findings],
            'suggestions': result.get('suggestions', []),
            'summary_pdf_url': f'/api/verify/{report.id}/summary' if result.get('summary_pdf_path') else None
        }), 200
        
    except ImportError as e:
        return jsonify({'error': f'Service not available: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:report_id>', methods=['GET'])
def get_report(report_id):
    """Get verification report details"""
    report = VerificationReport.query.get_or_404(report_id)
    return jsonify({
        'id': report.id,
        'risk_score': report.risk_score,
        'findings': json.loads(report.findings_json) if report.findings_json else [],
        'suggestions': json.loads(report.suggestions_json) if report.suggestions_json else [],
        'created_at': report.created_at.isoformat(),
        'summary_pdf_url': f'/api/verify/{report.id}/summary' if report.summary_pdf_path else None
    }), 200

@bp.route('/<int:report_id>/summary', methods=['GET'])
def download_summary(report_id):
    """Download verification summary PDF"""
    from flask import send_file
    report = VerificationReport.query.get_or_404(report_id)
    if report.summary_pdf_path and Path(report.summary_pdf_path).exists():
        return send_file(report.summary_pdf_path, as_attachment=True, download_name=f'verification_report_{report_id}.pdf')
    return jsonify({'error': 'Summary not found'}), 404


