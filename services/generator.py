import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from config import Config
from jinja2 import Template
from markdown import markdown
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover - fallback for older SDKs
    OpenAI = None

class ContractGenerator:
    """Generates contracts from templates and natural language inputs"""
    
    def __init__(self):
        self.templates_path: Path = Path(Config.TEMPLATES_DATA_PATH)
        self.export_path: Path = Path(Config.EXPORT_FOLDER)
        self.export_path.mkdir(parents=True, exist_ok=True)

        self.openai_api_key = Config.OPENAI_API_KEY
        self.client = None
        if self.openai_api_key and OpenAI:
            try:
                self.client = OpenAI(api_key=self.openai_api_key)
            except Exception as exc:
                # Fail gracefully if SDK initialisation fails; downstream calls will use fallbacks
                print(f"OpenAI client initialisation failed: {exc}")
                self.client = None
        
        # Jurisdiction profiles
        self.jurisdiction_profiles = {
            'IN': {
                'governing_law': 'Laws of India',
                'default_dispute': 'Arbitration in accordance with Arbitration and Conciliation Act, 1996',
                'mandatory_clauses': ['parties', 'consideration', 'governing_law', 'signatures']
            },
            'US': {
                'governing_law': 'Laws of the United States',
                'default_dispute': 'Arbitration in accordance with Federal Arbitration Act',
                'mandatory_clauses': ['parties', 'consideration', 'governing_law', 'signatures']
            },
            'UK': {
                'governing_law': 'Laws of England and Wales',
                'default_dispute': 'Arbitration in accordance with Arbitration Act 1996',
                'mandatory_clauses': ['parties', 'consideration', 'governing_law', 'signatures']
            }
        }
    
    def generate(self, contract_type, parties, terms, jurisdiction='IN', language='en'):
        """Generate a contract"""
        # Load template
        template_path = self.templates_path / f"{contract_type.lower()}.md"
        if not template_path.exists():
            template_content = self._get_default_template(contract_type)
        else:
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
        
        # Get jurisdiction profile
        profile = self.jurisdiction_profiles.get(jurisdiction, self.jurisdiction_profiles['IN'])
        
        # Prepare template variables
        template_vars = {
            'contract_type': contract_type,
            'parties': parties or ['Party A', 'Party B'],
            'effective_date': terms.get('effective_date', datetime.now().strftime('%Y-%m-%d')),
            'consideration': terms.get('consideration', 'Mutual promises'),
            'scope': terms.get('scope', 'Services to be provided'),
            'payment': terms.get('payment', 'As agreed'),
            'taxes': terms.get('taxes', 'As per applicable law'),
            'ip': terms.get('ip', 'All IP shall vest in the service provider'),
            'confidentiality': terms.get('confidentiality', 'Standard confidentiality obligations'),
            'termination': terms.get('termination', 'Either party may terminate with 30 days notice'),
            'governing_law': profile['governing_law'],
            'dispute_resolution': terms.get('dispute', profile['default_dispute']),
            'nda': terms.get('nda', True),
            'jurisdiction': jurisdiction,
            'language': language
        }
        
        # Render template
        template = Template(template_content)
        rendered_markdown = template.render(**template_vars)

        # LLM polish (if API key available)
        polished_markdown = rendered_markdown
        if self.client:
            try:
                polished_markdown = self._polish_with_llm(rendered_markdown, contract_type, jurisdiction)
            except Exception as exc:
                print(f"LLM polish failed: {exc}")

        html_content = markdown(polished_markdown, extensions=["extra", "sane_lists"])

        # Generate file paths
        contract_id = uuid4().hex
        html_path = self.export_path / f"contract_{contract_id}.html"
        pdf_path = self.export_path / f"contract_{contract_id}.pdf"
        docx_path = self.export_path / f"contract_{contract_id}.docx"

        # Save HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Generate PDF (using markdown text for readability)
        self._generate_pdf(polished_markdown, pdf_path)

        # Generate DOCX
        self._generate_docx(polished_markdown, docx_path)
        
        # Generate summary
        summary = {
            'contract_type': contract_type,
            'parties': parties,
            'key_terms': {
                'payment': template_vars['payment'],
                'termination': template_vars['termination'],
                'jurisdiction': jurisdiction
            }
        }
        
        return {
            'html': html_content,
            'html_path': str(html_path),
            'pdf_path': str(pdf_path),
            'docx_path': str(docx_path),
            'summary': summary,
            'markdown': polished_markdown
        }
    
    def explain_clause(self, text, context=None, language='en', jurisdiction='IN'):
        """Explain a legal clause using RAG context"""
        if not context:
            context = []
        
        # Build context prompt
        context_text = ""
        if context:
            context_text = "\n\nRelevant Legal Sections:\n"
            for section in context:
                act = section.get('act_name', 'Unknown Act')
                section_code = section.get('section_code', '')
                content = section.get('content', '')
                context_text += f"\n{act} - {section_code}:\n{content}\n"
        
        prompt = f"""Explain the following legal query in plain language, focusing on Indian law:

Query: {text}
{context_text}

Provide a clear, educational explanation. Include relevant legal provisions if available. 
Remember: This is educational information only, not legal advice."""

        # Use LLM if available, otherwise return a simple explanation
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a legal assistant providing educational information about Indian laws. Always remind users to consult a lawyer for specific legal matters."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    max_tokens=1000,
                    timeout=10  # Add timeout to prevent hanging
                )
                return response.choices[0].message.content
            except Exception as exc:
                print(f"OpenAI API call failed: {exc}")
                # Fall through to fallback response
        
        # Fallback: Return explanation based on context
        if context:
            explanations = []
            for section in context:
                act = section.get('act_name', 'Unknown Act')
                section_code = section.get('section_code', '')
                content = section.get('content', '')
                explanations.append(f"According to {act}, {section_code}: {content}")
            
            return f"""Based on relevant legal sections, here's what you should know about "{text}":

{chr(10).join(explanations)}

**Important:** This is educational information only. For specific legal advice regarding your situation, please consult a qualified lawyer."""
        
        return f"""I can help explain legal concepts related to "{text}". However, I don't have specific information about this query in my knowledge base right now.

**Important:** This is educational information only. For specific legal advice, please consult a qualified lawyer. You can also try rephrasing your question or being more specific about which law or act you're asking about."""
    
    def _polish_with_llm(self, content, contract_type, jurisdiction):
        """Polish contract language using LLM"""
        prompt = f"""Review and polish this {contract_type} contract for {jurisdiction} jurisdiction.
Ensure legal consistency, proper terminology, and completeness.
Return only the polished contract text, no additional commentary.

Contract:
{content[:3000]}
"""
        if not self.client:
            return content

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a legal drafting assistant. Provide educational outputs only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
        )
        return response.choices[0].message.content
    
    def _generate_pdf(self, markdown_content: str, pdf_path: Path):
        """Generate PDF from markdown content"""
        doc = SimpleDocTemplate(str(pdf_path), pagesize=letter)
        styles = getSampleStyleSheet()
        story = []

        for line in self._markdown_to_plaintext_lines(markdown_content):
            para = Paragraph(line, styles['Normal'])
            story.append(para)
            story.append(Spacer(1, 12))

        doc.build(story)
    
    def _generate_docx(self, markdown_content: str, docx_path: Path):
        """Generate DOCX from markdown content"""
        doc = Document()
        for line in self._markdown_to_plaintext_lines(markdown_content):
            doc.add_paragraph(line)
        doc.save(str(docx_path))

    def _markdown_to_plaintext_lines(self, markdown_content: str):
        """Convert markdown into human-readable lines for exports"""
        lines = []
        for raw_line in markdown_content.splitlines():
            line = raw_line.strip()
            if not line:
                continue

            # Headings
            if line.startswith('#'):
                line = line.lstrip('#').strip().upper()

            # Bullet points
            if line.startswith(('- ', '* ')):
                line = f"• {line[2:].strip()}"

            line = line.replace('**', '').replace('__', '')
            lines.append(line)
        return lines
    
    def _get_default_template(self, contract_type):
        """Default template if file doesn't exist"""
        return """# {contract_type} AGREEMENT

**Date:** {{ effective_date }}

## PARTIES
{% for party in parties %}
- {{ party }}
{% endfor %}

## CONSIDERATION
{{ consideration }}

## SCOPE OF WORK
{{ scope }}

## PAYMENT TERMS
{{ payment }}

## INTELLECTUAL PROPERTY
{{ ip }}

## CONFIDENTIALITY
{{ confidentiality }}

## TERMINATION
{{ termination }}

## GOVERNING LAW
This agreement shall be governed by the laws of {{ governing_law }}.

## DISPUTE RESOLUTION
{{ dispute_resolution }}

## SIGNATURES

Party A: _________________    Date: _________

Party B: _________________    Date: _________

---
*This document is generated for educational purposes only. Consult a qualified lawyer for legal advice.*
""".format(contract_type=contract_type.upper())


