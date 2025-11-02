# COMMERCIAL LEASE AGREEMENT

**Date:** {{ effective_date }}

## PREMISES

The Lessor hereby leases to the Lessee the premises located at **{{ premises_address|default('Full address of property') }}** comprising **{{ premises_area|default('1000 sq. ft.') }}** for commercial use.

## TERM

Lease term shall commence on {{ start_date|default(effective_date) }} and continue for {{ lease_term|default('36 months') }} unless terminated earlier in accordance with this Agreement.

## RENT AND DEPOSIT

- Monthly Rent: {{ rent_amount|default('₹75,000') }} payable on or before the 5th day of each month.
- Security Deposit: {{ security_deposit|default('₹2,25,000 (3 months rent)') }} refundable upon termination subject to deductions.

## USE OF PREMISES

Premises shall be used solely for {{ permitted_use|default('office operations') }} and not for any unlawful or hazardous activities.

## MAINTENANCE

Lessor shall be responsible for structural maintenance; Lessee shall maintain interiors and promptly report issues. Utilities shall be borne by the Lessee.

## ALTERATIONS

Lessee shall not make structural alterations without prior written consent of the Lessor. Any approved alterations shall comply with applicable laws.

## INSURANCE

Lessee shall maintain adequate insurance coverage for assets and public liability within the premises.

## TERMINATION

Either party may terminate with {{ termination_notice|default('3 months') }} written notice after completion of lock-in period of {{ lock_in|default('12 months') }}. Early termination by Lessee results in forfeiture of security deposit unless otherwise agreed.

## SUBLETTING

Sublicensing or assignment of the premises requires prior written consent of the Lessor.

## GOVERNING LAW & DISPUTE RESOLUTION

This Agreement shall be governed by the laws of {{ governing_law }}. Disputes shall be resolved via {{ dispute_resolution|default('arbitration in accordance with Arbitration and Conciliation Act, 1996') }}.

## SIGNATURES

**Lessor:** ____________________    Date: _________

**Lessee:** ____________________    Date: _________

---
*Educational template only; seek professional legal advice.*
