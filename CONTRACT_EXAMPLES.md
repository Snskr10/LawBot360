# Contract Creation Examples

## API Endpoint
```
POST /api/contracts/generate
Content-Type: application/json
Authorization: Bearer <your_jwt_token>
```

## Example 1: NDA (Non-Disclosure Agreement)

```json
{
  "contract_type": "NDA",
  "parties": [
    "TechCorp Solutions Pvt. Ltd.",
    "Innovation Labs India"
  ],
  "terms": {
    "effective_date": "2025-01-15",
    "consideration": "For the purpose of exploring potential business collaboration",
    "scope": "Confidential information related to proprietary technology, business strategies, and customer data",
    "confidentiality": "The receiving party shall maintain strict confidentiality and not disclose any confidential information to third parties for a period of 3 years from the date of disclosure",
    "termination": "This agreement shall remain in effect for 3 years or until terminated by mutual written consent",
    "dispute": "Any disputes shall be resolved through arbitration in Mumbai, India, in accordance with the Arbitration and Conciliation Act, 1996"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Example 2: Employment Contract

```json
{
  "contract_type": "Employment",
  "parties": [
    "ABC Technologies Pvt. Ltd.",
    "John Doe"
  ],
  "terms": {
    "effective_date": "2025-02-01",
    "consideration": "Employment as Senior Software Engineer",
    "scope": "Design, develop, and maintain software applications. Participate in code reviews and technical discussions.",
    "payment": "Monthly salary of ₹1,50,000 plus applicable benefits including Provident Fund, Health Insurance, and Annual Bonus",
    "taxes": "All applicable taxes including TDS shall be deducted as per Income Tax Act, 1961",
    "ip": "All intellectual property created during employment shall vest in the employer",
    "confidentiality": "Employee shall maintain confidentiality of all company information during and after employment",
    "termination": "Either party may terminate with 30 days written notice. Company may terminate immediately for cause",
    "dispute": "Disputes shall be resolved through arbitration in accordance with the Arbitration and Conciliation Act, 1996"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Example 3: Service Agreement

```json
{
  "contract_type": "Service",
  "parties": [
    "Client Company Ltd.",
    "Service Provider Inc."
  ],
  "terms": {
    "effective_date": "2025-01-20",
    "consideration": "Provision of software development and consulting services",
    "scope": "Development of web application, mobile app, and ongoing maintenance and support services",
    "payment": "Payment of ₹50,00,000 as follows: 30% advance, 40% on milestone completion, 30% on final delivery",
    "taxes": "GST @ 18% shall be applicable as per CGST Act, 2017",
    "ip": "All deliverables and intellectual property rights shall vest in the client upon full payment",
    "confidentiality": "Both parties agree to maintain confidentiality of all shared information",
    "termination": "Either party may terminate with 60 days written notice. Client may terminate for breach with 30 days notice",
    "dispute": "Disputes shall be resolved through arbitration in Delhi, India"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Example 4: Partnership Agreement

```json
{
  "contract_type": "Partnership",
  "parties": [
    "Partner A - Rajesh Kumar",
    "Partner B - Priya Sharma",
    "Partner C - Amit Patel"
  ],
  "terms": {
    "effective_date": "2025-03-01",
    "consideration": "Formation of partnership firm for conducting business in software development",
    "scope": "Partners agree to contribute capital, skills, and efforts to the partnership business",
    "payment": "Profits and losses shall be shared equally among all partners (33.33% each)",
    "ip": "All intellectual property created by the partnership shall be owned jointly by all partners",
    "confidentiality": "Partners shall maintain confidentiality of partnership affairs",
    "termination": "Partnership may be dissolved by mutual consent or as per Partnership Act, 1932",
    "dispute": "Disputes between partners shall be resolved through mutual discussion or arbitration"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Example 5: Lease Agreement

```json
{
  "contract_type": "Lease",
  "parties": [
    "Property Owner - ABC Real Estate",
    "Tenant - XYZ Corporation"
  ],
  "terms": {
    "effective_date": "2025-04-01",
    "consideration": "Lease of commercial property located at 123 Business Street, Mumbai",
    "scope": "Lease of 5000 sq. ft. office space for commercial use",
    "payment": "Monthly rent of ₹2,00,000 payable in advance. Security deposit of ₹6,00,000",
    "taxes": "GST on rent @ 18% shall be paid by tenant as per CGST Act, 2017",
    "termination": "Lease term is 3 years. Either party may terminate with 90 days written notice",
    "dispute": "Disputes shall be subject to the jurisdiction of courts in Mumbai"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Example 6: Simple NDA (Minimal Data)

```json
{
  "contract_type": "NDA",
  "parties": [
    "Company A",
    "Company B"
  ],
  "terms": {
    "consideration": "Mutual exchange of confidential information",
    "confidentiality": "Standard confidentiality obligations for 2 years"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Example 7: Service Agreement (Hindi Language)

```json
{
  "contract_type": "Service",
  "parties": [
    "ग्राहक कंपनी",
    "सेवा प्रदाता"
  ],
  "terms": {
    "effective_date": "2025-01-15",
    "consideration": "सॉफ्टवेयर विकास सेवाएं प्रदान करना",
    "scope": "वेब एप्लिकेशन और मोबाइल ऐप विकसित करना",
    "payment": "₹25,00,000 का भुगतान",
    "termination": "30 दिन की सूचना के साथ समाप्त किया जा सकता है"
  },
  "jurisdiction": "IN",
  "language": "hi"
}
```

## Required Fields

- **contract_type**: Required - Type of contract (e.g., "NDA", "Employment", "Service", "Partnership", "Lease")
- **parties**: Required - Array of party names (minimum 2 parties)
- **terms**: Optional - Dictionary with contract terms (will use defaults if not provided)
- **jurisdiction**: Optional - Defaults to "IN" (India). Options: "IN", "US", "UK"
- **language**: Optional - Defaults to "en" (English). Options: "en", "hi"

## Optional Terms Fields

All fields in `terms` are optional and will use defaults if not provided:

- `effective_date`: Date when contract becomes effective (format: "YYYY-MM-DD")
- `consideration`: Purpose/value exchange
- `scope`: Scope of work/services
- `payment`: Payment terms and amounts
- `taxes`: Tax-related clauses
- `ip`: Intellectual property clauses
- `confidentiality`: Confidentiality obligations
- `termination`: Termination conditions
- `dispute`: Dispute resolution mechanism
- `nda`: Boolean for NDA inclusion

## Response Format

```json
{
  "contract_id": 1,
  "html": "<html>Generated contract HTML</html>",
  "pdf_url": "/api/contracts/1/pdf",
  "docx_url": "/api/contracts/1/docx",
  "summary": {
    "parties": ["Party A", "Party B"],
    "contract_type": "NDA"
  },
  "markdown": "# Generated contract markdown..."
}
```

## Testing with cURL

```bash
# Example API call
curl -X POST http://localhost:5000/api/contracts/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "contract_type": "NDA",
    "parties": ["Company A", "Company B"],
    "terms": {
      "consideration": "Mutual exchange of information",
      "confidentiality": "2 years confidentiality period"
    },
    "jurisdiction": "IN",
    "language": "en"
  }'
```

## Testing with JavaScript/TypeScript

```typescript
import { generateContract } from './api/client';

const contractData = {
  contract_type: "NDA",
  parties: ["Company A", "Company B"],
  terms: {
    consideration: "Mutual exchange of information",
    confidentiality: "2 years confidentiality period"
  },
  jurisdiction: "IN",
  language: "en"
};

try {
  const result = await generateContract(contractData);
  console.log('Contract ID:', result.contract_id);
  console.log('PDF URL:', result.pdf_url);
} catch (error) {
  console.error('Error:', error);
}
```

