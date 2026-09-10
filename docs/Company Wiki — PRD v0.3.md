# Company Wiki

**Product Requirements Document**  
**Version:** 0.3  
**Status:** Implementation Draft  
**Skill Name:** `company-wiki`  
**Product Name:** Company Wiki / 企业 Wiki  
**Product Type:** Portable Agent Skill  
**Target:** AI agents and coding agents

---

## 1. Product Summary

**Company Wiki** is an agent skill that builds and maintains a progressively disclosed, evidence-backed wiki over an organization's existing document systems.

It works with document systems such as:

- Google Drive
- Microsoft SharePoint / OneDrive
- WeCom Drive / 企业微盘
- Dropbox
- local or network document repositories
- other document systems accessible to the agent

Company Wiki does **not** own or ingest source documents.

The existing document system remains the **system of record**.

Company Wiki uses existing document skills, MCP tools, CLIs, connectors, or filesystem capabilities provided by the agent host to access source documents.

It creates a lightweight, LLM-readable wiki over them:

```text
Existing Document Systems
          │
          │ existing skills/tools
          ▼
        Agent
          │
     company-wiki
          │
          ▼
      Company Wiki
          │
   progressive disclosure
          ▼
    Original Documents
```

The initial implementation should determine how far this architecture can go using:

> **LLM reasoning + existing document access + LLM-readable wiki documents**

before introducing custom software infrastructure.

---

## 2. Core Hypothesis

A useful company knowledge layer for hundreds or low thousands of documents may not require a traditional RAG stack.

Modern LLM agents can already:

- search
- read
- summarize
- classify
- compare
- synthesize
- navigate
- reason across documents

Existing document systems already provide:

- storage
- permissions
- editing
- folders
- synchronization
- versioning
- search
- sharing

Agent hosts increasingly provide access through:

- document skills
- MCP
- CLI
- connectors
- filesystem tools
- native integrations

Therefore Company Wiki should first test:

> **Can an agent skill construct, navigate, and maintain a useful organizational wiki directly over existing documents?**

---

## 3. Product Principle

> **Use documents as infrastructure before building knowledge infrastructure.**

Do not introduce by default:

- databases
- vector databases
- custom indexes
- ingestion pipelines
- source adapter frameworks
- background services
- custom search infrastructure

Additional infrastructure should be introduced only when a demonstrated requirement cannot reasonably be satisfied by the document-native, LLM-first architecture.

---

## 4. What Company Wiki Is

Company Wiki is primarily **knowledge-management behavior encoded as an agent skill**.

The skill teaches the agent:

- how to inspect an existing document repository
- how to discover important organizational topics
- how to organize those topics
- how to create useful wiki structures
- how to navigate knowledge progressively
- how to search intelligently
- how to identify likely authoritative sources
- how to synthesize multiple documents
- how to expose contradictions and uncertainty
- how to maintain the wiki as source documents evolve
- when to return to original evidence

The intelligence belongs primarily in:

> **LLM + skill**

rather than custom application code.

A valid V1 may contain **no executable Company Wiki code at all**.

---

## 5. Product Boundary

Company Wiki is deliberately **document-derived**.

It answers:

> **What does the company know through its existing documents, and how can that knowledge be made easier to navigate and use?**

It does not attempt to represent all organizational knowledge.

Conceptually:

```text
Existing Company Documents
          ↓
      Company Wiki
          ↓
document-derived knowledge view
          ↓
other agents / applications /
broader knowledge systems
```

Company Wiki must not implicitly evolve into:

- a general Knowledge Space
- an AI Workspace
- an operational business interface
- a business database
- a workflow engine
- an enterprise ontology
- a universal knowledge graph

Those systems may consume Company Wiki later.

---

## 6. Source of Truth

Original company documents remain authoritative.

Examples include:

- Google Docs
- Word documents
- PDFs
- SharePoint pages
- WeCom documents
- spreadsheets
- presentations
- other cloud documents

Company Wiki must not require:

- modifying source documents
- adding AI metadata to source documents
- creating one metadata sidecar per source
- converting source documents to Markdown
- copying the source corpus into another repository

