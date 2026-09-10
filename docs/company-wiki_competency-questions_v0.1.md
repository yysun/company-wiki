# company-wiki — Competency Questions

**Version:** 0.1  
**Status:** Draft evaluation catalog  
**Purpose:** Define the questions the `company-wiki` schema must help an LLM answer.

---

## 1. Why Competency Questions Exist

The schema should not be designed by attempting to model the entire company.

Instead, start with questions the AI must be able to answer.

Each competency question tests whether the schema contains enough:

- concepts;
- vocabulary;
- source routing;
- authority information;
- relationships;
- business definitions;
- problem-solving guidance.

Competency questions therefore serve as both **schema requirements** and **evaluation cases**.

---

## 2. Question Record Format

Recommended format:

```yaml
id: CQ-POLICY-001
question: What is the current travel reimbursement policy?
intent: authoritative_lookup
domain:
  - people
expected_problem_pattern: authoritative-lookup
required_evidence:
  - current approved policy
authority_expectation:
  - approved
  - canonical
notes: >
  The agent must not answer from an old archived policy when a newer approved
  version exists.
```

For initial use, plain Markdown tables or bullet entries are also acceptable.

---

# 3. A. Authoritative Lookup

## CQ-LOOKUP-001

**Question:** What is the current travel reimbursement policy?

Tests:

- policy vocabulary;
- canonical HR source;
- effective date;
- authority precedence.

Expected pattern: `authoritative-lookup`

---

## CQ-LOOKUP-002

**Question:** What is the official definition of an active customer?

Tests:

- business definitions;
- distinction between informal usage and canonical definition;
- source of truth.

Expected pattern: `authoritative-lookup`

---

## CQ-LOOKUP-003

**Question:** What is the current SLA for critical support incidents?

Tests:

- terminology;
- policy/service definition;
- current versus historical versions.

Expected pattern: `authoritative-lookup`

---

## CQ-LOOKUP-004

**Question:** Which document contains the approved launch criteria for Product X?

Tests:

- knowledge type `requirement` / `decision`;
- product domain;
- approved source routing.

Expected pattern: `authoritative-lookup`

---

## CQ-LOOKUP-005

**Question:** What does “GA” mean in our product documents?

Tests:

- acronym expansion;
- organization-specific vocabulary.

Expected pattern: `authoritative-lookup`

---

# 4. B. Ownership and Responsibility

## CQ-OWNER-001

**Question:** Who owns the customer cancellation process?

Tests:

- `owned_by`;
- process concept;
- organization/role source.

Expected pattern: `find-owner`

---

## CQ-OWNER-002

**Question:** Which team is responsible for maintaining the pricing rules?

Tests:

- concept-to-owner relationship;
- distinction between business owner and technical implementation owner.

Expected pattern: `find-owner`

---

## CQ-OWNER-003

**Question:** Who can approve an exception to the travel policy?

Tests:

- policy;
- approval authority;
- role relationships.

Expected pattern: `find-owner`

---

# 5. C. Version and Change Questions

## CQ-CHANGE-001

**Question:** What changed between the old and new pricing policy?

Tests:

- version discovery;
- `supersedes`;
- current versus historical sources;
- semantic comparison.

Expected pattern: `compare-versions`

---

## CQ-CHANGE-002

**Question:** When did the current cancellation policy take effect?

Tests:

- effective-date facet;
- current policy resolution.

Expected pattern: `compare-versions`

---

## CQ-CHANGE-003

**Question:** Which requirements were added in Product X v2?

Tests:

- version facet;
- requirements knowledge type;
- comparison across releases.

Expected pattern: `compare-versions`

---

## CQ-CHANGE-004

**Question:** Has the definition of active customer changed in the last two years?

Tests:

- business-definition history;
- authority;
- temporal comparison.

Expected pattern: `compare-versions`

---

# 6. D. Decision Discovery and Reconstruction

## CQ-DECISION-001

**Question:** What did we decide about mobile authentication?

Tests:

