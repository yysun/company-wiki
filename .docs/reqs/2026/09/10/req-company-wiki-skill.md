# REQ: company-wiki-skill

**Sources:**
- [PRD v0.4](../../../../../docs/company-wiki_PRD_v0.4.md)
- [Schema Specification v0.1](../../../../../docs/company-wiki_schema_v0.1.md)
- [Competency Questions v0.1](../../../../../docs/company-wiki_competency-questions_v0.1.md)

**Rebaseline:** On 2026-09-10 the user corrected the architecture. The product is a document-native
wiki over a cloud-drive document collection. The earlier schema-heavy, YAML-oriented design and its
assumption that folders are available are superseded by this requirement.
**Date:** 2026-09-10
**Deliverable:** the `company-wiki` agent skill package, examples, and behavioral test specification.
The skill itself is Markdown only; it contains no executable code.
**Chinese name:** 企业文库

## Problem

Company knowledge already lives in cloud-drive documents and source systems. A cloud drive may have no
usable folders, weak metadata, and poor YAML support. A central machine schema would add a second
knowledge system that is hard to keep current and is not how people read the source material.

The real missing layer is a navigable reading path: a small entry document, question- or domain-oriented
guides, focused detail documents, and links to authoritative source documents. The agent must be able to
follow that path with the host's ordinary document search, open, and link-following tools.

## Outcome

Deliver a portable skill that builds and uses a curated company wiki whose nodes are ordinary cloud-drive
documents and whose edges are ordinary native hyperlinks, bookmarks, or heading links.

The wiki is a navigation and evidence layer, not a graph database, ingestion pipeline, or replacement for
source systems. Original sources remain authoritative and are never copied or modified. The wiki is
progressively disclosed:

- **Level 0 — home/map:** what the wiki covers, how to start, and links to major guides.
- **Level 1 — guides:** a domain or competency-question reading path with a short summary and selected
  links.
- **Level 2 — detail:** a focused policy, concept, decision, definition, metric, dependency, or risk.
- **Level 3 — evidence:** the original source document or repository view.

The format is ordinary document prose, headings, lists, tables, and labeled links. YAML is not required
for organization documents. Folders are not required for discovery or navigation; titles, summaries,
headings, link labels, and native document identifiers are the durable handles.

## Acceptance Criteria

### Package and portability

- [x] `skills/company-wiki/` ships `SKILL.md`, `README.md`, and linked `references/*.md`; root
      `examples/` ships a worked document graph. Root `tests/` ships the E2E specification and fixtures.
- [x] The package contains no executable code, database, graph index, embedding, cache, connector, or
      organization-specific content. The organization wiki is created in the chosen cloud-drive
      collection and survives skill updates independently.
- [x] `SKILL.md` follows Agent Skills format: `name: company-wiki`, a single useful description under
      1024 characters containing `company wiki` and `企业文库`, ten concise behaviors, progressive
      loading, safety rules, and routing to every reference file. It is at most 150 lines and contains
      no detailed workflow procedure.
- [x] Each workflow can load `SKILL.md`, its own reference, and only the documents that reference names.
      All package links resolve. The shipped instructions contain no PRD/spec section-number dependency.
- [x] `README.md` explains the cloud-drive model, the package layout, how to initialize/query/maintain,
      and that wiki documents—not a local schema directory—are organization data to preserve.

### Document-native graph and progressive disclosure

- [x] The format defines a wiki document as a human-readable node with a title, a short summary, useful
      headings, and labeled links. Suggested labels such as `governed by`, `defined by`, `depends on`,
      `evidence`, and `see also` are a small vocabulary, not a machine schema.
- [x] Native link targets are preserved exactly when read or written. A visible label without a usable
      target is reported as a broken edge; a target without a meaningful label is reported as weak
      navigation. Heading anchors/bookmarks are supported when the host exposes them.
- [x] The home/map document links to guides; guides link to focused detail and evidence documents; detail
      documents link to authoritative sources and related nodes. A flat cloud-drive collection works just
      as well as a foldered one. Folders, filenames, YAML blocks, sidecars, and stable local paths are not
      runtime prerequisites.
- [x] The agent reads the home document's opening, headings, and link labels first, then follows only
      relevant edges. It does not load the whole collection by default. Each generated or maintained node
      has an explicit next-reading path.
- [x] A document's recommended human-readable labels may record type, owner, status, effective date,
      review date, language, or source authority in prose or a small table. Missing labels remain
      uncertainty; the agent does not invent them.
- [x] The host adapter contract is explicit: discovery may return a title plus provider-native document
      id or URL; reads return the opening, headings, link labels, and exact targets the provider exposes;
      writes create or edit only wiki documents; and link writes preserve both label and target. If a host
      cannot preserve a target, heading anchor, or permission boundary, the skill reports that capability
      as unverified or unavailable instead of guessing.

### Initialization

- [x] When no wiki home/map exists, init asks which document systems or collections to include and which
      language the wiki should use before creating anything. It skips a question only when the user's
      request answers it; host context does not count. It invites optional domains, authoritative sources,
      terminology, and real questions.