The wiki is a **derived knowledge projection**, not a replacement corpus.

---

## 7. Existing Document Access

Company Wiki should use document-access capabilities already available to the agent.

Examples:

```text
Google Drive skill
SharePoint skill
WeCom skill
MCP document tools
CLI tools
filesystem tools
host connectors
native agent integrations
```

Architecture:

```text
                  Agent Host
                      │
        ┌─────────────┼─────────────┐
        │             │             │
  company-wiki   Drive skill   WeCom skill
        │        MCP / CLI / FS     │
        │             │             │
        └─────────────┼─────────────┘
                      ▼
               Document System
```

Company Wiki should **compose with existing skills and tools** rather than rebuilding document access.

---

## 8. No Mandatory Source Adapter

Company Wiki does not require a custom source-adapter framework in V1.

If the host can already:

- list documents
- search documents
- read documents
- inspect available metadata
- follow document links

Company Wiki should use those capabilities directly.

Provider-specific adapters may be introduced later only if actual portability problems demonstrate a need.

---

## 9. The Wiki Overlay

Company Wiki creates or uses a dedicated wiki area in an existing document system.

Conceptually:

```text
Company Drive/
├── HR/
├── Finance/
├── Operations/
├── Projects/
│
└── Company Wiki/
    ├── INDEX
    ├── HR
    ├── Finance
    ├── Operations
    └── ...
```

The representation depends on the underlying platform.

Wiki content may be:

- Google Docs
- SharePoint pages
- WeCom documents
- Markdown files
- other LLM-readable cloud documents

The wiki must remain understandable by both humans and LLM agents.

---

## 10. No Database by Default

Company Wiki V1 should not require a database.

The wiki documents themselves should first be tested as the durable knowledge overlay.

Prefer:

```text
Source Documents
       ↓
      LLM
       ↓
Company Wiki Documents
```

over:

```text
Source Documents
       ↓
ingestion/index/database
       ↓
knowledge application
```

Wiki documents may provide sufficient durable representation for:

- navigation
- topic organization
- distilled knowledge
- lightweight metadata
- source references
- relationships
- maintenance state
- agent memory

If this proves insufficient, infrastructure may be added later.

---

## 11. Progressive Disclosure

**Progressive disclosure is a fundamental architectural requirement.**

Company Wiki should behave like a well-designed agent skill.

A skill typically follows:

```text
SKILL.md
    ↓
relevant reference/workflow
    ↓
detailed instructions
```

Company Wiki should follow:

```text
Company Wiki INDEX
        ↓
domain guide
        ↓
topic page
        ↓
original source evidence
```

The agent should load only as much knowledge as necessary for the current task.

---

## 12. Knowledge Levels

Company Wiki defines four conceptual levels.

### Level 0 — Wiki Index

A compact map of major organizational knowledge areas.

```markdown
# Company Wiki

## HR

Employee policies, benefits, hiring, leave and workplace procedures.

→ HR

## Finance

Expenses, purchasing, budgeting and financial procedures.

→ Finance

## Operations

Operational procedures and internal processes.

→ Operations

## Sales

Pricing, sales process, customers and commercial policies.

→ Sales
```

The index must remain compact.

It is a map, not an encyclopedia.

### Level 1 — Domain / Major Topic Guide

```markdown
# HR

## Leave

Vacation, sick leave and other employee absence policies.

→ Leave

## Benefits

Employee health, dental and other benefits.

→ Benefits

## Hiring

Recruitment, offers and onboarding.

→ Hiring

## Workplace Policies

General employee rules and expectations.

→ Workplace Policies
```

This level primarily routes the agent toward relevant knowledge.

### Level 2 — Topic Page

```markdown
# Travel Reimbursement

Use this topic for employee business travel expenses,
transportation, mileage and accommodation.

## Key Knowledge

- Business travel normally requires approval.
- Mileage reimbursement is governed by the current travel policy.
- Expense claims follow the expense submission procedure.

## Explore

- Travel Approval
- Mileage
- Accommodation
- Expense Submission

## Primary Sources

- Travel Policy 2026
- Expense Procedure 2026

## Related Topics

- Purchasing
- Employee Expenses
```

