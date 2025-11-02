from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    created_at: datetime

# Contract Schemas
class ContractGenerateRequest(BaseModel):
    contract_type: str  # NDA, Employment, Service, etc.
    parties: List[str] = []
    terms: Dict[str, Any] = {}
    language: str = "en"
    jurisdiction: str = "IN"
    profile: str = "india_default"

class ContractResponse(BaseModel):
    contract_id: int
    html: Optional[str] = None
    pdf_url: Optional[str] = None
    docx_url: Optional[str] = None
    summary: Dict[str, Any] = {}

# Verification Schemas
class VerificationRequest(BaseModel):
    jurisdiction: str = "IN"
    language: str = "en"

class Finding(BaseModel):
    clause: str
    issue: str
    severity: str  # critical, high, medium, low
    suggestion: str

class VerificationResponse(BaseModel):
    report_id: int
    risk_score: float
    findings: List[Finding] = []
    suggestions: List[str] = []
    summary_pdf_url: Optional[str] = None

# Explain Schemas
class ExplainRequest(BaseModel):
    text: str
    language: str = "en"
    jurisdiction: str = "IN"

class ExplainResponse(BaseModel):
    explanation: str
    refs: List[str] = []

# Compliance Schemas
class ComplianceCheck(BaseModel):
    category: str  # GST, TDS, Companies Act, etc.
    status: str  # pass, warn, fail
    message: str
    citation: Optional[str] = None

class ComplianceResponse(BaseModel):
    checks: List[ComplianceCheck] = []
    overall_status: str

# Dashboard Schemas
class DashboardMetrics(BaseModel):
    counts: Dict[str, int] = {}
    risk_histogram: List[Dict[str, Any]] = []
    top_missing_clauses: List[str] = []
    compliance_scores: List[Dict[str, Any]] = []

# Template Schemas
class TemplateResponse(BaseModel):
    id: int
    name: str
    jurisdiction: str
    category: str
    risk_level: str


