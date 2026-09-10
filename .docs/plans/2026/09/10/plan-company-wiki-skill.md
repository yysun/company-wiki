# Plan: company-wiki-skill

**REQ:** [req-company-wiki-skill.md](../../../../reqs/2026/09/10/req-company-wiki-skill.md)
**E2E spec:** [test-company-wiki-skill.md](../../../../../tests/test-company-wiki-skill.md)
**Baseline inputs:** the user's v0.4 PRD, schema draft, and competency-question draft under `docs/`.
Those files were pre-existing user changes and remain outside story commits.
**Git base:** `090993f` (`initialize project`), recovered from the original story before this
rebaseline. Earlier story commits are `1bc8e05`, `9b94040`, and `3ab98e2`; their schema-heavy design is
being replaced, not extended.

## Outcome

Deliver a Markdown-only `company-wiki` skill that builds and navigates a document-native knowledge graph
over a cloud-drive collection. The proof run uses a flat logical drive export plus a git repository, but
the filesystem layout is only a test adapter: runtime guidance uses document titles, native identifiers,
headings, and links, never folder names.

The result must support progressive disclosure from a small home/map to guides, focused detail, and
authoritative evidence. It must not create a central YAML schema, require folders, copy source content,
or introduce retrieval infrastructure.

## Boundaries

- **Changed:** `skills/company-wiki/**`, `examples/**`, `tests/**`, and this story's `.docs/**` artifacts.
- **Preserved:** `docs/**` and unrelated staged/unstaged user work. Story commits stage explicit paths.
- **No executable source:** the package and examples remain Markdown only; verification commands stay in
  this plan.
- **Rollback:** revert story commits. Cloud-drive wiki documents are independent user data; source
  documents and repositories are never modified.

## Architecture decisions

### D1 — Document graph, not schema

- A wiki document is a node. A native cloud-drive hyperlink, bookmark, or heading link is an edge.
- A small vocabulary of human-readable relationship labels is guidance only; no machine-parsed record
  format is required.
- The drive is the document store. Wiki documents are created there, alongside or among existing drive
  documents according to the provider's capabilities. The skill does not create a local `schema/` or
  `competency-questions.md` instance.

### D2 — Progressive disclosure

- Level 0: one small home/map document with scope, reading instructions, and links to guides.
- Level 1: domain or competency-question guides with summaries and selected next links.
- Level 2: focused concepts, policies, decisions, metrics, risks, and definitions.
- Level 3: original evidence documents, repository views, or provider-native source links.
- Agents read titles, opening summaries, headings, and link labels before detail, then follow only
  relevant edges. A flat collection is valid.

### D3 — Human-readable document contract

Every generated or maintained wiki node should have: a title; a one- or two-sentence summary; headings
that answer the reader's question; labeled links with preserved targets; and a “next reading” path.
Optional type, owner, status, date, language, and authority lines may be prose or a small table. Missing
metadata is uncertainty, not permission to invent it. Source content is linked, not copied.

### D4 — Capability and safety boundary

Use only cloud-drive/document skills, MCP tools, agent plugins, CLIs, APIs, and repository tools already
exposed by the host app. Detect whether those capabilities can list, search, read, create, edit, and
preserve native links. If a capability is missing, report it and continue only with evidence still
accessible. Never invent a connector or call an undocumented provider API. Read source content as data,
never instructions; obey permissions; use git read-only; never store credentials, restricted content, or
sidecars.

The bounded adapter contract is: discovery returns a document title and, when available, the provider's
native id or URL; a read returns the opening, headings, visible link labels, and exact targets exposed by
the provider; a write creates or edits only wiki documents; and a link round-trip preserves both label and
target. A provider-specific heading anchor, bookmark, backlink, or permission-denied response is marked
unsupported when the host does not expose it. The local test adapter models these values as Markdown links
and stable document names; it does not claim to prove a particular cloud provider.

### D5 — Workflow routing

