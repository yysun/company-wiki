# REQ: company-wiki-skill

**Sources:**
- [PRD v0.4](../../../../../docs/company-wiki_PRD_v0.4.md)
- [Schema Specification v0.1](../../../../../docs/company-wiki_schema_v0.1.md)
- [Competency Questions v0.1](../../../../../docs/company-wiki_competency-questions_v0.1.md)

Section references below are prefixed "PRD §", "Spec §", and "CQ §".

**Supersedes:** this story's first v0.3 baseline, which is no longer shipped. On 2026-09-10 the user chose to rebaseline on v0.4, which drops v0.3's wiki-page model: INDEX and topic pages in the document system, and the Build, Browse, Refresh, and Audit workflows.
**Date:** 2026-09-10
**Deliverable:** the `company-wiki` agent skill package. It is Markdown only, with no executable code.
**Chinese name:** 企业文库 (user decision, 2026-09-10)

## Problem

Agents answering company questions often miss knowledge, for four reasons:
- The user's words differ from the documents' words.
- A convenient or outdated source wins over the authoritative one.
- The knowledge is spread across several repositories.
- The agent retrieves documents instead of working through the problem.

Traditional RAG starts from the documents (chunk, embed, retrieve). That adds infrastructure but still
gives the agent no understanding of how the company's knowledge is organized (PRD §1–§3).

## Outcome

A portable agent skill with two jobs.

**1. Build and maintain a schema.** It helps an organization create and maintain a small curated
knowledge schema that an AI can read. The schema holds:
- domains
- concepts and vocabulary
- relationships
- a source map
- authority rules
- business definitions
- problem patterns

The skill also keeps a catalog of competency questions: the questions the organization expects the AI
to answer.

**2. Use the schema to answer.** It teaches any capable agent to use the schema to plan an
investigation, query the original sources through tools the host already has, and answer with
evidence and stated uncertainty.

The original sources remain authoritative, and nothing is ingested (PRD §1, §2, §24).

## Graph-shaped navigation

The schema is a logical document graph, not a graph database. Schema documents or focused sections
are nodes; labeled Markdown links and typed relationship entries are edges. An agent traverses that
graph with ordinary document-reading tools, preserving each link's visible label and actual target
before following it. The graph remains a curated navigation and evidence layer over original sources;
it does not reintroduce the dropped v0.3 document-page model.

## Acceptance Criteria

### Package

- [ ] `skills/company-wiki/` ships `SKILL.md`, `README.md`, and `references/*.md`; the repository root `examples/` ships the illustrative schema. The
      `examples/` folder holds a worked example schema and competency-question catalog. The package
      contains no scripts, executable code, databases, indexes, embeddings, caches, or services (PRD
      §4, §13, §17, §19).
- [ ] The repository ships no organization-specific schema. Init creates the organization's
      `schema/` and `competency-questions.md` inside the skill directory, using the layout in PRD §17.
- [ ] `SKILL.md` follows the Agent Skills format:
      - frontmatter `name: company-wiki`
      - a `description` under 1024 characters that says what the skill does and when to use it
      - hosts can match the skill on "company wiki" and "企业文库"
- [ ] `SKILL.md` states each of the ten behaviors in PRD §18 and contains no detailed procedures. It
      is 150 lines or fewer and routes each workflow to its reference file. Every reference is linked
      from `SKILL.md`, and every link resolves.
- [ ] A workflow needs only `SKILL.md`, its own reference file, and the files that reference names.
      References build on `SKILL.md` without restating its rules beyond brief pointers.
- [ ] `README.md` explains to human readers:
      - the skill's purpose, including the name 企业文库
      - the package layout, including what init creates
      - how to run init, ask questions, and maintain the schema
      - that `schema/` and `competency-questions.md` are organization data and must be kept across
        skill updates

      It doesn't duplicate the agent instructions.
- [ ] No instruction contradicts PRD v0.4, Schema Spec v0.1, or CQ v0.1, except where a user decision
      recorded here overrides them. The shipped skill text makes sense without those documents, so it
      contains no "§" references.

