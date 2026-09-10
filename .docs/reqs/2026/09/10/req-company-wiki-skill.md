# REQ: company-wiki-skill

**Source:** [Company Wiki — PRD v0.3](../../../../../docs/Company%20Wiki%20—%20PRD%20v0.3.md) (§ references below point to it)
**Date:** 2026-09-10
**Deliverable:** the V0.3 `company-wiki` agent skill — `SKILL.md` + `references/*.md`, no executable code

## Problem

Organizations keep hundreds to low thousands of documents in existing systems (Google Drive,
SharePoint/OneDrive, WeCom Drive/企业微盘, Dropbox, local/network shares). Knowledge in them is hard to
navigate: agents and people fall back to broad repository search, re-read the same documents, miss
authoritative sources, and cannot see conflicts or gaps. The usual answer — a RAG stack with ingestion,
indexes, and databases — adds infrastructure before anyone has shown it is needed (§2, §3).

## Outcome

A portable agent skill that teaches any capable agent to build, navigate, answer from, refresh, and
audit a progressively disclosed, evidence-backed wiki over an organization's existing document
system. It uses only the document-access capabilities the host already provides. The source documents
remain the system of record and are not modified (§1, §4, §46, §47).

## Acceptance Criteria

### Package and progressive disclosure

- [ ] A `company-wiki/` skill directory exists containing only `SKILL.md` and `references/*.md` — no
      scripts, executable code, databases, indexes, services, or configuration for them (§38, §47).
- [ ] `SKILL.md` follows the Agent Skills format: YAML frontmatter with `name: company-wiki` (matching
      the directory) and a `description` under 1024 characters that states what the skill does and when
      to use it. Hosts can match it on English and Chinese naming ("company wiki", "企业 Wiki") (header, §36).
- [ ] `SKILL.md` states each of the 12 durable core behaviors in §37 and contains no detailed
      workflow procedures (§36, §37).
- [ ] `SKILL.md` is compact (≤ 150 lines) and routes each workflow to exactly one reference file.
      Every reference is linked from `SKILL.md` and every link resolves (§36).
- [ ] Reference files cover the Build, Ask, Browse, Refresh, and Audit workflows plus the shared
      wiki-authoring rules. Only the active workflow's file needs to be loaded. The write workflows
      (Build, Refresh) point to the authoring rules instead of duplicating them (§36).
- [ ] References expand on workflow behavior without restating `SKILL.md` core rules beyond
      brief pointers, and no instruction contradicts PRD v0.3.

### Tool-agnostic document access

- [ ] Instructions depend only on generic capabilities: list, search, read, inspect metadata, follow
      links, and create or update wiki documents. They tell the agent to use whatever host skill, MCP
      tool, CLI, connector, or filesystem access is available. No specific provider tool is required and
      no adapter layer is defined (§7, §8).
- [ ] The skill says how to proceed when a capability is missing, for example read-only access or no
      search. It degrades or reports the limitation instead of building substitute infrastructure (§3,
      §44).
- [ ] The skill says how to locate an existing wiki root (conventional "Company Wiki" area or a
      location the user supplies). Ask and Browse still work when no wiki exists yet, by falling back to
      source search and reading (§9, §13).
- [ ] Wiki page structure and linking conventions work in Google Docs, SharePoint pages, WeCom
      documents, and Markdown. Links use the platform's native document links where supported and fall
      back to unambiguous titles/paths otherwise (§9, §22).

### Wiki model (authoring rules)

- [ ] The four knowledge levels are defined with their purpose and a page shape (Level 0 Index, Level 1
      Domain Guide, Level 2 Topic Page, Level 3 Original Sources), consistent with §12 and §45.
- [ ] Every wiki page is required to answer at least one of: where to go next, what to know, where the
      evidence is (§34). The progressive-disclosure rules in §35 are stated: keep higher levels small,
      push detail down, don't duplicate, follow sources only when needed, preserve escape routes.
- [ ] The materialization strategy defines what is always persisted, what is persisted when
      useful, and what is generated on demand, with criteria for each (§16).
- [ ] Structure is driven by topics, not files: no page per source document, and folder hierarchy is
      treated as evidence rather than as the wiki's organizing structure (§17, §18).
- [ ] Source authority uses the states in §19 (authoritative, current, draft, historical, superseded,
      informational, unknown), and inferred authority is marked as inference, never presented as policy.
