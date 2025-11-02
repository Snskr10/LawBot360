import json

from flask import Blueprint, request, jsonify
from models.db import db, Contract, User, Artifact, AuditEvent
from models.schemas import ContractGenerateRequest, ContractResponse
from datetime import datetime
import hashlib
import os

bp = Blueprint('contracts', __name__)

@bp.route('/generate', methods=['POST'])
def generate_contract():
    """Generate a contract from natural language or structured input"""
    try:
        from services.generator import ContractGenerator
        generator = ContractGenerator()
        
        data = request.json
        req = ContractGenerateRequest(**data)
        
        # For MVP, using user_id = 1 (default user)
        # In production, get from JWT/session
        user_id = request.headers.get('X-User-Id', 1)
        
        # Generate contract
        result = generator.generate(
            contract_type=req.contract_type,
            parties=req.parties,
            terms=req.terms,
            jurisdiction=req.jurisdiction,
            language=req.language
        )
        
        # Save to database
        contract = Contract(
            user_id=user_id,
            contract_type=req.contract_type,
            jurisdiction=req.jurisdiction,
            language=req.language,
            status='draft',
            html_path=result.get('html_path'),
            pdf_path=result.get('pdf_path'),
            docx_path=result.get('docx_path'),
            metadata_json=json.dumps({
                'parties': req.parties,
                'terms': req.terms,
                'generated_at': datetime.utcnow().isoformat()
            })
        )
        db.session.add(contract)
        db.session.commit()
        
        # Create audit event
        audit = AuditEvent(
            user_id=user_id,
            action='create_contract',
            metadata_json=json.dumps({
                'contract_type': req.contract_type,
                'contract_id': contract.id
            })
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'contract_id': contract.id,
            'html': result.get('html'),
            'pdf_url': f'/api/contracts/{contract.id}/pdf',
            'docx_url': f'/api/contracts/{contract.id}/docx',
            'summary': result.get('summary', {}),
            'markdown': result.get('markdown')
        }), 200
        
    except ImportError as e:
        return jsonify({'error': f'Service not available: {str(e)}'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/<int:contract_id>', methods=['GET'])
def get_contract(contract_id):
    """Get contract details"""
    contract = Contract.query.get_or_404(contract_id)
    return jsonify({
        'id': contract.id,
        'contract_type': contract.contract_type,
        'jurisdiction': contract.jurisdiction,
        'language': contract.language,
        'status': contract.status,
        'risk_score': contract.risk_score,
        'created_at': contract.created_at.isoformat(),
        'pdf_url': f'/api/contracts/{contract.id}/pdf' if contract.pdf_path else None,
        'docx_url': f'/api/contracts/{contract.id}/docx' if contract.docx_path else None
    }), 200

@bp.route('/<int:contract_id>/pdf', methods=['GET'])
def download_pdf(contract_id):
    """Download contract as PDF"""
    from flask import send_file
    contract = Contract.query.get_or_404(contract_id)
    if contract.pdf_path and os.path.exists(contract.pdf_path):
        return send_file(contract.pdf_path, as_attachment=True, download_name=f'contract_{contract_id}.pdf')
    return jsonify({'error': 'PDF not found'}), 404

@bp.route('/<int:contract_id>/docx', methods=['GET'])
def download_docx(contract_id):
    """Download contract as DOCX"""
    from flask import send_file
    contract = Contract.query.get_or_404(contract_id)
    if contract.docx_path and os.path.exists(contract.docx_path):
        return send_file(contract.docx_path, as_attachment=True, download_name=f'contract_{contract_id}.docx')
    return jsonify({'error': 'DOCX not found'}), 404

@bp.route('/list', methods=['GET'])
def list_contracts():
    """List user's contracts"""
    user_id = request.headers.get('X-User-Id', 1)
    contracts = Contract.query.filter_by(user_id=user_id).order_by(Contract.created_at.desc()).limit(50).all()
    
    return jsonify([{
        'id': c.id,
        'contract_type': c.contract_type,
        'jurisdiction': c.jurisdiction,
        'status': c.status,
        'risk_score': c.risk_score,
        'created_at': c.created_at.isoformat()
    } for c in contracts]), 200


