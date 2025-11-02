import hashlib
import os
from datetime import datetime
from typing import Dict, Any
import json

class SignatureService:
    """E-signature service (mock for MVP, can integrate DocuSign later)"""
    
    def __init__(self):
        self.envelopes = {}  # In-memory storage for MVP
    
    def create_envelope(self, contract_id: int, pdf_path: str, signer: Dict[str, Any]) -> Dict[str, Any]:
        """Create e-signature envelope"""
        envelope_id = f"env_{contract_id}_{int(datetime.now().timestamp())}"
        
        # Calculate file hash
        file_hash = self._calculate_hash(pdf_path)
        
        # Store envelope info
        self.envelopes[envelope_id] = {
            'contract_id': contract_id,
            'pdf_path': pdf_path,
            'signer': signer,
            'status': 'pending',
            'file_hash': file_hash,
            'created_at': datetime.now().isoformat(),
            'signed_at': None
        }
        
        # Generate signer link (mock)
        signer_link = f"/sign/{envelope_id}?token=mock_token"
        
        return {
            'envelope_id': envelope_id,
            'status_url': f"/api/sign/status/{envelope_id}",
            'signer_link': signer_link,
            'file_hash': file_hash
        }
    
    def get_envelope_status(self, envelope_id: str) -> Dict[str, Any]:
        """Get envelope status"""
        if envelope_id not in self.envelopes:
            raise ValueError("Envelope not found")
        
        envelope = self.envelopes[envelope_id]
        return {
            'envelope_id': envelope_id,
            'status': envelope['status'],
            'created_at': envelope['created_at'],
            'signed_at': envelope.get('signed_at'),
            'signer': envelope['signer']
        }
    
    def sign_envelope(self, envelope_id: str, signer_name: str, ip_address: str = None) -> Dict[str, Any]:
        """Sign an envelope (mock)"""
        if envelope_id not in self.envelopes:
            raise ValueError("Envelope not found")
        
        envelope = self.envelopes[envelope_id]
        envelope['status'] = 'signed'
        envelope['signed_at'] = datetime.now().isoformat()
        envelope['signer_ip'] = ip_address
        
        # Create audit entry
        audit_data = {
            'envelope_id': envelope_id,
            'signer_name': signer_name,
            'signer_ip': ip_address,
            'timestamp': envelope['signed_at'],
            'file_hash': envelope['file_hash']
        }
        
        return audit_data
    
    def _calculate_hash(self, file_path: str) -> str:
        """Calculate SHA256 hash of file"""
        sha256_hash = hashlib.sha256()
        try:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return f"hash_error_{hash(str(e))}"


