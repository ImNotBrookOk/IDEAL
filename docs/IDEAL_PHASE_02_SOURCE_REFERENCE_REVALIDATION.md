# IDEAL Phase 02 — Official Source Reference Revalidation

**Status:** Targeted source revalidation; research evidence only  
**Checkpoint:** 090 — 17 November 2026  
**Scope:** New Zealand privacy/tax references and core security/host-hardening references  
**Boundary:** Not legal advice, regulatory certification, a provider eligibility determination or implementation approval.

## 1. Executive result

The core source positions remain directionally consistent with IDEAL's architecture, but several nuances need to be preserved explicitly. The most important are the amended wording of Privacy Act 2020 section 27, the distinction between agent-only processing and a provider's own-purpose use, the CARF exclusion for own-benefit activity, and inconsistent future CARF account-registration dates across two Inland Revenue pages.

No new owner decision is created. New Zealand crypto-perpetual tax treatment remains unresolved and requires specialist advice before any tax rules are encoded.

## 2. New Zealand privacy sources

### Privacy Act 2020 — section 27

The current consolidated Act page is stated to be in force as at 8 October 2026. Section 27 is a conditional personal/domestic-affairs exception for an individual:
- IPPs 1–3A and 4(b) do not apply to an individual collecting personal information solely for personal/domestic affairs.
- IPPs 5–12 do not apply to an individual holding information solely for those purposes where it was collected lawfully, received unsolicited, or created by the individual.
- The exception does not apply where collection, use or disclosure would be highly offensive to a reasonable person.
- Section 27 does not automatically exempt a separate cloud, bank-data, AI or other provider agency, nor does it decide the provider's contractual duties or the consequences of the provider using information for its own purposes.

The amendment history matters: section 27(1) was amended on 1 May 2026; section 27(2)(b) was replaced on 27 November 2025. Earlier summaries that omit the lawful/unsolicited/created alternatives are incomplete.

### Section 11 and IPP 12

Privacy Act section 11 treats information held by an agency solely as an agent for another agency differently from information the provider uses/discloses for its own purposes. The Office of the Privacy Commissioner explains that agent-only storage/processing is generally not itself an IPP 12 overseas disclosure; the principal remains responsible for the information. If the provider uses/discloses the data for its own purposes, including model training or cross-customer reuse, the analysis changes and both agencies may be treated as holding the information.

IPP 12 still governs qualifying disclosures to foreign persons/entities and requires comparable safeguards or another statutory basis. Do not treat all offshore processing as automatically prohibited, or all processors as automatically exempt. Assess the actual provider role, contract, subprocessor chain, data use and jurisdiction.

## 3. Inland Revenue — cryptoasset records and CARF

### Personal cryptoasset records

IRD's cryptoasset record-keeping page says records supporting a cryptoasset tax position must be kept for at least seven years, even after the cryptoassets are no longer held. The listed evidence includes asset type, transaction date/type, units, NZD value, year-opening/closing units, exchange records, bank statements and wallet addresses.

The page was last updated 28 April 2021. Its scope should not be extended automatically to every derivative/perpetual contract. Whether a particular contract and its associated records fall within the guidance requires current NZ tax interpretation.

### CARF / RCASP

IRD's current CARF overview says New Zealand-connected Reporting Crypto-Asset Service Providers must collect/report from 1 April 2026, retain specified records for seven years, and make the first report by 30 June 2027 for the period 1 April 2026–31 March 2027.

IRD's published exclusions include persons or entities only engaged in crypto-asset activities for their own benefit. A private owner trading for their own account is therefore not an RCASP merely because they use crypto exchanges; the counterparty/platform's separate business role must be assessed. Creating software is also not itself RCASP activity if it does not facilitate exchange/conversion on behalf of users.

**Source discrepancy:** the CARF overview last updated 8 June 2026 says myIR registration will be available from March 2027, while the more recently updated “How to report information” page (6 November 2026) says registration opens 3 December 2026. Do not hard-code either date into IDEAL. This is a provider-facing operational detail and is not relevant to IDEAL's current private single-user research scope.

CARF reporting is an information-reporting regime; it does not itself determine taxable income or create a new tax charge.

## 4. Tax legislation status

