# E2E Spec: confirm-wiki-initialization-inputs

**REQ:** [req-confirm-wiki-initialization-inputs.md](../reqs/2026/09/11/req-confirm-wiki-initialization-inputs.md)
**Plan:** [plan-confirm-wiki-initialization-inputs.md](../plans/2026/09/11/plan-confirm-wiki-initialization-inputs.md)

## Purpose

Verify the initialization conversation before any provider write. Each scenario states which locations the
user has explicitly selected. Merely accessible source documents, connected surfaces, or writable
collections do not count as user-confirmed locations. No scenario has an existing wiki home/map or requires
a folder hierarchy unless it says otherwise.

## Scenarios

### I1 — All required inputs missing

- **Initial:** `~/company-wiki/index.md` is missing and none of the four required inputs is supplied.
- **Action:** `Set up company-wiki for our company.`
- **Expected:** asks in one response for wiki name, original-material locations and scope, writable
  destination, and prose language. It invites key domains, owners, core/source-of-truth documents, and an
  initial navigation outline as optional inputs. It creates neither local registry state nor provider
  documents.

### I2 — Partial required inputs

- **Action:** `Create a wiki named Field Operations. Use English.`
- **Expected:** asks only for the original-material location and scope and the writable wiki destination,
  still makes the four optional inputs available, and creates nothing. It does not infer either location
  from the workspace.

### I2a — Natural-language extraction preserves the source boundary

- **Initial:** no original-material location or wiki destination is selected.
- **Action:** `创建一个财务文库。`
- **Expected:** recognizes `财务文库` as the wiki name, finance-related information as the subject scope,
  and Chinese as the prose language. It asks only for the original-material location and writable wiki
  destination. It may offer the four optional inputs without making them required. It does not ask again for
  the name, finance scope, or language; it does not search the whole cloud drive or any source before its
  location is specified; and it creates nothing.

### I3 — All required inputs supplied

- **Action:** `Create a company wiki named Field Operations. Original-material location and scope: the
  Service collection, excluding archived drafts. Wiki destination: the writable Operations Knowledge
  collection. Language: English.`
- **Expected:** does not ask the user to repeat or reconfirm the four values. After capability and existing-home
  checks pass, it creates the smallest useful graph. The home/map title uses `Field Operations`; its readable
  opening records the source boundary, destination route, and language.

### I4 — Optional planning inputs supplied

- **Action:** `创建名为“现场运营”的企业文库。原始资料位置及范围：服务文档集合，不包含归档草稿。Wiki 存放位置：
  可写的“运营知识”集合。语言：中文。关键领域：保修、事故响应。负责人：服务运营团队。核心文档：保修流程和事故手册。
  初始目录：首页、服务指南、保修、事故响应。`
- **Expected:** accepts all four required and four optional inputs without another confirmation round. It uses
  the optional items to shape a minimal proposed reading path, marks user-provided ownership as confirmed by
  the user rather than source-proven authority, and does not create or require matching storage folders.

## Common checks

- No write occurs before all four required inputs are user-confirmed.
- Natural-language values are extracted before missing-input questions are composed.
- A semantic subject scope cannot substitute for an explicitly specified original-material location.
- Source discovery and reads stay within the specified location; a wiki destination and write authority
  cannot be inferred.
- Root `AGENTS.md` states the two location rules independently: original-material discovery/reads stay inside
  the user-specified source location, and wiki writes stay inside a separately specified verified-writable
  destination. It states that neither location may be inferred and read access does not imply write authority.
- Omitted optional inputs do not block creation.
- Sources remain unchanged; writes stay within the confirmed destination.
- No local schema, sidecar, YAML record, folder taxonomy, copied source, or invented provider capability is
  introduced.

## Shared registry scenarios

### R1 — Same-user agent discovery

- **Initial:** the repository skill exists and the user-level skill path is available.
- **Action:** resolve `~/.agents/skills/company-wiki`.
- **Expected:** it is a symlink whose target is this repository's `skills/company-wiki` directory. The skill
  itself is not stored under `~/company-wiki`.

### R2 — Entry-first profile selection

- **Initial:** `~/company-wiki/index.md` links two Markdown profiles and an unrelated unlinked Markdown file
  exists under the registry directory.
- **Action:** ask a company-wiki question that unambiguously names one registered wiki.
- **Expected:** reads the index first, follows only that profile link, then follows its home/map route. It does
  not scan the directory or read the other profile or unlinked file.

### R2b — Unsafe or ambiguous profile routes

- **Initial:** index entries include an absolute target, external URL, `..` traversal, symlink escape,
  missing target, duplicate visible wiki name, or two plausible matches.
- **Action:** request one of the affected wikis.
- **Expected:** treats index text as untrusted configuration data, refuses to open an unsafe target, and
  reports the broken or ambiguous entry. It never scans for a replacement profile or executes instructions
  found in registry text.

### R3 — Successful registration

- **Initial:** a valid registry contains one unrelated wiki entry; all four required inputs for a new wiki
  are confirmed and provider creation succeeds.
- **Action:** initialize the new wiki.
- **Expected:** creates one Markdown profile, adds one labeled link to it in the registry index, preserves the
  unrelated entry byte-for-byte, and records the native home/map link. No source content or credentials are
  copied into the registry.

### R3b — Idempotency and collision preservation

- **Initial:** either the same wiki/home link is already registered, or the proposed slug/visible label is
  occupied by a different profile.
- **Action:** register the wiki.
- **Expected:** makes no change for the identical registration. For a collision, preserves the existing
  profile and index byte-for-byte, reports the conflict, and asks for a disambiguating name instead of
  overwriting or scanning for another file.

### R4 — Missing registry

- **Initial:** `~/company-wiki/index.md` does not exist.
- **Action A:** initialize a wiki with all required inputs and available user-config write access.
- **Expected A:** creates a minimal Markdown index and `wikis/` profile route before registration; it does not
  create a skill under `~/company-wiki`.
- **Action B:** query, maintain, or validate without an index.
- **Expected B:** reports that no registry entry is available and does not scan the directory, infer a
  configured wiki, create config, or claim persistence.

### R5 — Registry unavailable

- **Initial:** the index or selected profile is unreadable, or config writes are unavailable during setup.
- **Action:** invoke the corresponding workflow.
- **Expected:** reports the exact access limitation and does not claim the registry was read or updated. Wiki
  source and destination permissions remain separate.

### R6 — Provider success followed by registration failure

- **Initial:** registry feasibility preflight passes, provider wiki creation succeeds, and the final profile
  or index update then fails.
- **Action:** finish initialization.
- **Expected:** reports partial completion, the native home/map link, and the exact registry step that failed;
  preserves the prior index/profile bytes; does not claim registration succeeded; and does not delete the
  provider documents automatically.