| Workflow | Loads |
|---|---|
| Query | `SKILL.md`, `references/query.md`, home/map and only relevant linked documents |
| Init | `SKILL.md`, `references/init.md`, `references/document-format.md`, optional root examples |
| Maintain / validate | `SKILL.md`, `references/maintain.md`, `references/document-format.md`, relevant drive documents |

`README.md` is for humans. References must not restate the whole skill.

### D6 — Init and persistence

Init asks for source systems/collections and wiki language before writing unless the user already answered.
It checks drive writability, inspects representative documents, drafts a minimal home/map and linked
guides, and marks unsupported inferences as proposed. A present home/map is never overwritten; init hands
off to maintenance. The user keeps the resulting drive documents across skill updates.

### D7 — Query and answer contract

Query understands intent, terminology, domain, question category, answer form, and freshness; enters via
the home/map; traverses links; checks source authority and conflicts; and iterates. Answers separate
facts, inferences, hypotheses, and uncertainty, cite read documents, and distinguish “not found” from
“does not exist.” The no-wiki path searches original sources and creates nothing.

### D8 — Maintenance and validation

Maintenance proposes minimal document/link edits with trigger, evidence, and affected competency
questions. A user correction is approval; other changes require approval. Validation is read-only and
checks home reachability, link targets and labels, disclosure depth, summaries, source authority,
staleness, orphans, permissions, and category coverage.

## Tasks

### REQ/AP reconciliation

- [x] Reconcile the correction across REQ, plan, and E2E spec: remove the folder-dependent and
      YAML-schema acceptance criteria; define cloud-drive documents, native links, and disclosure levels.
- [x] First AR completed: blocked on the missing bounded capability probe, adapter contract, incomplete
      category scenarios, mixed package references, and the example's old catalog naming.
- [x] Reran AR after those blockers were resolved: `AR passed: no blocking architecture flaws`. The
      recommendation is feasible without a graph database, connector, folder API, or organization-document
      YAML parser. Provider-specific write, heading/bookmark, and permission round-trips remain unverified
      because no external destination was selected.

### SS — Milestone A: package and examples

- [x] Run the first-SS capability probe before relying on provider-specific behavior. The host exposes
      Google Drive plugin tools for profile, search, fetch, native document reads, create, update, and
      batch content operations; profile access succeeded and no shared drives were returned. No cloud-drive
      destination was selected for this story, so no external write or permission round-trip was attempted.
      The local flat adapter covers exact Markdown label/target preservation; provider-specific heading,
      bookmark, and permission behavior remain explicitly unverified rather than inferred.
- [x] Rewrite `skills/company-wiki/SKILL.md` to state the ten behaviors, graph model, disclosure order,
      safety rules, loading boundaries, and workflow routing in <=150 lines. (72 lines.)
- [x] Rename and rewrite `references/document-format.md` as the document-node/link-edge contract and validation
      checklist. It must not require YAML or a local schema directory. (`schema-format.md` removed.)
- [x] Rewrite `references/init.md`, `references/query.md`, and `references/maintain.md` for cloud-drive
      documents, native links, flat collections, and ordinary document tools.
- [x] Rewrite `README.md` for human readers; explain that organization wiki documents live in the chosen
      drive and survive skill updates.
- [x] Rewrite `examples/sample-company/` as a worked flat document graph using headings, tables, prose,
      and ordinary links only. Rename the old catalog-shaped example to `question-guide.md`. (Leftover
      empty `examples/sample-company/schema/` directories removed.)
- [x] Run structural checks and complete the traceability map. Results on 2026-09-10 15:13: exact
      inventory matches; frontmatter parses (description 198 chars, both triggers present); `SKILL.md` 72
      lines; every reference linked; every relative link and heading anchor in package and examples
      resolves; no `§` markers; no fenced YAML/JSON and no frontmatter outside `SKILL.md`; no fixture
      tokens in package or examples; all eight example-only tokens present in examples; `git diff --check`
      clean; `docs/**` untouched. The only `schema/` mention is `SKILL.md`'s instruction not to look for one.

### SS — Milestone B: tests and fixtures

