# company-wiki / 企业文库

**Version:** `1.0.0`
**Repository:** https://github.com/yysun/company-wiki

See the [changelog](../../CHANGELOG.md) for release changes and known limitations.

`company-wiki` is a portable Agent Skill for an admin-governed Company Library Index and a user-controlled
Personal Wiki. The Index taxonomy is the governed backbone: it records canonical terms, aliases, source routes, and
authority guidance. A small set of typed native links forms the useful discovery graph on top, while native source
search retrieves original evidence before the agent answers with citations.

The cloud drive is the primary durable home of the wiki. Create ordinary native documents and links through the
host's existing document tools; users need neither Markdown files nor a Git repository or a separate wiki server.
GitHub distributes the skill, and Git commit history does not drive wiki maintenance. Explicitly selected local
folders support Markdown wiki storage, and repositories may be registered as original-material sources.

This package does not impose folders, YAML records, a graph
database, a provider-side derived search/evidence index, embeddings, source copies, or a connector. The small local
Markdown registry is configuration only. A flat document collection is valid.

## Package layout

- `SKILL.md` — concise routing, graph model, loading order, safety, and answer contract.
- `references/init.md` — initialize a home/map and the first reading paths.
- `references/bootstrap.md` — create a minimal Personal Wiki by reference.
- `references/curate.md` — make durable navigation knowledge or promote it by scope.
- `references/add-source.md` — discover candidates from search criteria and reconcile selected sources (`Ingest` alias).
- `references/change-protocol.md` — shared authority, approval, and failure contract for writes.
- `references/publication.md` — provider-managed access, explicit source inheritance, safe generation, and legacy cleanup.
- `references/registry.md` — select and safely persist user-level wiki configuration.
- `references/query.md` — route once, refine searches, read bounded evidence, and verify exact quotations.
- `references/maintain.md` — propose and apply corrections, repairs, and restructuring.
- `references/validate.md` — inspect graph health, source drift, gaps, and contradictions without writing.
- `references/document-format.md` — node, edge, disclosure, question-guide, and validation guidance.
- `../../examples/` — a flat illustrative graph, not organization content.

## Try the example

The entry document is [`company-wiki-home.md`](../../examples/sample-company/company-wiki-home.md).
Open it first, then follow the shortest relevant path:

`taxonomy and routing context → one route decision → native source search → original evidence`

For example, a workplace-policy question chooses the people route and source evidence together; a customer
metric question chooses the customer route and source evidence together. The outline ranks likely routes but
never blocks direct source search within the registered scope.

The Markdown files under `examples/sample-company/` are a local, flat-drive adapter for testing the
reading order and link graph. They are not a required filesystem layout and are not uploaded or copied
into a real wiki. In production, put equivalent ordinary documents in the chosen cloud drive and let
the host's existing cloud-drive/document skill, MCP tool, or agent plugin open them. For a local smoke
test, give the agent the whole example directory, tell it to start at `company-wiki-home.md`, and ask it
to answer using only documents reached from that entry point.

The installed skill contains no organization wiki. Init creates a small Company Library Index from bounded
representative sampling. Bootstrap creates a minimal Personal Wiki by reference without sampling or copying the
company corpus. Both link to original source documents instead of copying them and propose exact pages before
any durable write.

## Lifecycle

`Init → Bootstrap → Explore ↔ Query → Curate → Add Source → Maintain → Validate`

Add Source is the explicit bridge between discovery and durable knowledge. The user selects one new source by
default, or supplies a finite batch. A title, keywords, or filename pattern can first produce a bounded candidate
list inside the registered source scope; the user selects exact members before their bodies are read. The agent
reads the selection, compares it with relevant wiki nodes and evidence,
and presents the exact proposed edits. Source selection permits reading but not those edits; the agent writes
only after approval and revalidation. An unchanged source produces no edit or receipt. Validate is separately
read-only, while fixes route to Maintain.

