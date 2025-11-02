import re
from pathlib import Path
from typing import Any, Dict, List
from uuid import uuid4

import docx
import fitz  # PyMuPDF
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

from config import Config
from services.compliance import ComplianceChecker
from services.ocr import OCRService

class DocumentVerifier:
    """Verifies contracts for missing clauses and risks"""
    
    def __init__(self):
        self.ocr_service = OCRService()
        self.compliance_checker = ComplianceChecker()
        self.reports_path = Path(Config.EXPORT_FOLDER) / "reports"
        self.reports_path.mkdir(parents=True, exist_ok=True)
        
        # Mandatory clauses by contract type
        self.mandatory_clauses = {
            'generic': ['parties', 'consideration', 'governing_law', 'signatures'],
            'employment': ['parties', 'position', 'salary', 'notice_period', 'confidentiality', 'ip_ownership', 'termination'],
            'nda': ['parties', 'confidential_info_definition', 'obligations', 'duration', 'exceptions', 'governing_law'],
            'service': ['parties', 'scope', 'payment', 'deliverables', 'termination', 'intellectual_property'],
            'lease': ['parties', 'premises', 'rent', 'duration', 'deposit', 'maintenance', 'termination']
        }
        
        # Risk indicators
        self.hedge_words = ['best effort', 'reasonable', 'as soon as practicable', 'approximately', 'about', 'may', 'could']
        self.vague_phrases = ['subject to', 'unless otherwise', 'to the extent', 'as applicable']
    
    def verify(self, file_path: str, jurisdiction: str = 'IN', language: str = 'en') -> Dict[str, Any]:
        """Verify a contract document"""
        # Extract text
        text = self._extract_text(file_path)
        
        # Detect contract type
        contract_type = self._detect_contract_type(text)
        
        # Extract metadata
        metadata = self._extract_metadata(text)
        
        # Check mandatory clauses
        missing_clauses = self._check_mandatory_clauses(text, contract_type)
        
        # Check for risk indicators
        risk_factors = self._analyze_risks(text)
        
        # Compliance check
        compliance_result = self.compliance_checker.check(text, jurisdiction)
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(missing_clauses, risk_factors, compliance_result)
        
        # Generate findings
        findings = self._generate_findings(missing_clauses, risk_factors, compliance_result)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(findings, contract_type, jurisdiction)

        summary_pdf_path = self._generate_summary_pdf(
            contract_type=contract_type,
            metadata=metadata,
            risk_score=risk_score,
            findings=findings,
            suggestions=suggestions
        )

        return {
            'contract_type': contract_type,
            'metadata': metadata,
            'risk_score': risk_score,
            'findings': findings,
            'suggestions': suggestions,
            'summary_pdf_path': summary_pdf_path
        }
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF or DOCX"""
        if file_path.endswith('.pdf'):
            return self._extract_from_pdf(file_path)
        elif file_path.endswith(('.docx', '.doc')):
            return self._extract_from_docx(file_path)
        else:
            return ""
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF"""
        try:
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except:
            # Try OCR if direct extraction fails
            return self.ocr_service.extract_text(file_path)
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = docx.Document(file_path)
            return '\n'.join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"Error extracting DOCX: {e}"
    
    def _detect_contract_type(self, text: str) -> str:
        """Detect contract type from text"""
        text_lower = text.lower()
        if 'non-disclosure' in text_lower or 'nda' in text_lower:
            return 'nda'
        elif 'employment' in text_lower or 'employee' in text_lower:
            return 'employment'
        elif 'lease' in text_lower or 'rent' in text_lower:
            return 'lease'
        elif 'service' in text_lower and 'agreement' in text_lower:
            return 'service'
        else:
            return 'generic'
    
    def _extract_metadata(self, text: str) -> Dict[str, Any]:
        """Extract contract metadata"""
        # Extract dates
        date_pattern = r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'
        dates = re.findall(date_pattern, text)
        
        # Extract amounts (currency patterns)
        amount_pattern = r'[₹$€£]\s*\d+(?:,\d{3})*(?:\.\d{2})?'
        amounts = re.findall(amount_pattern, text)
        
        # Extract parties (simplified - looks for "Party A", "Company Name", etc.)
        party_pattern = r'(?:Party\s+[AB]|Company|Corporation|LLC|Pvt\.?\s+Ltd\.?)'
        parties = re.findall(party_pattern, text, re.IGNORECASE)
        
        return {
            'dates': dates[:5],
            'amounts': amounts[:5],
            'parties': list(set(parties))[:5]
        }
    
    def _check_mandatory_clauses(self, text: str, contract_type: str) -> List[str]:
        """Check for missing mandatory clauses"""
        mandatory = self.mandatory_clauses.get(contract_type, self.mandatory_clauses['generic'])
        missing = []
        
        text_lower = text.lower()
        clause_keywords = {
            'parties': ['party', 'between', 'hereinafter'],
            'consideration': ['consideration', 'payment', 'compensation'],
            'governing_law': ['governing law', 'jurisdiction', 'laws of'],
            'signatures': ['signature', 'signed', 'witness'],
            'confidentiality': ['confidential', 'non-disclosure', 'nda'],
            'ip_ownership': ['intellectual property', 'ip', 'copyright', 'patent'],
            'termination': ['termination', 'terminate', 'end of agreement'],
            'notice_period': ['notice', 'notice period'],
            'scope': ['scope', 'work', 'services', 'deliverables']
        }
        
        for clause in mandatory:
            keywords = clause_keywords.get(clause, [])
            found = any(keyword in text_lower for keyword in keywords)
            if not found:
                missing.append(clause)
        
        return missing
    
    def _analyze_risks(self, text: str) -> Dict[str, Any]:
        """Analyze text for risk indicators"""
        text_lower = text.lower()
        risks = {
            'hedge_words_found': [],
            'vague_phrases_found': [],
            'unclear_payment': 'payment' in text_lower and ('tbd' in text_lower or 'to be determined' in text_lower),
            'no_liability_cap': 'liability' in text_lower and 'limited' not in text_lower and 'cap' not in text_lower,
            'no_indemnity': 'indemnity' not in text_lower,
            'unclear_termination': 'termination' in text_lower and ('30 days' not in text_lower and 'notice' not in text_lower)
        }
        
        # Find hedge words
        for word in self.hedge_words:
            if word in text_lower:
                risks['hedge_words_found'].append(word)
        
        # Find vague phrases
        for phrase in self.vague_phrases:
            if phrase in text_lower:
                risks['vague_phrases_found'].append(phrase)
        
        return risks
    
    def _calculate_risk_score(self, missing_clauses: List[str], risk_factors: Dict, compliance_result: Dict) -> float:
        """Calculate overall risk score (0-100, higher = more risk)"""
        score = 0.0
        
        # Missing clauses contribute 40 points max
        score += min(len(missing_clauses) * 10, 40)
        
        # Risk factors contribute 30 points max
        if risk_factors.get('unclear_payment'):
            score += 10
        if risk_factors.get('no_liability_cap'):
            score += 8
        if risk_factors.get('no_indemnity'):
            score += 7
        if risk_factors.get('unclear_termination'):
            score += 5
        
        # Hedge words and vague phrases
        score += min(len(risk_factors.get('hedge_words_found', [])) * 2, 10)
        score += min(len(risk_factors.get('vague_phrases_found', [])) * 1, 10)
        
        # Compliance issues contribute 30 points max
        compliance_fails = sum(1 for check in compliance_result.get('checks', []) if check.get('status') == 'fail')
        score += min(compliance_fails * 5, 30)
        
        return min(score, 100.0)
    
    def _generate_findings(self, missing_clauses: List[str], risk_factors: Dict, compliance_result: Dict) -> List[Dict]:
        """Generate structured findings"""
        findings = []
        
        # Missing clauses
        for clause in missing_clauses:
            findings.append({
                'clause': clause.replace('_', ' ').title(),
                'issue': f'Missing mandatory clause: {clause}',
                'severity': 'critical' if clause in ['parties', 'consideration', 'signatures'] else 'high',
                'suggestion': f'Add a clear {clause} clause to the contract'
            })
        
        # Risk factors
        if risk_factors.get('unclear_payment'):
            findings.append({
                'clause': 'Payment Terms',
                'issue': 'Payment terms are unclear or TBD',
                'severity': 'high',
                'suggestion': 'Specify exact payment amounts, timelines, and methods'
            })
        
        if risk_factors.get('no_liability_cap'):
            findings.append({
                'clause': 'Liability',
                'issue': 'No liability cap or limitation clause',
                'severity': 'medium',
                'suggestion': 'Add a limitation of liability clause with reasonable caps'
            })
        
        # Compliance issues
        for check in compliance_result.get('checks', []):
            if check.get('status') in ['fail', 'warn']:
                findings.append({
                    'clause': check.get('category', 'Compliance'),
                    'issue': check.get('message', 'Compliance issue detected'),
                    'severity': 'high' if check.get('status') == 'fail' else 'medium',
                    'suggestion': check.get('message', 'Review compliance requirements')
                })
        
        return findings
    
    def _generate_suggestions(self, findings: List[Dict], contract_type: str, jurisdiction: str) -> List[str]:
        """Generate actionable suggestions"""
        suggestions = []
        
        for finding in findings:
            if finding['severity'] in ['critical', 'high']:
                suggestions.append(f"Add {finding['clause']}: {finding['suggestion']}")
        
        # Add general suggestions
        if len(findings) > 5:
            suggestions.append("Consider having a lawyer review this contract before signing")
        
        return suggestions[:10]  # Limit to top 10

    def _generate_summary_pdf(
        self,
        contract_type: str,
        metadata: Dict[str, Any],
        risk_score: float,
        findings: List[Dict[str, Any]],
        suggestions: List[str]
    ) -> str:
        """Create a concise verification summary PDF and return its path"""

        report_id = uuid4().hex
        summary_path = self.reports_path / f"verification_{report_id}.pdf"

        doc = SimpleDocTemplate(str(summary_path), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        heading = Paragraph("LawBot 360 - Verification Summary", styles['Heading2'])
        story.append(heading)
        story.append(Spacer(1, 12))

        meta_lines = [
            f"Contract Type: {contract_type.title()}",
            f"Detected Parties: {', '.join(metadata.get('parties', [])) or 'Not detected'}",
            f"Detected Dates: {', '.join(metadata.get('dates', [])) or 'Not detected'}",
            f"Detected Amounts: {', '.join(metadata.get('amounts', [])) or 'Not detected'}",
            f"Risk Score: {risk_score:.1f} / 100"
        ]

        for line in meta_lines:
            story.append(Paragraph(line, styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Key Findings:", styles['Heading3']))
        if findings:
            for finding in findings[:10]:
                body = f"• {finding.get('clause', 'Clause')}: {finding.get('issue')} ({finding.get('severity').upper()})"
                story.append(Paragraph(body, styles['Normal']))
        else:
            story.append(Paragraph("No major issues detected.", styles['Normal']))
        story.append(Spacer(1, 12))

        story.append(Paragraph("Recommendations:", styles['Heading3']))
        if suggestions:
            for suggestion in suggestions[:10]:
                story.append(Paragraph(f"• {suggestion}", styles['Normal']))
        else:
            story.append(Paragraph("No additional recommendations.", styles['Normal']))

        story.append(Spacer(1, 18))
        disclaimer = (
            "Outputs generated by LawBot 360 are drafting aids for educational purposes only "
            "and do not constitute legal advice. Please consult a qualified advocate for final review."
        )
        story.append(Paragraph(disclaimer, styles['Italic']))

        doc.build(story)

        return str(summary_path)