A topic page contains useful distilled knowledge but should not unnecessarily reproduce source documents.

### Level 3 — Original Sources

When precise evidence or additional detail is required, the agent follows references to original documents.

Examples:

```text
Travel Policy 2026
Expense Procedure 2026
Employee Handbook
Finance Approval Policy
```

Original documents remain authoritative.

---

## 13. Progressive Retrieval

Default retrieval flow:

```text
User Question
      ↓
Wiki Index
      ↓
Relevant Domain
      ↓
Relevant Topic
      ↓
Is available knowledge sufficient?
      │
   ┌──┴──┐
  yes    no
   │      │
answer   search/read
         source docs
             ↓
           answer
```

Do not load the complete wiki or source repository into context.

---

## 14. Navigation and Search Are Complementary

Progressive navigation does not replace search.

The agent may use:

```text
wiki navigation
+
repository search
+
direct source reading
```

depending on the task.

Broad questions often benefit from wiki navigation.

Precise lookup questions may benefit from direct repository search.

Example:

> What are our employee leave policies?

Prefer wiki navigation first.

Example:

> Find the document mentioning a $2,500 approval threshold.

Prefer repository search.

The skill should choose the most efficient strategy.

---

## 15. Wiki as Projection

The wiki is a **knowledge projection over source documents**.

It is not another source repository.

```text
Source Documents
       ↓
LLM interpretation
       ↓
   Company Wiki
       ↓
human + agent navigation
```

Its purpose is to make organizational information easier to:

- understand
- navigate
- connect
- retrieve
- verify
- maintain

---

## 16. Materialization Strategy

Not every discovered fact or topic requires a permanent wiki page.

Use three levels.

### Always Materialize

Persist compact structural knowledge:

- Wiki Index
- major domains
- major topic maps

### Materialize When Useful

Persist stable and repeatedly useful topics such as:

- Vacation
- Travel Reimbursement
- Customer Refunds
- Purchasing
- Employee Onboarding

### Generate on Demand

Highly specific or rarely requested knowledge should normally be synthesized directly from source documents without creating a permanent page.

Example:

> What hotel expenses are allowed if an employee extends a business trip for two personal days?

The answer may be generated directly from evidence.

---

## 17. Organic Wiki Growth

Do not generate one wiki page per source document.

Wiki structure should emerge from **knowledge topics and usefulness**, not source-file count.

For example:

```text
700 source documents
```

does not imply:

```text
700 wiki pages
```

A useful structure might instead contain:

```text
6 major domains
35 topic guides
70 useful topic pages
```

There is no target ratio.

The structure should fit the organization.

---

## 18. Topic Discovery

During initial build, the agent should inspect enough of the repository to discover meaningful organizational topics.

Useful signals include:

- folder structure
- document titles
- document contents
- repeated terminology
- policies
- business processes
- organizational functions
- document relationships
- existing indexes
- search results
- document ownership
- document recency

Folder structure is evidence, not ontology.

Do not blindly reproduce the source-drive hierarchy.

---

## 19. Authority

Company Wiki must distinguish:

> **relevance**

from:

> **authority**

Possible source states include:

```text
authoritative
current
draft
historical
superseded
informational
unknown
```

The LLM may infer likely authority from:

- title
- date
- version
- owner
- explicit wording
- document relationships
- references from other authoritative sources

But inferred authority remains inference.

Do not silently convert uncertain inference into organizational policy.

---

## 20. Conflict Detection

When meaningful sources disagree, expose the disagreement.

Example:

```markdown
## Conflict

Travel Policy 2026 states:

$0.61/km

Employee Handbook states:

$0.55/km

The Travel Policy is newer and appears to supersede the
handbook, but this precedence has not been explicitly verified.
```

Do not silently resolve contradictions merely to produce a clean answer.

---

## 21. Freshness

Use information already available through the document system where possible.

Potential signals include:

- modification date
- document version
- effective date stated in content
- newer related documents
- explicit supersession
- review date

Avoid building dedicated freshness infrastructure in V1.

---

## 22. Evidence and Source Links

Important organizational claims should remain traceable to original documents.

Topic pages should link to source evidence where useful:

```markdown
## Primary Sources

- [Travel Policy 2026](source-link)
- [Expense Procedure](source-link)
```

Where supported, links should open the original cloud documents.

The wiki should make evidence easier to reach, not hide it.

---

## 23. Ask Workflow

When answering a question:

1. Understand the user's information need.
2. Consult the minimum useful wiki level.
3. Determine whether existing wiki knowledge is sufficient.
4. Search or read original documents when necessary.
5. Prefer current and authoritative evidence.
6. Identify meaningful conflicts and uncertainty.
7. Answer directly.
8. Reference original evidence when appropriate.
9. Do not create permanent wiki content unless it is likely to be useful again.

---

## 24. Browse Workflow

When exploring a subject:

1. Locate the nearest relevant wiki domain or topic.
2. Present the appropriate knowledge guide.
3. Expose useful subtopics.
4. Show meaningful related topics.
5. Identify important source documents.
6. Allow progressive navigation toward detail and evidence.

Browse should expose the structure of organizational knowledge rather than merely returning search results.

---

## 25. Build Workflow

Initial wiki construction is primarily an LLM task.

```text
Inspect repository
      ↓
understand existing structure
      ↓
sample/search representative documents
      ↓
identify major domains
      ↓
discover important topics
      ↓
create compact INDEX
      ↓
create domain/topic guides
      ↓
identify primary sources
      ↓
link original documents
      ↓
stop before unnecessary detail
```

Do not exhaustively summarize every source document.

The objective is useful knowledge navigation, not precomputing every possible answer.

---

## 26. Refresh Workflow

Refresh should be incremental and reasoning-driven.

Example:

```text
New HR policy
      ↓
inspect it
      ↓
identify affected wiki topics
      ↓
update only relevant pages
```

Another example:

```text
Travel Policy updated
      ↓
inspect changes
      ↓
update Travel Reimbursement
      ↓
check related Expense topics
```

Avoid rebuilding the complete wiki unnecessarily.

---

## 27. Audit Workflow

Company Wiki should inspect both the document corpus and the wiki for knowledge-quality problems.

Look for:

- conflicting guidance
- apparently superseded documents
- stale information
- duplicate policies
- missing authoritative sources
- orphaned topics
- broken references
- poor wiki organization
- important source areas absent from the wiki
- wiki pages no longer supported by current sources

Audit results are recommendations.

Do not modify original source documents without explicit authorization.

---

## 28. Knowledge Gap Discovery

Company Wiki may identify likely missing knowledge.

Example:

```text
Customer refunds are referenced in:

- Customer Service Guide
- Sales Handbook

but no authoritative refund policy was found.
```

Report this as:

> **Possible knowledge gap**

Do not claim that information does not exist merely because it was not found.

---

## 29. Human Readability

Company Wiki documents must remain useful to humans.

Prefer:

```markdown
# Purchasing

## Approval

...

## Vendors

...

## Related Topics

...
```

Avoid exposing unnecessary machine state or large metadata structures.

---

## 30. LLM Readability

Wiki documents must simultaneously be optimized for agent consumption.

Prefer:

- clear headings
- concise descriptions
- stable terminology
- explicit source references
- meaningful links
- compact pages
- predictable structure
- progressive detail

Avoid:

- giant generated summaries
- repeated source content
- excessive prose
- duplication across topic pages
- unrelated material in the same page

---

## 31. Relationships

V1 should express most relationships naturally through wiki links.

Example:

```markdown
## Related Topics

- Travel Approval
- Employee Expenses
- Purchasing

## Primary Sources

- Travel Policy 2026
- Expense Procedure
```

A graph database or formal relationship schema is not required.

Introduce structured relationships only if normal document links prove insufficient.

---

## 32. Metadata

Do not modify source documents to add Company Wiki metadata.