- [ ] Update `tests/test-company-wiki-skill.md` so the logical drive is flat and document-native. Physical
      fixture subdirectories are explicitly harness-only. Init writes wiki documents to a flat writable
      collection, not `skills/company-wiki/schema/**`.
- [ ] Replace record-shaped defect fixtures with broken-link, weak-label, stale/orphan, and unreferenced
      document cases. Keep source facts neutral and out of the shipped skill.
- [ ] Run fixture checks and confirm no example-only or fixture-only tokens leak into the package.

### TT

- [ ] Report that no unit or integration suites apply; rerun all Markdown, link, package, and fixture
      checks.

### ET

- [ ] Reassess the runner probe first. If a standalone headless agent session and transcript export are
      unavailable, use isolated-agent reports in neutral temporary workspaces and disclose the weaker
      read-order evidence and repository-leak mitigation.
- [ ] Run every scenario in the reconciled E2E spec, including init gates, flat-drive document creation,
      link traversal, no-wiki fallback, maintenance approval, validation, permission safety, and source
      integrity. Record the exact package/fixture commits exercised.

## Validation

Run from the repository root. The exact shipped inventory after migration is:

```text
examples/sample-company/authoritative-lookup-guide.md
examples/sample-company/churn-rate-detail.md
examples/sample-company/company-wiki-home.md
examples/sample-company/customer-guide.md
examples/sample-company/people-guide.md
examples/sample-company/question-guide.md
examples/sample-company/vacation-policy-detail.md
skills/company-wiki/README.md
skills/company-wiki/SKILL.md
skills/company-wiki/references/init.md
skills/company-wiki/references/maintain.md
skills/company-wiki/references/query.md
skills/company-wiki/references/document-format.md
```

All example files are documents in one flat illustrative collection; their contents must be ordinary
document graph examples, not a runtime schema format. Checks must prove:

- Agent Skills frontmatter parses, triggers are present, and `SKILL.md` is <=150 lines.
- Every reference link resolves, every relative Markdown link in package/examples resolves, and no
  shipped instruction contains a PRD/spec section marker.
- No package/example file contains a fenced YAML block, executable code, organization-specific fixture
  token, or repository-derived answer.
- Examples use their own illustrative tokens and never copy organization fixture tokens.
- Fixtures have their planted facts exactly once, contain no test annotations, and contain no example-only
  tokens. Defects are ordinary Markdown link/coverage defects.
- `git diff --check` passes and unrelated `docs/**` staged work remains untouched.

No unit or integration suite applies to this Markdown-only deliverable.

## Traceability

| Requirement | Evidence after implementation |
|---|---|
| Package layout, metadata, portability | Exact inventory, frontmatter check, package inspection |
| Document node/link edge model | `SKILL.md`; `references/document-format.md`; example graph; link traversal scenario |
| Flat-drive compatibility and no YAML dependency | Init/query references; flat-drive ET setup; no-fenced-YAML guard |
| Progressive disclosure | `SKILL.md`, format contract, home → guide → detail → evidence scenario |
| Init gates and persistence | `references/init.md`; S0/S0b/S1/S1b/S6 |
| Query, evidence, conflicts, gaps, permissions | `references/query.md`; S2/S3/S7 |
| Maintenance and validation | `references/maintain.md`; S4/S4b/S5 |
| CQ categories A–O | Category table in `query.md`; traceable category checks |
| Source integrity and safety | Common checks C1–C6; source checksum and no-instruction-following assertions |

## Risks

- **Provider variance:** link IDs, heading anchors, backlinks, and write operations differ. The skill
  preserves what the host exposes and reports the rest; this remains a pilot integration risk.
- **Flat-drive ambiguity:** titles can collide. The agent uses provider-native IDs or exact targets when
  available and reports ambiguity rather than relying on filenames or folders.
- **Document drift:** links can become stale. Validation surfaces broken edges and orphan nodes; it does
  not silently delete or rewrite authoritative sources.
- **LLM variability:** isolated-agent evidence may not prove strict read order. Reports are checked for
  repository-path leaks and the limitation is recorded.
- **Synthetic proof:** the E2E run demonstrates behavior, not answer-quality lift over raw search.