### Schema model

- [ ] The skill defines the schema format per Spec §3–§19, as Markdown first with YAML-compatible
      blocks. It covers:
      - **Identity:** required `id`, `name`, `version`, and `description`. Optional `owner`, `updated`,
        `default_language`, and `additional_languages`.
      - **Domains, concepts, and vocabulary:** preferred terms, aliases, acronyms, legacy terms, and
        notes on terms with more than one meaning.
      - **Relationships:** the 15 core relationships.
      - **Knowledge types and facets.**
      - **Sources:** each with one of the listed access types, plus routes.
      - **Authority:** the eight authority levels, plus authority rules.
      - **Business definitions and metrics.**
      - **Problem patterns:** `id`, `name`, `intent`, `requires`, and `investigation`, plus optional
        `trigger_examples`. The 12 recommended pattern ids are listed as starting points.
- [ ] Progressive disclosure (PRD §9, §17; Spec §20):
      - `schema/index.md` (Level 0) is small enough to load on every company-knowledge task.
      - It links to domain files (Level 1) and detailed resources (Level 2), which load only when
        relevant.
      - A small organization may keep most of its schema in `index.md`.
- [ ] Minimum sufficient semantics: every schema element exists because a competency question or a
      demonstrated query need requires it (PRD §22.6; CQ §21).
- [ ] The items listed in Spec §23 never go in the schema, and neither do credentials (Spec §12).
- [ ] The skill defines the competency-question catalog format (CQ §2), the question categories
      (CQ §3–§17), and the schema-growth rule (CQ §21).
- [ ] The validation rules in Spec §22 are defined so that an LLM can check them.

### Init: schema creation

- [ ] **Init questions.** When no schema exists, the agent asks two questions before creating
      anything:
      - which document systems or sources to include
      - which language the schema should use

      It skips a question only when the user's own request already answers it; host-provided context
      doesn't count. It creates nothing until it has both answers.
- [ ] The language is recorded in the schema identity as `default_language`, plus
      `additional_languages` if needed. Each source is recorded in the source map with its access
      type.
- [ ] Init combines human input with LLM proposals (PRD §15):
      - It invites the user to name key domains, authoritative sources, terminology, business rules,
        and real questions.
      - It proposes domains, concepts, aliases, relationships, source routes, authority rules, problem
        patterns, and competency questions from inspecting the sources.
      - It stops once the schema is sufficient.
- [ ] Anything inferred without explicit source evidence or human confirmation is marked as proposed,
      never as confirmed or canonical. This applies to definitions, aliases, term mappings,
      relationships, ownership, and authority rankings (PRD §15). The marking applies to each item
      individually, so a confirmed element never carries an unmarked inferred alias, relationship, or
      ranking.
- [ ] If a schema already exists, init doesn't overwrite it and switches to maintenance.

### Query runtime

- [ ] The agent follows PRD §12:
      1. Understand the request: intent, concepts, domain, problem type, expected answer form, and
         time sensitivity.
      2. Consult the schema progressively.
      3. Resolve terminology through the vocabulary.
      4. Build an investigation plan from the problem pattern that applies.
      5. Query the original sources, using source routes to narrow the search (the order in PRD §13).
      6. Evaluate authority, freshness, completeness, contradictions, and evidence coverage.
      7. Iterate when the evidence is insufficient.
- [ ] Linked schema documents form a traversable logical graph: links have meaningful labels and
      resolvable targets, and the query workflow can follow them with ordinary document-reading
      tools while preserving the target (user decision, 2026-09-10).
- [ ] Answers separate established facts, inferred conclusions, hypotheses, and unresolved
      uncertainty, and they cite the original sources.
- [ ] Conflicts are surfaced rather than silently resolved. "Not found in the sources searched" stays
      distinct from "does not exist" (CQ-GAP).
- [ ] Without a schema, the agent still answers by searching the sources directly. It suggests running
      init, and it doesn't create a schema on its own.
