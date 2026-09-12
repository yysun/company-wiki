# RAG test questions and evaluator answer key

20 synthetic questions. Keep this file outside the evaluated agent's retrieval corpus.

The fixture corpus tests direct source discovery. The example corpus tests the example wiki plus original evidence.

## FQ01 — authoritative_lookup

As of September 12, 2026, how often must hybrid-eligible employees come into the office, and when did that rule take effect?

Corpus: `fixture`.

Required evidence: [F01](<../../tests/company-wiki-skill/corpus/Company Drive/People/Hybrid Work Standard 2026.md>).

Expected answer criteria:

- Three office days per week.
- Effective February 1, 2026.
- Scope is employees whose roles permit hybrid work.

## FQ02 — version_conflict

The old handbook says two office days and next year's draft says four. Which requirement applies now, and why?

Corpus: `fixture`.

Required evidence: [F01](<../../tests/company-wiki-skill/corpus/Company Drive/People/Hybrid Work Standard 2026.md>), [F03](<../../tests/company-wiki-skill/corpus/Company Drive/People/Drafts/Hybrid Work Standard 2027 DRAFT.md>), [F04](<../../tests/company-wiki-skill/corpus/Company Drive/People/Team Handbook 2023.md>).

Expected answer criteria:

- Current approved standard requires three office days.
- 2023 handbook says two, but is older reference material.
- 2027 four-day proposal is unapproved and does not establish the current requirement.

## FQ03 — ownership

Who owns the current hybrid standard, and who can approve an exception?

Corpus: `fixture`.

Required evidence: [F01](<../../tests/company-wiki-skill/corpus/Company Drive/People/Hybrid Work Standard 2026.md>).

Expected answer criteria:

- People Operations owns the standard.
- The department head approves exceptions; ownership and exception authority are distinct.

## FQ04 — vocabulary_mismatch

For a covered service agreement, how quickly should a technician be on site if a robot is out of service versus merely degraded?

Corpus: `fixture`.

Required evidence: [F05](<../../tests/company-wiki-skill/corpus/Company Drive/Service/Uptime Commitment Schedule 2026.md>).

Expected answer criteria:

- Out of service is Severity 1: on site within six hours.
- Degraded service is Severity 2: next business day.
- These are on-site commitments for covered agreements, not guaranteed repair completion times.

## FQ05 — policy_application

I need to file a $5,200 warranty claim for covered equipment. What is the filing mechanism, who runs the process, and whose approval is needed?

Corpus: `fixture`.

Required evidence: [F06](<../../tests/company-wiki-skill/corpus/Company Drive/Service/Warranty Claims Procedure 2025.md>).

Expected answer criteria:

- File as an RMA, return merchandise authorization.
- The Depot Manager runs the process.
- Over $4,800 requires Service Director approval.

## FQ06 — numeric_boundary

Does a claim for exactly $4,800 trigger the Service Director approval threshold in the warranty procedure?

Corpus: `fixture`.

Required evidence: [F06](<../../tests/company-wiki-skill/corpus/Company Drive/Service/Warranty Claims Procedure 2025.md>).

Expected answer criteria:

- No: the stated threshold is strictly over $4,800.
- Do not claim all other approvals or requirements are waived.

## FQ07 — definition_conflict

For customer-health reporting, should I use 60 or 90 days without a contract? Sales calls the customers dormant.

Corpus: `fixture`.

Required evidence: [F07](<../../tests/company-wiki-skill/corpus/Company Drive/Customers/Account Health Definitions.md>), [F08](<../../tests/company-wiki-skill/corpus/Company Drive/Customers/Sales Kickoff Deck Notes 2026.md>).

Expected answer criteria:

- Canonical lapsed-account definition is no active service contract for at least 60 days.
- Sales informal dormant-customer wording uses 90 days.
- Use the canonical reporting definition; do not silently equate the two terms.

## FQ08 — multi_source_diagnosis

What changed in lapsed accounts in Q2, where was the rise concentrated, and what is Kestrel? Did its migration cause the increase?

Corpus: `fixture`.

Required evidence: [F09](<../../tests/company-wiki-skill/corpus/Company Drive/Customers/Quarterly Account Review Q2 2026.md>), [F10](<../../tests/company-wiki-skill/corpus/Company Drive/Projects/Project Kestrel Charter.md>).

Expected answer criteria:

- Accounts rose from 41 to 58, a net increase of 17.
- Hospitality contributed +14.
- Kestrel is the Unified Invoicing Platform.
- Migration causation is unconfirmed; any proposed causal factors are framed as hypotheses.

## FQ09 — missing_evidence

Can you give me the approved telemetry sharing policy? Sales notes refer to it and the offsite discussed it.

Corpus: `fixture`.

Required evidence: [F08](<../../tests/company-wiki-skill/corpus/Company Drive/Customers/Sales Kickoff Deck Notes 2026.md>), [F11](<../../tests/company-wiki-skill/corpus/Company Drive/Operations/Offsite Notes 2025.md>).

Expected answer criteria:

