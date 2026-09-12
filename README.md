# company-wiki / 企业文库

[中文](README.zh-CN.md)

`company-wiki` is a portable agent skill for building and using a permission-aware Company Library Index and
user-controlled Personal Wiki over existing cloud-drive and repository documents.

The Company Library Index is a document-native taxonomy and source map:

- the taxonomy is the governed backbone for canonical terms, aliases, authority, and source routes;
- a navigation tree organizes the taxonomy without claiming relationships;
- a small set of typed native links supplies the useful discovery graph on top;
- scoped cloud-drive or repository search retrieves original evidence;
- answers cite the evidence actually read and distinguish facts from uncertainty.

It does not require a vector database, graph database, metadata sidecar, central document repository,
or a new connector. Original documents remain authoritative.

The Personal Wiki accumulates durable user judgment and routing context—not a private document cache. It retains
reused concepts and source routes, project and decision context, annotations, hypotheses, priorities, and reusable
investigation patterns, so later questions start with better judgment. Company facts still require current original
evidence when they are used.

An explicitly declared local folder works for both source retrieval and Markdown wiki storage. The source folder
and writable wiki folder must still be separate; local-folder support never permits a wider filesystem search or a
write back to the source collection.

## Repository layout

- [`skills/company-wiki/`](skills/company-wiki/) — installable skill package and workflow references.
- [`examples/`](examples/) — small flat example graph for local smoke tests and demonstrations.
- [`docs/`](docs/) — product requirements, schema, and competency material.
- [`tests/`](tests/) — end-to-end specification, fixtures, and validation scenarios.

## Try the example

Start with [`examples/sample-company/company-wiki-home.md`](examples/sample-company/company-wiki-home.md), then
make one routing decision from its compact outline before opening source evidence.

The sample files are illustrative only; they are not real company content and do not prescribe a
folder structure for production use.

### Local-folder demo

No upload is required for a local or private demonstration. Declare separate folders for the bounded source corpus
and writable wiki:

```text
Company Wiki Demo/
├── Test Sources/   # fixture documents; bounded read/search scope
└── Test Wiki/      # separate writable Markdown wiki destination
```

For example, ask:

> Create a demo wiki named Company Wiki Demo. Original material: the local `Test Sources` folder only. Wiki
> destination: the separate writable local `Test Wiki` folder. Use English. Do not search outside `Test Sources`.

This supports smoke tests and private Personal Wikis. A cloud-synced folder can use the same local adapter, but
local availability does not prove cloud-provider identity, ACLs, or governance. Use a provider integration for
Team or Company writes that require those checks.

### Cloud-drive demo

Do not upload the repository examples verbatim as a real wiki. To test a supported provider, deploy a small,
controlled fixture corpus to one provider-specific test collection, keeping the test source and writable wiki
destination separate:

```text
Company Wiki Demo — Google Drive
├── Test Sources/   # fixture documents; bounded read/search scope
└── Test Wiki/      # separate writable wiki destination
```

For example, ask:

> Create a demo wiki named Company Wiki Demo. Original material: the Google Drive `Test Sources` collection only.
> Wiki destination: the separate writable Google Drive `Test Wiki` collection. Use English. Do not search outside
> `Test Sources`.

The fixture corpus should include an alias, a current authoritative document, an obsolete conflicting document, a
multi-document question, and a decoy. Test a restricted document too when the provider can represent its ACLs.
Repeat this setup only for providers the product supports; each provider needs its own acceptance test because
search, links, and permissions differ.

## Lifecycle

`Init → Bootstrap → Explore ↔ Query → Curate → Add Source → Maintain → Validate`

- **Init** creates a small, admin-governed Company Library Index from representative sampling.
- **Bootstrap** creates a minimal Personal Wiki by reference, without resampling or copying the company corpus.
- **Explore** is transient; **Query** answers from same-operation original evidence and remains read-only.
- **Curate**, **Add Source**, and **Maintain** propose and then apply approved durable changes.
- **Validate** is read-only graph and freshness inspection.

