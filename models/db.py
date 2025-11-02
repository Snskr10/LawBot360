from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and access control"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')  # admin, lawyer, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    contracts = db.relationship('Contract', backref='user', lazy=True)
    reports = db.relationship('VerificationReport', backref='user', lazy=True)
    audit_events = db.relationship('AuditEvent', backref='user', lazy=True)

class Artifact(db.Model):
    """Stores references to generated/uploaded files"""
    __tablename__ = 'artifacts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    artifact_type = db.Column(db.String(50))  # contract, report, upload
    path = db.Column(db.String(500))
    sha256 = db.Column(db.String(64))  # File hash
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Contract(db.Model):
    """Contract model - stores generated contracts"""
    __tablename__ = 'contracts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contract_type = db.Column(db.String(100))  # NDA, Employment, Service, etc.
    jurisdiction = db.Column(db.String(10), default='IN')
    language = db.Column(db.String(10), default='en')
    status = db.Column(db.String(50), default='draft')  # draft, signed, verified
    html_path = db.Column(db.String(500))
    pdf_path = db.Column(db.String(500))
    docx_path = db.Column(db.String(500))
    risk_score = db.Column(db.Float)
    metadata_json = db.Column(db.Text)  # Stores contract inputs as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class VerificationReport(db.Model):
    """Document verification reports"""
    __tablename__ = 'verification_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    contract_id = db.Column(db.Integer, db.ForeignKey('contracts.id'), nullable=True)
    uploaded_file_path = db.Column(db.String(500))
    risk_score = db.Column(db.Float)
    findings_json = db.Column(db.Text)  # JSON array of findings
    suggestions_json = db.Column(db.Text)  # JSON array of suggestions
    summary_pdf_path = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ClauseTemplate(db.Model):
    """Reusable clause templates"""
    __tablename__ = 'clause_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    jurisdiction = db.Column(db.String(10), default='IN')
    category = db.Column(db.String(100))  # ip, confidentiality, payment, etc.
    text = db.Column(db.Text, nullable=False)
    required_vars = db.Column(db.Text)  # JSON array of variable names
    risk_level = db.Column(db.String(20))  # low, medium, high
    is_mandatory = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class LawSection(db.Model):
    """Legal sections from various acts"""
    __tablename__ = 'law_sections'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500))
    section_code = db.Column(db.String(50))
    jurisdiction = db.Column(db.String(10), default='IN')
    act_name = db.Column(db.String(200))  # Contract Act, IT Act, etc.
    text = db.Column(db.Text)
    citations_json = db.Column(db.Text)  # JSON array of related cases/references
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AuditEvent(db.Model):
    """Audit trail for all actions"""
    __tablename__ = 'audit_events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(100))  # create_contract, verify_document, etc.
    artifact_id = db.Column(db.Integer, db.ForeignKey('artifacts.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    metadata_json = db.Column(db.Text)  # Additional context as JSON