- decision discovery;
- product/technology cross-domain search;
- explicit decision artifact versus discussion.

Expected pattern: `reconstruct-decision`

---

## CQ-DECISION-002

**Question:** Why did we choose Vendor A instead of Vendor B?

Tests:

- decision rationale;
- related proposals/evaluations;
- supporting meeting notes.

Expected pattern: `reconstruct-decision`

---

## CQ-DECISION-003

**Question:** Who made the decision to postpone the launch, and when?

Tests:

- decision owner;
- decision date;
- authoritative versus informal evidence.

Expected pattern: `reconstruct-decision`

---

## CQ-DECISION-004

**Question:** Is the 2025 decision about data retention still valid?

Tests:

- superseding decisions;
- current authority;
- historical decision records.

Expected pattern: `reconstruct-decision`

---

# 7. E. Metric Explanation and Diagnosis

## CQ-METRIC-001

**Question:** Why did customer churn increase last quarter?

Tests:

- canonical churn definition;
- temporal comparison;
- segment decomposition;
- event/change search;
- causal caution.

Expected pattern: `explain-metric-change`

---

## CQ-METRIC-002

**Question:** Why did conversion fall after the website redesign?

Tests:

- metric definition;
- change timing;
- product change relationship;
- competing explanations.

Expected pattern: `explain-metric-change`

---

## CQ-METRIC-003

**Question:** Which customer segment contributed most to the decline in revenue?

Tests:

- metric decomposition;
- segmentation facet;
- quantitative evidence.

Expected pattern: `explain-metric-change`

---

## CQ-METRIC-004

**Question:** Did the pricing change actually improve retention?

Tests:

- before/after comparison;
- confounders;
- relationship between pricing and retention;
- appropriate uncertainty.

Expected pattern: `explain-metric-change`

---

## CQ-METRIC-005

**Question:** Why does the Finance dashboard show a different customer count from CRM?

Tests:

- metric/business definitions;
- source authority;
- reconciliation;
- timing and filtering differences.

Expected pattern: `explain-metric-change`

---

# 8. F. Dependency and Impact Analysis

## CQ-DEPEND-001

**Question:** Which systems depend on the customer identity service?

Tests:

- `depends_on`;
- system relationships;
- technical sources.

Expected pattern: `trace-dependency`

---

## CQ-DEPEND-002

**Question:** What would be affected if we retired Service X?

Tests:

- reverse dependency traversal;
- systems, processes, and products;
- incomplete-dependency handling.

Expected pattern: `trace-dependency`

---

## CQ-DEPEND-003

**Question:** Which teams and projects are affected by the new privacy policy?

Tests:

- policy relationships;
- organization/project mapping;
- cross-domain reasoning.

Expected pattern: `trace-dependency`

---

## CQ-DEPEND-004

**Question:** Which product features rely on Vendor A?

Tests:

- vendor-to-system-to-feature relationships;
- multi-hop navigation.

Expected pattern: `trace-dependency`

---

# 9. G. Incident Investigation

## CQ-INCIDENT-001

**Question:** What caused yesterday's payment outage?

Tests:

- incident source;
- logs/status reports;
- causal evidence;
- timeline reconstruction.

Expected pattern: `investigate-incident`

---

## CQ-INCIDENT-002

**Question:** Has this timeout problem happened before?

Tests:

- incident similarity;
- terminology expansion;
- historical search.

Expected pattern: `find-precedent`

---

## CQ-INCIDENT-003

**Question:** What did we do last time this integration failed?

Tests:

- historical incident resolution;
- precedent;
- procedure versus one-off workaround.

Expected pattern: `find-precedent`

---

## CQ-INCIDENT-004

**Question:** Which release introduced the regression?

Tests:

- release timeline;
- incident timing;
- source-code/release relationship.

Expected pattern: `investigate-incident`

---

# 10. H. Policy Application

## CQ-POLICY-001

**Question:** Can an employee expense a taxi home after working late?

Tests:

- current policy;
- rule interpretation;
- exceptions;
- uncertainty when scenario is not explicitly covered.