Do not create one metadata file per source.

Where useful, lightweight metadata may appear in wiki pages:

```markdown
Status: Current
Primary source: Travel Policy 2026
Last reviewed: 2026-09-10
```

Metadata should remain useful to humans as well as LLMs.

Avoid machine-oriented metadata unless a demonstrated need exists.

---

## 33. Permissions

The underlying document system remains responsible for source-document permissions.

Company Wiki should use permission-aware document capabilities when available.

The skill must not intentionally expose information the current user cannot access.

Persisted wiki content creates an additional risk:

> A generated summary can leak information from a restricted source even when the original source remains protected.

Therefore:

- do not persist restricted information into a more broadly accessible wiki page
- where source ACLs differ materially, prefer runtime synthesis
- generated wiki content should inherit appropriate access restrictions where the document platform supports them

Company Wiki does not implement a replacement ACL system.

---

## 34. Wiki Authoring Principles

Every Company Wiki document should answer one of three questions:

1. **Where should I go next?**
2. **What should I know about this topic?**
3. **Where is the evidence?**

If a section does none of these, it probably should not be there.

Wiki pages should favor:

> concise knowledge + navigation + evidence

over comprehensive reproduction of source documents.

---

## 35. Progressive Disclosure Rules

The wiki should follow these rules:

### Keep higher levels small

Indexes and domain pages should contain just enough information to choose the next relevant path.

### Push detail downward

Specific rules, exceptions, procedures, and evidence belong deeper in the structure.

### Do not duplicate

Knowledge should have a natural home and be linked from other topics rather than copied repeatedly.

### Follow sources only when necessary

If a topic page sufficiently answers the question, do not automatically read every source document.

### Preserve escape routes

Every generated knowledge page should make it easy to reach original evidence when needed.

---

## 36. Skill Structure

The skill itself must follow the same progressive-disclosure principle as the wiki.

Suggested structure:

```text
company-wiki/
├── SKILL.md
└── references/
    ├── build.md
    ├── ask.md
    ├── browse.md
    ├── refresh.md
    ├── audit.md
    └── authoring.md
```

`SKILL.md` should remain compact.

Detailed instructions should be loaded only for the active workflow.

---

## 37. SKILL.md Responsibilities

`SKILL.md` should establish only the durable core behavior:

1. Existing documents remain the source of truth.
2. Use existing document skills and tools.
3. Prefer document-native capabilities over custom infrastructure.
4. Navigate Company Wiki progressively.
5. Load the minimum knowledge necessary.
6. Search original repositories when wiki navigation is insufficient.
7. Prefer current and authoritative evidence.
8. Preserve links to evidence.
9. Expose conflicts and uncertainty.
10. Do not invent organizational facts.
11. Update wiki content when repeated use makes materialization worthwhile.
12. Avoid unnecessary code, databases, indexes, or infrastructure.

Detailed workflow logic belongs in reference files.

---

## 38. Initial Implementation

V0.3 should deliberately test the smallest possible implementation:

```text
company-wiki/
├── SKILL.md
└── references/*.md

+

existing document skill

+

existing cloud document system
```

There should initially be:

```text
no database
no vector store
no custom retrieval service
no adapter framework
no daemon
no separate backend
```

A coding agent should **not create these proactively**.

---

## 39. Reference Pilot

The initial pilot should use approximately:

```text
100–500 real organizational documents
```

stored in an existing cloud document system.

The pilot should create:

- one Company Wiki root
- one compact index
- a small number of domain guides
- useful topic pages
- source links
- enough structure to support representative questions

The goal is to learn whether the LLM-first approach works, not to build infrastructure.

---

## 40. Pilot Questions

Create a representative test set containing questions such as:

### Direct fact

> What is the mileage reimbursement rate?

### Policy

> Can employees expense airport taxis?

### Procedure

> How do I request reimbursement?

### Discovery

> What documentation do we have about onboarding new customers?

### Cross-document synthesis

> Summarize our employee travel rules.

### Authority

> Which travel policy is currently in force?

### Conflict

