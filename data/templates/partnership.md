# PARTNERSHIP AGREEMENT

**Date:** {{ effective_date }}

## PARTNERS

This Partnership Agreement is entered into between:

{% for partner in partners %}
- **{{ partner.name|default('Partner Name') }}** holding {{ partner.share|default('50%') }} profit share
{% endfor %}

(collectively referred to as the "Partners").

## BUSINESS

The Partners agree to conduct business under the name **{{ firm_name|default('Firm Name LLP') }}** with its principal place of business at {{ firm_address|default('Registered address') }}.

## CAPITAL CONTRIBUTIONS

Each Partner shall contribute capital as follows:

{% for partner in partners %}
- {{ partner.name|default('Partner') }}: {{ partner.capital|default('₹5,00,000') }}
{% endfor %}

## PROFITS AND LOSSES

Profits and losses shall be shared in proportion to the Partners' respective profit shares unless otherwise unanimously agreed in writing.

## MANAGEMENT

Decisions shall be made by majority vote of Partners. Matters involving capital expenditure above {{ approval_threshold|default('₹2,00,000') }} require unanimous consent.

## DUTIES AND RESTRICTIONS

Partners shall devote adequate time and attention to the partnership business and shall not engage in competing activities without consent of other Partners.

## BANKING

Partnership funds shall be deposited in a designated bank account requiring signatures of any two Partners for withdrawals.

## BOOKS AND RECORDS

Proper accounts shall be maintained and audited annually. Each Partner may inspect books upon reasonable notice.

## ADMISSION & RETIREMENT

New Partners may be admitted only with unanimous consent. A Partner may retire by giving {{ retirement_notice|default('90 days') }} written notice. Settlement shall be based on capital account plus share of profits till retirement date.

## DISSOLUTION

The Partnership may be dissolved by unanimous decision or upon occurrence of events specified in the Indian Partnership Act, 1932. Assets and liabilities shall be distributed as per capital accounts.

## DISPUTE RESOLUTION

Disputes shall be resolved through {{ dispute_resolution|default('arbitration in accordance with Arbitration and Conciliation Act, 1996') }}.

## GOVERNING LAW

This Agreement shall be governed by the laws of {{ governing_law }}.

## SIGNATURES

{% for partner in partners %}
**{{ partner.name|default('Partner') }}:** ____________________    Date: _________
{% endfor %}

---
*Educational template only; seek professional legal counsel before execution.*