Expected pattern: `policy-application`

---

## CQ-POLICY-002

**Question:** Does this customer qualify for a refund under the current policy?

Tests:

- policy plus operational facts;
- source-of-truth customer state;
- rule application.

Expected pattern: `policy-application`

---

## CQ-POLICY-003

**Question:** Which approval is required for a purchase over $50,000?

Tests:

- threshold rule;
- owner/approver;
- current policy.

Expected pattern: `policy-application`

---

## CQ-POLICY-004

**Question:** Is this proposed data use allowed under our privacy rules?

Tests:

- policy interpretation;
- sensitive ambiguity;
- need to distinguish policy facts from legal advice.

Expected pattern: `policy-application`

---

# 11. I. Proposal Evaluation

## CQ-PROPOSAL-001

**Question:** Should we replace Vendor A with Vendor B?

Tests:

- objective;
- decision criteria;
- cost;
- risk;
- dependencies;
- historical experience.

Expected pattern: `evaluate-proposal`

---

## CQ-PROPOSAL-002

**Question:** What are the strongest arguments for and against moving this workload to the cloud?

Tests:

- balanced evidence;
- architecture constraints;
- operational history;
- cost/risk sources.

Expected pattern: `evaluate-proposal`

---

## CQ-PROPOSAL-003

**Question:** Does this proposal conflict with any existing architecture decisions?

Tests:

- proposal concepts;
- architecture decision records;
- constraints;
- superseding decisions.

Expected pattern: `evaluate-proposal`

---

## CQ-PROPOSAL-004

**Question:** What information is missing before we can make this decision?

Tests:

- evidence requirements;
- explicit gap detection;
- problem-pattern requirements.

Expected pattern: `evaluate-proposal`

---

# 12. J. Historical Reconstruction

## CQ-HISTORY-001

**Question:** How did the current onboarding process evolve?

Tests:

- historical documents;
- version sequence;
- decisions;
- policy/process changes.

Expected pattern: `compare-versions`

---

## CQ-HISTORY-002

**Question:** When did we first identify this risk?

Tests:

- historical search;
- meeting/issue records;
- earliest evidence versus later summaries.

Expected pattern: `find-precedent`

---

## CQ-HISTORY-003

**Question:** What were the original goals of Project X?

Tests:

- early project artifacts;
- distinction between initial and current goals.

Expected pattern: `reconstruct-decision`

---

# 13. K. Status and Situation Understanding

## CQ-STATUS-001

**Question:** What is the current status of Project X?

Tests:

- project sources;
- freshness;
- plan versus actual status;
- latest authoritative update.

Expected pattern: `summarize-status`

---

## CQ-STATUS-002

**Question:** What are the unresolved blockers for the launch?

Tests:

- issue/project artifacts;
- status;
- ownership;
- dependency relationships.

Expected pattern: `summarize-status`

---

## CQ-STATUS-003

**Question:** Which decisions are still pending?

Tests:

- decision status;
- meeting/action records;
- distinction between proposed and decided.

Expected pattern: `summarize-status`

---

## CQ-STATUS-004

**Question:** What changed since last week's project update?

Tests:

- time comparison;
- latest status sources;
- concise delta extraction.

Expected pattern: `summarize-status`

---

# 14. L. Risk Identification

## CQ-RISK-001

**Question:** What are the main risks to the launch?

Tests:

- risk records;
- blockers;
- dependencies;
- unresolved assumptions.

Expected pattern: `identify-risk`

---

## CQ-RISK-002

**Question:** Which known risks have no mitigation plan?

Tests:

- risk-to-mitigation relationship;
- completeness;
- status.

Expected pattern: `identify-risk`

---

## CQ-RISK-003

**Question:** Are there precedents suggesting this migration is risky?

Tests:

- incidents;
- historical projects;
- comparable cases.

Expected pattern: `find-precedent`

---

# 15. M. Cross-Source Reconciliation

## CQ-RECON-001

**Question:** The project plan says launch is October 1, but the meeting notes say October 15. Which date should I use?