> Do any documents disagree about mileage reimbursement?

### Navigation

> Show me what we know about purchasing.

### Gap detection

> Do we have a clear policy for customer refunds?

---

## 41. Evaluation

Evaluate Company Wiki against four primary dimensions.

### Answer Quality

Can the agent produce correct and useful answers?

### Navigation Quality

Can the agent reach relevant information without indiscriminately searching the entire corpus?

### Evidence Quality

Can important claims be traced back to source documents?

### Maintenance Quality

Can the wiki remain useful as source documents change?

Secondary measures:

- number of source documents read per task
- context consumption
- time/tool calls required
- unnecessary wiki duplication
- false conflict detection
- missed authoritative sources
- user corrections required

---

## 42. Success Criteria

V0.3 is successful if:

1. A useful wiki can be built from real company documents using primarily LLM reasoning.
2. Existing document skills provide sufficient source access.
3. Users and agents can navigate the wiki progressively.
4. Common questions can be answered with traceable evidence.
5. The wiki substantially reduces repeated broad repository search.
6. The wiki can be refreshed without a complete rebuild.
7. Source documents remain untouched.
8. No separate database is required for normal operation.
9. No custom ingestion or RAG service is required for normal operation.
10. The wiki remains understandable and editable as normal documents.

---

## 43. Failure Signals

Only consider additional infrastructure when evidence reveals specific failures.

Examples:

### Search failure

Native document search cannot reliably retrieve relevant sources.

Possible later response:

- lightweight full-text index
- semantic retrieval

### Scale failure

Progressive document navigation becomes too slow or context-heavy.

Possible later response:

- generated compact index
- cache
- structured catalog

### Relationship failure

Natural wiki links cannot represent required relationships.

Possible later response:

- structured relationship representation

### Refresh failure

Source changes cannot be detected reliably.

Possible later response:

- change tracking
- lightweight state store

### Performance failure

Repeated analysis of the same documents becomes expensive.

Possible later response:

- caching
- persisted analysis state

Infrastructure must address an observed failure, not an anticipated one.

---

## 44. Infrastructure Escalation Principle

Use the following order:

```text
1. LLM reasoning
      ↓
2. existing document skills
      ↓
3. Company Wiki documents
      ↓
4. native repository search
      ↓
5. lightweight scripts if necessary
      ↓
6. local cache/index if necessary
      ↓
7. database if necessary
      ↓
8. semantic/vector infrastructure if necessary
```

Do not jump directly to the bottom of this stack.

---

## 45. Example End State

A mature Company Wiki might look like:

```text
Company Wiki
│
├── INDEX
│
├── People
│   ├── Hiring
│   ├── Leave
│   ├── Benefits
│   └── Performance
│
├── Finance
│   ├── Expenses
│   ├── Travel Reimbursement
│   ├── Purchasing
│   └── Approval Limits
│
├── Sales
│   ├── Pricing
│   ├── Customer Onboarding
│   └── Contracts
│
└── Operations
    ├── Customer Support
    ├── Escalation
    └── Internal Procedures
```

Each level progressively reveals additional knowledge.

Original documents remain underneath this structure as evidence rather than being duplicated into it.

---

## 46. Product Definition

> **Company Wiki is a portable agent skill that builds and maintains a progressively disclosed, evidence-backed wiki over existing company document systems.**

It does not own the source documents.

It does not require another knowledge database.

It does not assume a RAG architecture.

It uses the company's existing document infrastructure and the agent's existing document capabilities to transform stored information into navigable organizational knowledge.

---

## 47. V0.3 Implementation Directive

For the first implementation:

> **Start with no custom code.**

Implement:

```text
SKILL.md
+
workflow/reference Markdown
+
existing document skills/tools
+
Company Wiki documents
```

Run the architecture against real documents and real questions.

Only add software infrastructure after a concrete limitation has been observed and documented.

The purpose of V0.3 is not to prove that databases, embeddings, or retrieval infrastructure are unnecessary forever.

The purpose is to discover **how much organizational knowledge management an LLM agent can accomplish before any of them become necessary.**