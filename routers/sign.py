from flask import Blueprint, request, jsonify
from models.db import db, Contract, AuditEvent
from services.signer import SignatureService

bp = Blueprint('sign', __name__)
signer = SignatureService()

@bp.route('/envelope', methods=['POST'])
def create_envelope():
    """Create e-signature envelope (DocuSign sandbox or mock)"""
    try:
        data = request.json
        contract_id = data.get('contract_id')
        signer_info = data.get('signer', {})
        
        if not contract_id:
            return jsonify({'error': 'contract_id required'}), 400
        
        contract = Contract.query.get_or_404(contract_id)
        user_id = request.headers.get('X-User-Id', 1)
        
        # Create envelope (mock for now, can integrate DocuSign later)
        envelope_result = signer.create_envelope(
            contract_id=contract_id,
            pdf_path=contract.pdf_path,
            signer=signer_info
        )
        
        # Update contract status
        contract.status = 'pending_signature'
        db.session.commit()
        
        # Create audit event
        audit = AuditEvent(
            user_id=user_id,
            action='create_envelope',
            metadata_json=f'{{"contract_id": {contract_id}, "envelope_id": "{envelope_result.get("envelope_id")}"}}'
        )
        db.session.add(audit)
        db.session.commit()
        
        return jsonify({
            'envelope_id': envelope_result.get('envelope_id'),
            'status_url': envelope_result.get('status_url'),
            'signer_link': envelope_result.get('signer_link')
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@bp.route('/status/<envelope_id>', methods=['GET'])
def get_envelope_status(envelope_id):
    """Get envelope signature status"""
    try:
        status = signer.get_envelope_status(envelope_id)
        return jsonify(status), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400