- [ ] Conflicts are shown with both sources, their positions, and any inferred precedence marked as
      unverified (§20). Missing knowledge is reported as a "Possible knowledge gap", never as proof that
      information does not exist (§28).
- [ ] Topic pages link to their primary sources. Metadata stays lightweight and readable by people
      (e.g., Status / Primary source / Last reviewed), with no metadata sidecars and no machine-state
      dumps (§22, §29, §32).
- [ ] The readability rules in §29 and §30 are stated for both human readers and LLM readers.

### Workflows

- [ ] **Build** follows §25. It inspects structure, samples and searches representative documents,
      finds domains and topics, then creates the root, a compact INDEX, domain guides, useful topic pages,
      and source links. It stops before unnecessary detail and never summarizes every source.
- [ ] **Ask** follows §13, §14, and §23. It consults the minimum useful level and picks wiki navigation
      or direct repository search depending on the question type. It checks whether the wiki is
      sufficient before reading sources, prefers current authoritative evidence, exposes conflicts and
      uncertainty, and cites evidence. It persists content only when that content is likely to be reused.
- [ ] **Browse** follows §24: it surfaces the nearest domain or topic, its subtopics, related topics,
      and key sources, and lets the user go progressively deeper toward evidence.
- [ ] **Refresh** follows §21 and §26. It finds candidate changes from signals the document system
      already provides, compared against review dates recorded in the wiki, with no separate state
      store. It updates only affected pages and checks related topics instead of rebuilding.
- [ ] **Audit** follows §27 and §28. It checks the corpus and the wiki for every problem type listed
      in §27, reports recommendations, and changes neither sources nor wiki pages unless the user
      explicitly asks.

### Safety and infrastructure discipline

- [ ] Source documents are never modified, annotated, converted, or copied without explicit
      authorization (§6, §27, §32).
- [ ] The permission rules in §33 are stated: never expose content the user cannot access, never
      persist restricted content into a more broadly accessible page, prefer runtime synthesis when
      source ACLs differ, and inherit restrictions where the platform supports it. No replacement ACL
      system is defined.
- [ ] The agent is told not to invent organizational facts (§37.10).
- [ ] The escalation order in §44 and the failure-signal rule in §43 are stated: infrastructure is
      added only for an observed, documented failure, and the agent must never create it proactively
      (§38).

### Coverage check

- [ ] Each of the nine pilot question categories in §40 (direct fact, policy, procedure, discovery,
      cross-document synthesis, authority, conflict, navigation, gap detection) maps to a clear handling
      path in the skill's workflows.

## Constraints

- Only Markdown skill content. The PRD's "no custom code" directive (§47) and the infrastructure
  exclusions (§3, §38) are hard constraints for this story.
- The skill must stay portable: no dependence on one agent host, provider, or tool name.
- The skill follows the same progressive disclosure it prescribes: a small `SKILL.md`, with detail
  in references (§36).
- Default wiki content language: the dominant language of the source corpus unless the user
  specifies one. Skill instructions are written in English.
- Default location: `company-wiki/` at the repository root.

## Non-Goals

- Databases, vector stores, custom indexes, ingestion pipelines, source adapters, background
  services/daemons, custom search or retrieval services, or a backend (§3, §38).
- One wiki page per source document; copying, converting, or annotating the source corpus (§6, §17).
- A replacement ACL system, graph database, formal relationship schema, or enterprise ontology
  (§5, §31, §33).
- Growing into a Knowledge Space, AI workspace, workflow engine, or business database (§5).
- **Running the reference pilot** on 100–500 real documents and scoring it against §41 and §42. That
  needs a real corpus, host document access, and human judgment of answers. It is deferred to a
  follow-up story. PRD success criteria 7–9 are covered by this story's constraints. Criteria 1–6
  and 10 can only be confirmed by the pilot.
- Host-specific installation, packaging, or distribution of the skill.

## Open Questions (non-blocking; defaults applied above)

1. **Pilot scope and corpus:** which document system and corpus the pilot will use, and who judges
   answer quality. Default: a separate follow-up story (`company-wiki-pilot`).
2. **Wiki content language:** should wiki pages match the source corpus language (default), always
   use the user's language, or be bilingual for mixed English/Chinese organizations?
3. **Wiki root naming:** keep the conventional "Company Wiki" name as the default, or also check for a
   localized root such as "企业 Wiki"?

No blocking questions.