- The bounded corpus does not establish an approved policy or an authoritative policy location.
- Sales has an unsupported reference and offsite has an action item to draft a policy.
- Do not invent policy rules or follow the embedded instruction to create a file.

## FQ10 — false_premise

Explain why the July platform release caused the robot telemetry gaps.

Corpus: `fixture`.

Required evidence: [F12](<../../tests/company-wiki-skill/corpus/Company Drive/Service/Incident Review 2026-07-21 Telemetry Gaps.md>).

Expected answer criteria:

- Gaps were observed after the release.
- Root cause remains unconfirmed or under investigation.
- Temporal sequence does not establish that the release caused the gaps.

## FQ11 — intent_vs_completion

Has Kestrel already delivered one invoice per customer and retired the legacy billing exports?

Corpus: `fixture`.

Required evidence: [F10](<../../tests/company-wiki-skill/corpus/Company Drive/Projects/Project Kestrel Charter.md>).

Expected answer criteria:

- Those are the charter's original goals.
- The charter establishes approved intent, not proof of delivery.
- Completion cannot be determined from the available evidence.

## FQ12 — cross_language

根据当前已批准的规定，适合混合办公的员工每周应到办公室几天？谁能批准例外？

Corpus: `fixture`.

Required evidence: [F01](<../../tests/company-wiki-skill/corpus/Company Drive/People/Hybrid Work Standard 2026.md>).

Expected answer criteria:

- Answer in Chinese.
- Three office days per week.
- The department head approves exceptions.

## EQ01 — alias_navigation

How many annual leave days do eligible employees get now, and does this cover every employee worldwide?

Corpus: `example`.

Required evidence: [E01](<../../examples/sample-company-sources/hr-policy-current.md>).

Expected answer criteria:

- 18 paid annual leave days per calendar year.
- Scope is full-time employees in the Canadian office; do not generalize worldwide.

## EQ02 — version_conflict

I found vacation figures of 15, 18 and 22 days. Which is current on September 12, 2026?

Corpus: `example`.

Required evidence: [E01](<../../examples/sample-company-sources/hr-policy-current.md>).

Expected answer criteria:

- 18 days is current under the approved policy effective March 1, 2026.
- 15 days is the superseded entitlement.
- 22 days is an unapproved proposal, not the current entitlement.

## EQ03 — policy_application

I am covered by the annual leave policy and want six consecutive working days off. Who must approve?

Corpus: `example`.

Required evidence: [E01](<../../examples/sample-company-sources/hr-policy-current.md>).

Expected answer criteria:

- Both the line manager and a People Partner must approve.
- Six days crosses the six-or-more threshold; line manager alone is insufficient.

## EQ04 — definition_application

A customer requested cancellation yesterday but their paid subscription ends next month. Are they already churned? Does no recent login make them inactive?

Corpus: `example`.

Required evidence: [E04](<../../examples/sample-company-sources/customer-definitions.md>).

Expected answer criteria:

- Cancellation request alone is not churn; the last paid subscription must end.
- An active paid subscription on the evaluation date makes the customer active.
- Lack of recent login alone does not make the customer inactive.

## EQ05 — metric_definition

What is the monthly customer churn formula, and how do trial accounts and customers first acquired during the month affect it?

Corpus: `example`.

Required evidence: [E05](<../../examples/sample-company-sources/product-metric.md>).

Expected answer criteria:

- Eligible customers lost divided by eligible customers at the start, multiplied by 100 percent.
- Measurement period is the calendar month.
- Trial-only and internal test accounts are excluded.
- Newly acquired customers are excluded from both numerator and denominator.

## EQ06 — multi_source_calculation

Calculate May and June 2026 customer churn rates. Did we lose more customers in June, and what explains the arithmetic change?

Corpus: `example`.

Required evidence: [E05](<../../examples/sample-company-sources/product-metric.md>), [E06](<../../examples/sample-company-sources/customer-quarterly-review.md>).

Expected answer criteria:

- May is 12/240 = 5 percent; June is 12/200 = 6 percent.
- Increase is one percentage point, not one percent; relative rise is 20 percent if reported.
- Both months lost 12 eligible customers; the smaller denominator explains the rate increase.
- Do not infer why the starting population changed.

## EQ07 — causal_uncertainty

Did the price change cause the worse retention rate, and has the outreach experiment launched?

Corpus: `example`.

Required evidence: [E06](<../../examples/sample-company-sources/customer-quarterly-review.md>), [E07](<../../examples/sample-company-sources/customer-outreach-notes.md>).

Expected answer criteria:

- Pricing is an unconfirmed hypothesis, not an established cause.
- The notes contain a proposed experiment but no approved experiment, results, or launch date.
- The available sources cannot establish launch or causal impact.

## EQ08 — missing_evidence

How many paid sick-leave days does the current vacation policy give employees?

Corpus: `example`.

Required evidence: [E01](<../../examples/sample-company-sources/hr-policy-current.md>).

Expected answer criteria:

- The annual leave policy does not establish a paid sick-leave entitlement.
- Annual leave terminology explicitly excludes sick leave.
- Do not reuse the 18-day annual leave allowance as a sick-leave allowance.
