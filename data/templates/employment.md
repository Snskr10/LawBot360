# EMPLOYMENT AGREEMENT

**Date:** {{ effective_date }}

## PARTIES

**Employer:** {{ parties[0] if parties else 'Company Name' }}  
**Employee:** {{ parties[1] if parties|length > 1 else 'Employee Name' }}

## POSITION

The Employee shall be employed in the position of **{{ position|default('Software Engineer') }}**, reporting to {{ supervisor|default('Department Head') }}.

## TERM

This Agreement shall commence on {{ start_date|default(effective_date) }} and shall continue until terminated in accordance with the terms herein.

## COMPENSATION

The Employee shall receive:

- **Base Salary:** {{ salary|default('₹8,00,000 per annum') }}
- **Payment Frequency:** Monthly
- **Additional Benefits:** As per company policy

## DUTIES AND RESPONSIBILITIES

The Employee agrees to:

1. Devote full time and attention to the performance of duties
2. Follow all company policies and procedures
3. Maintain confidentiality of company information
4. Perform duties with due diligence and care

## NOTICE PERIOD

Either party may terminate this Agreement by providing {{ notice_period|default('two (2) months') }} written notice to the other party.

## CONFIDENTIALITY

The Employee agrees to maintain strict confidentiality regarding all proprietary and confidential information of the Company, both during employment and after termination.

## INTELLECTUAL PROPERTY

All intellectual property, inventions, and work product created by the Employee in the course of employment shall be the exclusive property of the Company.

## TERMINATION

This Agreement may be terminated:

1. By either party with {{ notice_period|default('two (2) months') }} written notice
2. Immediately by the Company for cause (misconduct, breach of agreement)
3. By mutual agreement

## RESTRICTIVE COVENANTS

{% if include_non_solicit %}
The Employee agrees not to solicit employees or customers of the Company for a period of {{ non_solicit_period|default('one (1) year') }} after termination.
{% endif %}

{% if include_non_compete %}
The Employee agrees not to compete with the Company in similar business for a period of {{ non_compete_period|default('one (1) year') }} after termination.
{% endif %}

## GOVERNING LAW

This Agreement shall be governed by and construed in accordance with the laws of {{ governing_law }}.

## DISPUTE RESOLUTION

Any dispute arising out of or relating to this Agreement shall be resolved through {{ dispute_resolution }}.

## SIGNATURES

**Employer:** _________________    Date: _________

**Employee:** _________________    Date: _________

---
*This document is generated for educational purposes only. Consult a qualified lawyer for legal advice.*