This source-to-wiki reconciliation does not introduce centralized ingestion. `Ingest` remains a compatibility
alias. There is no source copy,
embedding pipeline, provider-side index, processing ledger, mandatory log, watcher, or background sync.

Wiki documents are organization data. Keep them in the drive and preserve them when updating or replacing
this skill. Do not move them into the installed package or treat package updates as a migration of the
organization's knowledge.

Publication uses provider-managed wiki permissions by default and requires current source access, exact-scope
authority, audience containment, and safe permissions from creation. Personal copies and index links are included.
Unavailable future source-permission inheritance alone does not block publication. Require continuing protection
across native surfaces only for an explicit user or governing requirement; missing required authorization yields
an authorized transient draft or direct-source answer. Shared generation excludes restricted context before synthesis;
known unsafe legacy reads are gated before model ingestion. V1 supplies no ACL sync or recall service.

Private user-owned local originals/tests remain supported with verified local identity/access and private scope;
synced/exported evidence does not inherit that exception. Writes require conditional/exclusive updates and
idempotent/conditional creates. Unknown outcomes are reconciled through exact targets/native operation keys before
retry; partial work is preserved without automatic rollback. Registration publishes the verified profile link last
with atomic conflict protection, but remains non-atomic across resources. No recovery ledger belongs in the registry.

The included adapter is a local fixture tool, not an enterprise connector. Package validation and isolated decision
tests do not establish native ACL enforcement or crash-safe transactions; deployments need provider acceptance.

## Shared local registry

Mutable configuration lives under `~/company-wiki`, with `index.md` as the single entry and linked profiles
under `wikis/`. The registry stores wiki and source locators, language, optional navigation inputs, and the
native home/map link. It stores no source copies, credentials, or evidence. The skill reads the index first,
follows only the selected contained profile, and never scans the directory.

Keep the versioned skill in this repository. Expose it to other same-user local Codex agents with
`~/.agents/skills/company-wiki` as a symlink to this `skills/company-wiki/` directory. The skill is not stored
under `~/company-wiki`. Local or remote agents that cannot read the user's home directory cannot use this
registry and must report that limitation.

## Use it

1. Install the skill where the host can load it.
2. Ask the agent to set up `company-wiki` with four required inputs: wiki name, original-material location
   and scope, writable wiki destination, and wiki language. It asks once for whichever required inputs are
   missing.
   You may also provide four optional inputs: key domains, owners, core/source-of-truth documents, and an
   initial navigation outline. Optional inputs shape the first reading paths but never block creation.
   The outline is navigation, not a required folder tree.
   The agent extracts values already clear from natural language and asks only about genuine gaps. For
   example, “创建一个财务文库” already supplies the name, finance scope, and Chinese language; the agent can
   ask only for the unknown original-material location and writable destination. A subject never authorizes
   a whole-drive search: source discovery stays inside locations the user explicitly specifies.
3. Add new or changed sources by exact native targets or search criteria such as `加入 EDU-C**测试报告`.
   For search criteria, select from the returned candidates first. Review the proposed wiki changes, then approve
   them if they correctly preserve authority, conflicts, and evidence links.
4. Ask company questions normally. The taxonomy resolves canonical terms and aliases, while the few relevant typed
   links guide discovery; neither limits source search. The agent makes one routing decision, searches registered
   source locations, reads relevant original evidence, and cites documents it actually opened.
5. Ask it to Curate or Maintain structure, or Validate links and coverage. Every durable change has its own
   concrete proposal and approval; corrections are not approval. Validation is always read-only.

For cloud-drive work, the skill reuses only cloud-drive/document skills, MCP tools, or agent plugins the host
app already provides. For non-drive sources it uses only the host's corresponding exposed repository, CLI,
or API tools. It never invents a connector, calls an undocumented provider API, or assumes a new integration.
It reports unreachable sources, missing link metadata, and permission limits instead of inventing facts or
building retrieval infrastructure.
