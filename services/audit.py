from models.db import db, AuditEvent
from datetime import datetime
from typing import Dict, Any
import json

class AuditService:
    """Audit trail service"""
    
    def log_event(self, user_id: int, action: str, artifact_id: int = None, metadata: Dict[str, Any] = None):
        """Log an audit event"""
        event = AuditEvent(
            user_id=user_id,
            action=action,
            artifact_id=artifact_id,
            timestamp=datetime.utcnow(),
            metadata_json=json.dumps(metadata) if metadata else None
        )
        db.session.add(event)
        db.session.commit()
        return event
    
    def get_user_events(self, user_id: int, limit: int = 50):
        """Get audit events for a user"""
        return AuditEvent.query.filter_by(user_id=user_id).order_by(AuditEvent.timestamp.desc()).limit(limit).all()
    
    def get_artifact_events(self, artifact_id: int):
        """Get audit events for an artifact"""
        return AuditEvent.query.filter_by(artifact_id=artifact_id).order_by(AuditEvent.timestamp.asc()).all()