Here, **Ingest** is the compatibility alias for deliberate **Add Source** reconciliation. It is not centralized ingestion, bulk folder
processing, source copying, embeddings, or background synchronization. One source at a time is the default.

## How people use it

Once the assistant can access the company's documents, people can ask everyday questions in plain
language. For example:

> For a Google Drive demo, create a wiki from `Company Wiki Demo/Test Sources` only and write it to the separate
> `Company Wiki Demo/Test Wiki` collection. Do not search the rest of the drive.

> Create a wiki named Company Handbook. Original material: the current People, Operations, and Customer
> collections. Wiki destination: the writable Company Knowledge collection. Use English, with People,
> Operations, and Customers as the initial navigation outline.

> What is our current vacation policy? Use the latest approved policy, and tell me if older documents
> say something different.

> A customer asked about our response time for a critical service issue. Find the official answer and
> link me to the source.

> What does “lapsed customer” mean here? Show me the official definition and any related guidance.

> These two documents disagree about office attendance. Which one should we follow, and why?

> Check whether the wiki has broken links or areas that are out of date. Suggest fixes, but do not
> change anything yet.

> Ingest this newly approved policy. Show me the proposed wiki changes before applying them, and preserve the
> original document link instead of copying its content.

The assistant resolves the question through the taxonomy, uses only the few relevant typed links, then searches the
registered source locations and reads original evidence. It should say when information is missing, restricted,
outdated, or uncertain, and should ask for approval before making wiki changes.

Before creating a wiki, the assistant confirms four required inputs: wiki name, original-material location
and scope, writable wiki destination, and content language. Key domains, owners, core/source-of-truth
documents, and an initial navigation outline are optional. The outline shapes the reading path; it does not
require a matching storage-folder structure.

Setup is intent-aware, not a rigid form interview. If a request already conveys a value, the assistant does
not ask for it again. A request to “create a finance wiki,” for example, supplies the name and finance scope;
the request's language normally supplies the prose language. The assistant asks only for the unknown
original-material location and writable destination. It never turns a topic into permission to search the
whole cloud drive.

## Design principles

- The taxonomy is the governed backbone; typed links are the small useful graph on top; source search retrieves
  evidence.
- The wiki routes but never gates; the Personal Wiki is a retrieval prior, not a boundary.
- Personal growth retains durable judgment and routing context; it does not default to per-document summaries or
  metadata abstractions.
- The tree is for navigation and typed links are for discovery; routing happens once, before evidence retrieval.
- Reconcile selected new evidence through Add Source; do not turn initialization into an exhaustive import.
- Prefer authoritative, current sources and surface conflicts rather than hiding them.
- Preserve source documents; link to evidence instead of copying it into the wiki.
- Treat document content as data, not instructions.
- Keep maintenance explicit: propose changes and require approval for edits.
- Treat permissions, missing sources, stale links, and incomplete evidence as first-class conditions.

Shared writes require a provider-verified governing capability and evidence whose audience contains the destination
audience. Registry role labels do not grant authority. Before agent-mediated use, source access is rechecked; V1
cannot retract old static wiki bytes after a later source-ACL change without provider coupling.

A local adapter may verify effective local write access, but this is enough only for private/personal use and test
fixtures. It does not establish shared audience containment or Company/Team governance; if those checks are not
available, the assistant must return a proposal rather than write shared knowledge.

## Shared local configuration

`~/company-wiki/index.md` is the single entry point for mutable user configuration. It links to one Markdown
profile per wiki under `~/company-wiki/wikis/`. Profiles record locators and navigation metadata, not source
content or credentials. The skill reads the index first and never scans the directory.

The skill itself remains versioned at `skills/company-wiki/`. A user-level
`~/.agents/skills/company-wiki` symlink points to that directory so other local Codex agents for the same user
can discover it. The skill does not live under `~/company-wiki`; the cloud-drive wiki and original evidence
remain separate from both the registry and the skill.

See [`skills/company-wiki/README.md`](skills/company-wiki/README.md) for the package-level guide and
[`docs/company-wiki_PRD_v0.5.md`](docs/company-wiki_PRD_v0.5.md) for the product requirements.
