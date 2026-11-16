# 038 — Tardis market-data rights and usage boundary

**Date:** 16 November 2026  
**Phase:** 01 — Open-source and infrastructure research  
**Phase state:** IN PROGRESS; Phase 02 remains LOCKED

## Official terms reviewed

Tardis' published Terms of Service, section 9, describe permitted customer uses including storing Data and Manipulated Data on the Customer System and distributing Derived Data to Customer Users on that system. Section 9.2 restricts using the Services (wholly or partly) in products or services and prohibits redistributing or reselling the Data or Services, except aggregated/calculated data at a lowest resolution of 10 minutes. The terms also state that intellectual property in Data and Materials belongs to Tardis or its licensors and that customers have no rights beyond the express licence.

Official source:
- https://docs.tardis.dev/legal/terms-of-service

The public CSV documentation separately says first-of-month historical sample files are downloadable without an API key:
- https://docs.tardis.dev/downloadable-csv-files

The subscription documentation distinguishes Solo, Academic, Professional and Business plans and their data access/rights:
- https://docs.tardis.dev/faq/billing-and-subscriptions

## IDEAL usage facts

- IDEAL used only three public first-of-month OKX Swap CSV samples (1 Sep, 1 Oct, 1 Nov 2026) without an API key.
- The samples were used for internal historical BBO validation and source-quality research.
- Raw archives and reconstructed BBO rows were deleted by workflow cleanup.
- Only small summary artifacts and derived comparison metrics were retained.
- No raw data is committed to the repository or redistributed.
- No external users, customers or product service receive Tardis data.

## Restriction and disposition

1. Retain Tardis as a **secondary internal research/reference source only** under the currently reviewed public/standard terms.
2. Do not redistribute or resell raw Tardis data, normalized event streams, or sub-10-minute derived market data.
3. Do not embed Tardis data or Tardis services into a commercial or externally offered IDEAL product/service without an appropriate separate written licence.
4. Do not treat the 10-minute aggregation exception as permission for every use case; the exact customer agreement, data type, exchange/licensor restrictions and downstream display remain controlling.
5. If IDEAL later becomes a multi-user or commercial product, re-open data rights with Tardis and obtain product-specific written confirmation before any external data display or distribution.
6. Keep raw historical market data out of the public repository; retain only permitted audit summaries and non-reconstructive aggregate findings.

## Uncertainty

The public sample download page confirms that the first day of each month is available without an API key, but it does not by itself provide a separate bespoke redistribution licence for those sample files. This checkpoint therefore applies the conservative published Terms of Service boundary. It is not a legal opinion about the exact enforceability or application of those terms to the free samples.

No Tardis subscription, API key, paid data or external redistribution is authorised.
