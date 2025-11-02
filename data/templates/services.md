# SERVICE AGREEMENT

**Date:** {{ effective_date }}

## PARTIES

**Client:** {{ parties[0] if parties else 'Client Name' }}  
**Service Provider:** {{ parties[1] if parties|length > 1 else 'Service Provider Name' }}

## SCOPE OF SERVICES

The Service Provider shall perform the following services:

{{ scope|default('Detailed description of services to be delivered') }}

Deliverables shall be provided according to the agreed project plan.

## PAYMENT TERMS

- Total Fee: {{ payment|default('₹1,50,000 + applicable taxes') }}
- Payment Schedule: {{ payment_schedule|default('40% advance, 30% milestone, 30% on completion') }}
- Taxes: {{ taxes|default('GST at applicable rates') }}

## TIMELINE

Services will commence on {{ start_date|default(effective_date) }} and conclude by {{ end_date|default('agreed completion date') }}.

## CONFIDENTIALITY

Both parties agree to maintain confidentiality of proprietary information shared under this Agreement.

## INTELLECTUAL PROPERTY

{% if ip_ownership == 'client' %}
All deliverables and intellectual property developed under this Agreement shall vest with the Client upon full payment.
{% else %}
The Service Provider retains ownership of pre-existing IP. Custom deliverables are assigned to the Client upon full payment.
{% endif %}

## WARRANTIES

The Service Provider warrants that services shall be performed with professional diligence and accordance with prevailing industry standards.

## TERMINATION

Either party may terminate this Agreement with {{ termination_notice|default('30 days') }} written notice. In case of breach, the non-breaching party may terminate with immediate effect after giving the breaching party 15 days to cure the breach.

## LIMITATION OF LIABILITY

Liability of each party is capped at {{ liability_cap|default('aggregate fees paid under this Agreement') }} and excludes consequential damages.

## DISPUTE RESOLUTION

Disputes shall be resolved through {{ dispute_resolution|default('arbitration in accordance with Arbitration and Conciliation Act, 1996') }}.

## GOVERNING LAW

This Agreement shall be governed by the laws of {{ governing_law }}.

## SIGNATURES

**Client:** ____________________    Date: _________

**Service Provider:** ____________________    Date: _________

---
*Generated for educational purposes only. Obtain legal review before execution.*