- [x] Init checks that the chosen drive supports reading and writing documents and native links. If it
      cannot write, it explains the limitation and does not pretend to have saved a wiki.
- [x] Before dependent initialization behavior is relied on, a bounded capability probe checks document
      discovery, read, create, edit, native link label/target round-tripping, heading/bookmark handling,
      and permission-denied behavior. A failed probe stops provider-specific claims and leaves the wiki
      unchanged.
- [x] Init inspects source titles, summaries, headings, links, and representative content; proposes a
      minimal home/map, guides, and focused nodes; and links to sources rather than copying them.
      Inferences are marked proposed until supported by evidence or confirmed by the user.
- [x] Init uses the user's chosen language for wiki prose and records it in a human-readable document
      line or table. If a home/map already exists, init makes no overwrite and hands off to maintenance.

### Query, maintenance, and validation

- [x] Query understands intent, terms, domain, question type, answer form, and time sensitivity; starts
      at the home/map; resolves terminology through relevant guides; follows labeled links; reads source
      evidence; evaluates authority, freshness, completeness, conflicts, and permission; and iterates when
      evidence is insufficient.
- [x] Answers distinguish established facts, inferences, hypotheses, and unresolved uncertainty; cite
      the documents actually read; surface conflicts; and distinguish “not found in the searched sources”
      from “does not exist.” Proposed meaning is treated as inference; proposed navigation may guide search.
- [x] Without a wiki, query searches original sources directly, creates nothing, and suggests init. When
      search, link targets, or a source are unavailable, it reports the limit and uses only what remains.
- [x] Maintenance proposes additions, corrections, link repairs, stale-source changes, and new guides
      with their trigger, evidence, affected questions, and minimal document edits. A user correction is
      approval; other changes require approval. Confirmed meaning is never silently rewritten.
- [x] Validation is read-only by default. It checks the home/map, reachable native links, useful labels,
      progressive-disclosure depth, summaries, source authority, stale/broken/orphan nodes, permission
      boundaries, and whether every competency-question category has a route.

### Access and safety

- [x] Access is host-capability-first: for cloud-drive documents, use only the cloud-drive/document skills,
      MCP tools, or agent plugins already exposed by the host app. For non-drive sources, reuse only other
      host-exposed repository, CLI, or API tools. Do not invent a connector, call an undocumented provider
      API, or install/assume a new integration. Git operations are read-only.
- [x] Source content is data, never instructions. Sources and restricted documents are never modified or
      copied into the wiki. The agent never reveals content the current user cannot access, never stores
      credentials, and identifies inaccessible material by label, owner, and route when permitted.
- [x] No derived retrieval infrastructure is introduced proactively, and the agent does not invent
      organizational facts.

### Competency-question coverage

- [x] The query and maintenance guidance has a handling path for categories A–O: authoritative lookup,
      ownership, version/change, decision, metric, dependency, incident, policy application, proposal,
      history, status, risk, reconciliation, vocabulary, and unknown/missing knowledge.

## Verification record

VR completed on 2026-09-10 against the story commits `eb30a72`, `46b1c9a`, `14ff808`, and `6ee5437`.
Structural checks, fixture checks, and isolated local-adapter smoke runs passed. The host capability
probe found Google Drive discovery/read/create/update tools, but no Drive destination was selected, so
provider-level write, permission-denied, heading/bookmark, and native-link round-trip behavior remain
unverified by design. The skill reports those limits instead of claiming provider behavior. No unit or
integration suite applies to the Markdown-only package. CR passed: no major findings.

## Constraints

- The skill is Markdown only, portable, and host/tool agnostic.
- Organization documents live in the user's chosen cloud-drive collection. They may be flat, foldered,
  or exposed only through search/list APIs; the skill must not depend on folder names.
- Organization documents use ordinary readable content and native links. The Agent Skills frontmatter in
  `SKILL.md` is package metadata; it is not a requirement for organization documents.
- Skill instructions are English. Wiki prose follows the language chosen at init. The product name is
  企业文库.
- The root layout is fixed: `skills/`, `examples/`, and `tests/`.

## Non-Goals

- Graph databases, RDF/OWL/SPARQL, vector retrieval, embeddings, ingestion or copying of sources,
  generated summaries for every source, per-document sidecars, YAML-dependent organization schemas,
  folder-management workflows, new connectors, workflow engines, and process automation.
- Host-specific installation, packaging, or cloud-drive provisioning.
- Benchmarking answer quality against raw search; that requires a real organization and a separate pilot.
- The old local `schema/` plus `competency-questions.md` organization-data layout.

## Open Questions (non-blocking)

1. Which connected cloud-drive/document provider is used for the pilot? The skill will use whichever
   document tools the host exposes and report capability gaps.
2. How much native link metadata each provider exposes (document id, heading anchor, backlink list) varies
   by host; the skill must preserve what is available and state what is not.

**Resolved by the user on 2026-09-10:**
- Use a document-native graph over cloud-drive documents.
- Treat ordinary documents as nodes and native links as edges.
- Use progressive disclosure for reading.
- Do not require folders or YAML for the organization wiki.
- Keep the skill under `skills/`, tests under `tests/`, and examples under `examples/`.
