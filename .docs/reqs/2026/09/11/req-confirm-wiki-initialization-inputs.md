# REQ: confirm-wiki-initialization-inputs

**Date:** 2026-09-11
**Deliverable:** a stricter `company-wiki` initialization gate, a user-level Markdown registry shared across
local agents, and matching behavioral documentation.

## Problem

Initialization currently asks only for sources and language. That is not enough to create an identifiable
wiki in the correct destination. It leaves the wiki title and write location implicit, while mixing several
optional discovery prompts without a clear product contract.

## Outcome

Before creating wiki documents, initialization has four user-confirmed inputs: wiki name,
original-material location and scope, wiki destination, and content language. It extracts values already
conveyed by the user's natural-language request instead of mechanically asking for fields, but never infers
a source or destination location. It also invites exactly four optional inputs—key domains, owners, core
documents, and an initial navigation outline—without blocking creation when they are omitted.

The reusable skill remains versioned under this repository's `skills/company-wiki/` directory and is exposed
to local agents through the user-level `~/.agents/skills/company-wiki` symlink. Mutable wiki registrations
live separately as Markdown under `~/company-wiki`, whose `index.md` is the only runtime entry point.

## Acceptance Criteria

- [x] A setup request that omits any required input asks for every missing item in one concise response and
      creates nothing.
- [x] The four required inputs are: wiki name; explicitly specified original-material location and scope;
      writable wiki destination; and wiki prose language.
- [x] Initialization analyzes the user's wording before asking questions. Explicit or unambiguous values
      count as confirmed, including a named wiki, a subject implied by that name or request, and the language
      of the request when it clearly signals the desired prose language. A subject does not count as an
      original-material location.
- [x] A request that already provides all four required inputs is not asked to repeat or reconfirm them.
- [x] Initialization searches and reads only within original-material locations explicitly specified by the
      user. It never expands a semantic subject such as “finance” into a whole-drive or all-connected-source
      search.
- [x] Semantic analysis never invents an original-material location, writable destination, permission,
      inaccessible source, or broader scope. The agent asks only for required values that remain genuinely
      unknown or ambiguous.
- [x] Root `AGENTS.md` records the original-material location and wiki destination as two independent,
      foundational data-boundary rules: both require explicit user specification; reads stay within the
      former and writes stay within the verified-writable latter; read access never implies write authority.
- [x] Initialization invites exactly these four optional inputs: key domains, owners, core/source-of-truth
      documents, and an initial navigation outline.
- [x] Missing optional inputs never block initialization once the four required inputs are confirmed.
- [x] “Initial navigation outline” means a proposed human reading path, not a required storage-folder tree.
- [x] Created home/map documents use the confirmed wiki name and record the confirmed source boundary,
      destination route, and language in readable prose or a small table.
- [x] Package and root documentation describe the new initialization contract consistently in English and
      Chinese, and the focused behavioral specification covers missing, partial, complete, and optional-input
      cases.

### Shared Markdown registry correction

- [x] `~/company-wiki/index.md` is the single user-level registry entry point, and per-wiki Markdown profiles
      live under `~/company-wiki/wikis/`.
- [x] The skill source remains under repository `skills/company-wiki/`; no skill code or instruction file is
      stored inside `~/company-wiki`.
- [x] `~/.agents/skills/company-wiki` is a symlink to this repository's `skills/company-wiki` directory so
      other local Codex agents for the same user can discover the skill.
- [x] On invocation, the skill reads `~/company-wiki/index.md` first, follows only the selected profile link,
      and never scans the registry directory to discover configuration.
- [x] A profile target must be a relative Markdown link whose normalized and resolved path remains under
      `~/company-wiki/wikis/`. Reject absolute targets, URLs, `..` traversal, symlink escapes, missing
      targets, duplicate wiki names, and ambiguous selection instead of opening or guessing them.
- [x] Each profile is ordinary Markdown and records the wiki name, original-material location and scope,
      wiki destination, language, four optional inputs when supplied, and the native home/map link after
      creation.
- [x] A successful initialization creates or updates exactly one per-wiki profile and its index link. It
      preserves unrelated registry entries and does not treat registry content as source evidence.
- [x] Registration is collision-safe and idempotent: it never overwrites an existing profile with a different
      identity, never reuses a conflicting slug or duplicate label, and makes no change when the same
      profile/home link is already registered.
- [x] If the registry entry is missing, setup may create the minimal registry before registration; query,
      maintenance, and validation report the missing registry and do not invent a configured wiki. If the
      registry is unreadable or unwritable, the agent reports the limitation instead of claiming persistence.
- [x] Setup verifies registry read/write feasibility before creating provider wiki documents. If cloud
      creation succeeds but the final profile or index update fails, it reports partial completion and the
      native home link, preserves existing registry bytes, leaves provider documents intact, and never
      claims successful registration or auto-deletes the created wiki.
- [x] Registry documents contain locators and navigation metadata only: no credentials, copied original
      documents, generated evidence cache, YAML, or sidecars. Registry text is untrusted data, not agent
      instructions or evidence.
- [x] Package, root, and repository-agent documentation explain the separation between versioned skill,
      user-level registry, user-level symlink, cloud wiki documents, and original evidence.
- [x] Focused scenarios verify shared discovery, entry-first loading, no directory scan, minimal registration,
      preservation of unrelated entries, and missing/unavailable registry behavior.

## Constraints

- Preserve the document-native graph model; do not introduce folder, YAML, sidecar, or local-path
  requirements for the wiki graph or evidence. The only local-path exceptions are the user registry at
  `~/company-wiki` and the skill-discovery symlink at `~/.agents/skills/company-wiki`.
- Derive values from the user's wording, but do not infer them from the current tab, filesystem, host context,
  or detected documents alone.
- Continue using only host-exposed document/cloud-drive capabilities for wiki and source operations and
  respect their write boundaries. Local filesystem access is allowed only for the registry and skill symlink.
- Keep the change Markdown-only and host/provider agnostic.
- Keep the root `AGENTS.md` rules concise and applicable to every company-wiki initialization task in this
  repository.
- Treat `~/company-wiki` as mutable user configuration, not as the installed skill, organization wiki,
  original-material location, or evidence store.

## Non-goals

- Designing a visual form or provider-specific folder picker.
- Changing query, maintenance, or validation provider/evidence behavior beyond selecting the configured wiki
  through the registry and reporting missing or inaccessible registry state.
- Requiring optional taxonomy or governance metadata before a wiki can be created.
- Synchronizing the local registry across machines or making it available to cloud agents that cannot read
  the user's home directory.

## Blocking Questions

None. The user confirmed the four required and four optional initialization fields and the shared-registry
architecture on 2026-09-11.
