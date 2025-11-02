# NON-DISCLOSURE AGREEMENT

**Date:** {{ effective_date }}

## PARTIES

This Non-Disclosure Agreement ("Agreement") is entered into between:

{% for party in parties %}
- **{{ party }}**
{% endfor %}

(collectively referred to as the "Parties")

## PURPOSE

The Parties wish to engage in discussions regarding potential business opportunities and may share confidential information with each other.

## CONFIDENTIAL INFORMATION

For purposes of this Agreement, "Confidential Information" means all non-public, proprietary, or confidential information disclosed by one Party to the other, whether orally, in writing, or in any other form, including but not limited to:

1. Business plans, strategies, and financial information
2. Technical data, know-how, and trade secrets
3. Customer lists and relationships
4. Marketing and sales information
5. Any other information marked as "Confidential" or "Proprietary"

## OBLIGATIONS

Each Party agrees to:

1. Hold and maintain the Confidential Information in strict confidence
2. Not disclose the Confidential Information to any third party without prior written consent
3. Use the Confidential Information solely for the purpose of evaluating the business opportunity
4. Return or destroy all Confidential Information upon request

## EXCEPTIONS

This Agreement does not apply to information that:

1. Was publicly known prior to disclosure
2. Becomes publicly known through no breach of this Agreement
3. Was rightfully received from a third party without breach of confidentiality
4. Was independently developed without use of the Confidential Information

## DURATION

This Agreement shall remain in effect for {{ confidentiality_duration|default('three (3) years') }} from the date of last disclosure, or until terminated by mutual written consent.

## GOVERNING LAW

This Agreement shall be governed by and construed in accordance with the laws of {{ governing_law }}.

## DISPUTE RESOLUTION

Any dispute arising out of or relating to this Agreement shall be resolved through {{ dispute_resolution }}.

## SIGNATURES

IN WITNESS WHEREOF, the Parties have executed this Agreement as of the date first written above.

**{{ parties[0] if parties else 'Party A' }}:** _________________    Date: _________

**{{ parties[1] if parties|length > 1 else 'Party B' }}:** _________________    Date: _________

---
*This document is generated for educational purposes only. Consult a qualified lawyer for legal advice.*