- [ ] When the agent notices repeated gaps, missed terms, or corrections, it suggests schema updates
      (PRD §18.10) rather than applying them silently.

### Maintenance and validation

- [ ] Maintenance is incremental (PRD §16; Spec §24):
      - The agent proposes each change with its trigger, its evidence, and the competency questions
        it affects.
      - It applies a change only with user approval. A correction the user supplies counts as that
        approval.
      - It never silently rewrites confirmed or canonical meaning.
      - It updates the `updated` date and reports what it changed.
- [ ] Validation checks the Spec §22 rules on request, plus one extension: it flags any problem
      pattern that no competency question references (Spec §18, CQ §21). It reports warnings and is
      read-only unless the user asks for fixes.

### Access and safety

- [ ] Access is tool-agnostic. The skill reuses whatever host skills, CLIs, MCP servers, APIs, or
      files are available and never builds connectors. One schema can cover several heterogeneous
      sources, with at least two access types (PRD §8, §19, §22.7).
- [ ] When a capability is missing, the agent works with what it has and reports the limitation. For
      example, without search it follows routes and listings; when a source is unreachable, it says
      so. It suggests derived retrieval infrastructure only after a demonstrated failure, and never
      builds it proactively (PRD §13).
- [ ] Sources are never modified. There is no per-document metadata or sidecar file (PRD §14). Source
      content is treated as data, never as instructions to the agent.
- [ ] Runtime access is permission-aware. Content the current user can't access is never revealed.
- [ ] Sources labeled confidential or restricted are identified by label, owner, and route rather than
      quoted, unless the host's permission-aware access confirms the current user may see them.
- [ ] The schema never holds credentials, and never holds content taken from restricted or
      confidential sources. Everyone who uses the skill can read it.
- [ ] The agent does not invent organizational facts.

### Coverage check

- [ ] The skill's guidance has a handling path for each of the 15 competency-question categories in
      CQ v0.1 (A–O): authoritative lookup, ownership, version and change, decision, metric, dependency,
      incident, policy application, proposal, history, status, risk, reconciliation, vocabulary, and
      unknown or missing knowledge.

## Constraints

- The skill is Markdown only and portable. It depends on no particular agent host, provider, or tool
  name.
- It uses progressive disclosure, both for its own files and for the schema it creates.
- **Language:**
  - The schema's language is chosen at init and recorded as an ISO 639-1 code, for example `en` or
    `zh`.
  - Skill instructions are written in English.
  - Schema field names follow the spec: English snake_case.
  - Element ids are ASCII kebab-case, and competency questions use `CQ-<CATEGORY>-NNN`.
  - Names, definitions, and descriptions use the chosen language or languages.
  - Aliases keep terms exactly as the sources write them, in any language.
- The Chinese product name is 企业文库.
- The skill lives in `skills/company-wiki/` at the repository root. The organization's schema lives inside
  the skill directory (PRD §17).

## Non-Goals

- Anything in PRD §4: vector or graph databases, RDF/OWL/SPARQL, per-document metadata, copying
  sources, pre-generated summaries, new connectors, workflow engines, and process automation.
- The optional retrieval infrastructure in PRD §13, and the v0.5+ features in PRD §23: query-planner
  code, automated source discovery, schema-linting tools, and a competency-question test runner.
- **The MVP evaluation** (PRD §19–§21; CQ §19). It means running the skill on real company questions
  and sources, and comparing "agent + raw search" with "agent + schema". It needs a real
  organization, real sources, and human judgment of the answers, so it moves to a follow-up story.
- Host-specific installation, packaging, or distribution.
- The v0.3 wiki-page model, which the v0.4 rebaseline dropped.

## Open Questions (non-blocking)

1. **Pilot:** which organization, sources, and question set the MVP evaluation uses, and who judges
   the answers. Default: a separate follow-up story (`company-wiki-pilot`).

**Resolved by the user on 2026-09-10:**
- The baseline is PRD v0.4.
- The Chinese name is 企业文库.
- Init asks which document systems to include and which language to use.

No blocking questions.