IRD Tax Policy's bill page states the Taxation (Annual Rates for 2026–27, FBT Simplification, Foreign Investment Funds, and Remedial Measures) Bill was introduced 10 September 2026 and was at Select Committee stage as at 12 October 2026. Parliament's progress page records its first reading on 15 September and says submissions remain open until a new Finance and Expenditure Committee is convened in the next term.

No enacted change is inferred from the Bill or its proposals. Effective dates and enacted text must be checked before any rule pack uses them.

## 5. Security and host-hardening sources

### NIST

- NIST SP 800-207 Zero Trust Architecture remains the final 2020 publication and supports resource-centric, continuously verified access rather than implicit network/location trust.
- NIST's Key Management project page lists SP 800-57 Part 1 Revision 5 as the final recommendation and notes that Revision 6 was an initial public draft published 5 December 2025 with comments through 5 February 2026. No final Revision 6 was identified on the current project page during this check; use Rev. 5 as the final reference and recheck before implementation.
- NIST CSWP 39 was withdrawn on 29 June 2026 and superseded by CSWP 39-upd1, published 29 June 2026. If crypto-agility guidance is used, cite the updated paper, not the withdrawn version.

### Firecracker

The current upstream production-host setup guidance reinforces that a microVM is not a complete security boundary by itself:
- use Firecracker's jailer or equivalent restrictions;
- retain default restrictive seccomp;
- apply cgroup/resource limits and protect trusted jailer paths;
- patch host/guest kernels and host microcode;
- implement host-level guest-egress filtering because Firecracker does not filter guest network traffic itself;
- bound logs, serial output, resource consumption and noisy-neighbour effects;
- account for host/hardware vulnerabilities and side channels.

This supports the existing IDEAL position that VM isolation is one layer, not a substitute for host trust, network policy or independent containment.

## 6. Source register

- Privacy Act 2020, current consolidated text, section 27: https://www.legislation.govt.nz/act/public/2025/53/en/latest/sections/LMS899135/LMS23347/
- Privacy Act 2020, section 11: https://www.legislation.govt.nz/act/public/2020/31/en/latest/sections/LMS23318/
- Privacy Commissioner, third-party providers: https://www.privacy.org.nz/resources-and-learning/a-z-topics/working-with-third-party-providers/
- Privacy Commissioner, Principle 12: https://www.privacy.org.nz/privacy-principles/12/
- IRD cryptoasset record keeping: https://www.ird.govt.nz/cryptoassets/taxing/record-keeping
- IRD CARF overview: https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/crypto-asset-reporting-framework-overview
- IRD CARF reporting instructions: https://www.ird.govt.nz/international-tax/exchange-of-information/crypto-asset-reporting-framework/reporting-cryptoasset-service-providers/how-to-report-information
- IRD 2026–27 Taxation Bill status: https://www.taxpolicy.ird.govt.nz/bills/2026-fbt-simplification-tax-bill
- New Zealand Parliament, 2026–27 Taxation Bill: https://www.legislation.govt.nz/bill/government/2026/344/en/latest/
- NIST SP 800-207: https://csrc.nist.gov/pubs/sp/800/207/final
- NIST Key Management Guidelines: https://csrc.nist.gov/Projects/Key-Management/Key-Management-Guidelines
- NIST CSWP 39-upd1: https://csrc.nist.gov/pubs/cswp/39/upd1/considerations-for-achieving-crypto-agility/final
- Firecracker production host setup: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md

## 7. Disposition

The existing architecture's privacy, tax, and host-isolation boundaries remain appropriate at the design level. The source review adds precision but does not settle tax classification, provider status, host topology or retention periods. Keep those as explicit open decisions. Phase 02 remains active; Phases 03–19 remain locked.


## 8. Infrastructure security refresh — checkpoint 107 (18 November 2026)

A later targeted refresh is recorded in [Infrastructure Security Source Refresh](IDEAL_PHASE_02_INFRASTRUCTURE_SECURITY_SOURCE_REFRESH.md). It updates Linux kernel and Firecracker lifecycle facts, records CVE-2026-1386 and CVE-2026-5747, and expands future host acceptance criteria. This dated addendum supersedes no legal/tax/privacy findings in this source review.
