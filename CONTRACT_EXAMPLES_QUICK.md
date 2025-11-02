# Quick Contract Creation Examples

## 1. Basic NDA (Simplest)

```json
{
  "contract_type": "NDA",
  "parties": ["Acme Corp", "Beta Inc"],
  "terms": {
    "consideration": "Information exchange for potential collaboration"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## 2. Employment Contract

```json
{
  "contract_type": "Employment",
  "parties": ["Tech Solutions Pvt Ltd", "Employee Name"],
  "terms": {
    "payment": "₹80,000 per month plus PF and health insurance",
    "scope": "Software development and maintenance",
    "termination": "30 days notice required"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## 3. Service Agreement (Detailed)

```json
{
  "contract_type": "Service",
  "parties": ["Client Company", "Service Provider"],
  "terms": {
    "effective_date": "2025-01-15",
    "consideration": "Software development services",
    "scope": "Develop web application with user authentication, payment gateway integration, and admin dashboard",
    "payment": "₹30,00,000 total: 40% advance, 40% on completion, 20% on delivery",
    "taxes": "GST @ 18% applicable",
    "ip": "All IP rights transfer to client on full payment",
    "confidentiality": "Both parties maintain confidentiality",
    "termination": "60 days written notice required",
    "dispute": "Arbitration in Mumbai as per Arbitration Act, 1996"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## 4. Partnership Agreement

```json
{
  "contract_type": "Partnership",
  "parties": ["Partner 1", "Partner 2", "Partner 3"],
  "terms": {
    "consideration": "Formation of partnership for software consulting business",
    "payment": "Equal profit sharing (33.33% each)",
    "termination": "As per Partnership Act, 1932"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## 5. Lease Agreement

```json
{
  "contract_type": "Lease",
  "parties": ["Property Owner", "Tenant Company"],
  "terms": {
    "consideration": "Lease of 3000 sq ft commercial space",
    "payment": "₹1,50,000 monthly rent, ₹4,50,000 security deposit",
    "taxes": "GST @ 18% on rent",
    "termination": "3 year lease, 90 days notice for termination"
  },
  "jurisdiction": "IN",
  "language": "en"
}
```

## Minimum Required Fields

```json
{
  "contract_type": "NDA",
  "parties": ["Party A", "Party B"]
}
```

All other fields will use sensible defaults!

