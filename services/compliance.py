import re
from typing import List, Dict, Any
from models.schemas import ComplianceCheck, ComplianceResponse

class ComplianceChecker:
    """Checks financial and statutory compliance"""
    
    def __init__(self):
        # GST compliance rules
        self.gst_patterns = {
            'registration_required': r'gstin|gst\s+registration|goods\s+and\s+services\s+tax',
            'invoice_fields': r'invoice|tax\s+invoice|gstin|hsn|sac',
            'payment_timeline': r'payment\s+within|days\s+of\s+invoice|credit\s+period'
        }
        
        # TDS compliance
        self.tds_patterns = {
            'threshold_mention': r'tds|tax\s+deducted\s+at\s+source|withholding',
            'rates': r'\d+%\s+tds|tds\s+at\s+\d+%'
        }
        
        # Companies Act (India)
        self.companies_act_patterns = {
            'board_approval': r'board\s+approval|board\s+resolution',
            'related_party': r'related\s+party|related\s+person'
        }
        
        # MSME Act
        self.msme_patterns = {
            'payment_rule': r'45\s+days|msme|micro.*small.*medium',
            'supplier_relation': r'supplier|vendor|service\s+provider'
        }
        
        # IT Act / Data Protection
        self.data_protection_patterns = {
            'data_processing': r'data\s+processing|personal\s+data|personal\s+information',
            'breach_notification': r'data\s+breach|breach\s+notification|security\s+incident'
        }
    
    def check(self, text: str, jurisdiction: str = 'IN') -> Dict[str, Any]:
        """Check compliance for given text"""
        checks = []
        text_lower = text.lower()
        
        if jurisdiction == 'IN':
            # GST checks
            if self._has_commercial_transaction(text_lower):
                checks.extend(self._check_gst(text_lower))
            
            # TDS checks
            checks.extend(self._check_tds(text_lower))
            
            # Companies Act checks
            checks.extend(self._check_companies_act(text_lower))
            
            # MSME Act checks
            checks.extend(self._check_msme(text_lower))
            
            # Data Protection checks
            checks.extend(self._check_data_protection(text_lower))
        
        # Determine overall status
        overall_status = 'pass'
        if any(c.get('status') == 'fail' for c in checks):
            overall_status = 'fail'
        elif any(c.get('status') == 'warn' for c in checks):
            overall_status = 'warn'
        
        return {
            'checks': checks,
            'overall_status': overall_status
        }
    
    def _has_commercial_transaction(self, text: str) -> bool:
        """Check if text involves commercial transaction"""
        keywords = ['payment', 'invoice', 'purchase', 'sale', 'service', 'supply']
        return any(keyword in text for keyword in keywords)
    
    def _check_gst(self, text: str) -> List[Dict]:
        """Check GST compliance"""
        checks = []
        
        # Check if GST mentioned
        has_gst = bool(re.search(self.gst_patterns['registration_required'], text))
        has_invoice_fields = bool(re.search(self.gst_patterns['invoice_fields'], text))
        has_payment_timeline = bool(re.search(self.gst_patterns['payment_timeline'], text))
        
        if self._has_commercial_transaction(text):
            if not has_gst:
                checks.append({
                    'category': 'GST',
                    'status': 'warn',
                    'message': 'GST registration and invoicing requirements not mentioned',
                    'citation': 'GST Act, 2017'
                })
            elif not has_invoice_fields:
                checks.append({
                    'category': 'GST',
                    'status': 'warn',
                    'message': 'GST invoice fields (GSTIN, HSN/SAC) not clearly specified',
                    'citation': 'GST Act, 2017'
                })
            else:
                checks.append({
                    'category': 'GST',
                    'status': 'pass',
                    'message': 'GST compliance elements mentioned',
                    'citation': None
                })
        
        return checks
    
    def _check_tds(self, text: str) -> List[Dict]:
        """Check TDS compliance"""
        checks = []
        
        has_tds_mention = bool(re.search(self.tds_patterns['threshold_mention'], text))
        has_tds_rates = bool(re.search(self.tds_patterns['rates'], text))
        
        # If payment amount > threshold likely, check for TDS
        # For MVP, just check if mentioned
        if self._has_large_payment(text) and not has_tds_mention:
            checks.append({
                'category': 'TDS',
                'status': 'warn',
                'message': 'TDS withholding not mentioned for large payments',
                'citation': 'Income Tax Act, 1961'
            })
        elif has_tds_mention:
            if not has_tds_rates:
                checks.append({
                    'category': 'TDS',
                    'status': 'warn',
                    'message': 'TDS mentioned but rates/thresholds not specified',
                    'citation': 'Income Tax Act, 1961'
                })
            else:
                checks.append({
                    'category': 'TDS',
                    'status': 'pass',
                    'message': 'TDS compliance mentioned',
                    'citation': None
                })
        
        return checks
    
    def _check_companies_act(self, text: str) -> List[Dict]:
        """Check Companies Act compliance"""
        checks = []
        
        # Check for related party transactions
        has_related_party = bool(re.search(self.companies_act_patterns['related_party'], text))
        has_board_approval = bool(re.search(self.companies_act_patterns['board_approval'], text))
        
        if has_related_party and not has_board_approval:
            checks.append({
                'category': 'Companies Act',
                'status': 'warn',
                'message': 'Related party transaction mentioned but board approval not referenced',
                'citation': 'Companies Act, 2013'
            })
        
        return checks
    
    def _check_msme(self, text: str) -> List[Dict]:
        """Check MSME Act compliance"""
        checks = []
        
        has_msme = bool(re.search(self.msme_patterns['payment_rule'], text))
        has_supplier = bool(re.search(self.msme_patterns['supplier_relation'], text))
        
        if has_supplier and not has_msme:
            checks.append({
                'category': 'MSME Act',
                'status': 'warn',
                'message': 'Supplier relationship mentioned but 45-day payment rule not specified',
                'citation': 'MSME Development Act, 2006'
            })
        elif has_msme:
            checks.append({
                'category': 'MSME Act',
                'status': 'pass',
                'message': 'MSME payment timelines mentioned',
                'citation': None
            })
        
        return checks
    
    def _check_data_protection(self, text: str) -> List[Dict]:
        """Check data protection compliance"""
        checks = []
        
        has_data_processing = bool(re.search(self.data_protection_patterns['data_processing'], text))
        has_breach_notification = bool(re.search(self.data_protection_patterns['breach_notification'], text))
        
        if has_data_processing:
            if not has_breach_notification:
                checks.append({
                    'category': 'Data Protection',
                    'status': 'warn',
                    'message': 'Data processing mentioned but breach notification procedures not specified',
                    'citation': 'IT Act 2000, DPDP Act'
                })
            else:
                checks.append({
                    'category': 'Data Protection',
                    'status': 'pass',
                    'message': 'Data protection measures mentioned',
                    'citation': None
                })
        
        return checks
    
    def _has_large_payment(self, text: str) -> bool:
        """Heuristic to detect large payments (>1 lakh)"""
        # Look for amounts
        amount_pattern = r'[₹]\s*(\d+(?:,\d{3})*(?:\.\d{2})?)'
        amounts = re.findall(amount_pattern, text)
        
        for amount_str in amounts:
            try:
                # Remove commas
                amount = float(amount_str.replace(',', ''))
                if amount >= 100000:  # 1 lakh
                    return True
            except:
                pass
        
        return False