Tests:

- authority;
- freshness;
- conflict handling;
- unresolved uncertainty.

Expected pattern: `authoritative-lookup`

---

## CQ-RECON-002

**Question:** Two documents define “active account” differently. Which definition is official?

Tests:

- canonical business definition;
- source authority;
- conflict resolution.

Expected pattern: `authoritative-lookup`

---

## CQ-RECON-003

**Question:** CRM says the customer is active, while the account spreadsheet says cancelled. What is the current status?

Tests:

- operational system of record;
- stale derived sources.

Expected pattern: `authoritative-lookup`

---

# 16. N. Vocabulary and Semantic Navigation

## CQ-VOCAB-001

**Question:** Search for everything related to customer attrition, even if documents use the term churn.

Tests:

- aliases;
- query expansion;
- concept normalization.

Expected pattern: `authoritative-lookup`

---

## CQ-VOCAB-002

**Question:** Are “Project Falcon” and “NextGen CRM” the same initiative?

Tests:

- aliases/nicknames;
- concept identity;
- historical naming.

Expected pattern: `authoritative-lookup`

---

## CQ-VOCAB-003

**Question:** What does “P0” mean here?

Tests:

- overloaded terminology;
- domain-specific meaning;
- context-sensitive resolution.

Expected pattern: `authoritative-lookup`

---

# 17. O. Unknown and Missing Knowledge

## CQ-GAP-001

**Question:** Do we have an official policy for AI-generated customer communications?

Tests:

- ability to determine absence;
- distinction between no result and no policy;
- related policy discovery.

Expected pattern: `authoritative-lookup`

---

## CQ-GAP-002

**Question:** What don't we know yet about the cause of the churn increase?

Tests:

- evidence-gap detection;
- hypotheses versus facts;
- investigation completeness.

Expected pattern: `explain-metric-change`

---

## CQ-GAP-003

**Question:** Which important dependencies of Service X are undocumented?

Tests:

- compare known relationship sources;
- detect gaps without claiming completeness.

Expected pattern: `trace-dependency`

---

# 18. Evaluation Dimensions

Each competency question should eventually be scored across:

| Dimension | Question |
|---|---|
| Intent | Did the agent understand what kind of problem this was? |
| Vocabulary | Did it resolve aliases and company terminology? |
| Routing | Did it choose the right source(s)? |
| Authority | Did it prefer authoritative evidence? |
| Retrieval | Did it retrieve sufficient evidence? |
| Iteration | Did it search again when the first retrieval was insufficient? |
| Reasoning | Did it apply an appropriate investigation pattern? |
| Conflict | Did it identify contradictory evidence? |
| Uncertainty | Did it avoid overstating unsupported conclusions? |
| Answer | Was the final answer correct and useful? |

---

# 19. Suggested Benchmark Method

For each question, compare:

```text
A. LLM + raw source search
B. LLM + company-wiki schema + identical source access
```

Measure:

- correct-source rate;
- authoritative-source rate;
- answer correctness;
- number of search attempts;
- unresolved contradiction rate;
- hallucination rate;
- total context consumed.

This directly measures the value of the schema.

---

# 20. MVP Question Set

For a first implementation, select approximately 25 questions:

```text
5 authoritative lookup
3 ownership
3 decision reconstruction
4 metric diagnosis
3 dependency analysis
2 policy application
2 status
2 reconciliation
1 unknown-knowledge
```

Choose real company questions whenever possible.

A smaller set of realistic questions is more valuable than a large synthetic benchmark.

---

# 21. Schema-Growth Rule

A new schema element should normally exist because at least one competency question needs it.

For example:

```text
Question repeatedly misses "employee attrition"
  ↓
add alias relationship to "turnover"

Question retrieves old policy
  ↓
add authority rule / effective-date guidance

Question cannot find decision rationale
  ↓
add source route to decision records and meeting notes

Question needs multi-step diagnosis
  ↓
add or improve problem pattern
```

This keeps the schema grounded in actual problem-solving value.
