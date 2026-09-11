# Plan: company-wiki personal knowledge lifecycle

**REQ:** [req-company-wiki-lifecycle.md](../../../../reqs/2026/09/11/req-company-wiki-lifecycle.md)
**E2E:** [test-company-wiki-lifecycle.md](../../../../tests/test-company-wiki-lifecycle.md)
**Requirements source:**
[company-wiki-personal-wiki-requirements-v0.3.md](../../../../../docs/company-wiki-personal-wiki-requirements-v0.3.md)

## Outcome and boundaries

Replace the single-wiki `Init → Ingest → Query → Maintain → Validate` contract with layered ownership scopes
and the lifecycle `Init → Bootstrap → Explore ↔ Query → Curate → Maintain → Validate`, plus optional bounded
`Add Source` (with `Ingest` as a compatibility alias). Every durable write goes through one shared change
protocol that verifies provider-authenticated authority and audience containment. Retrieval follows the
REQ's five principles:
- the wiki routes but never gates;
- the Personal Wiki is a prior, not a boundary;
- trees navigate while graphs discover;
- original documents prove;
- routing is one phase.

This remains a provider-neutral skill, documentation, and test-harness change. It adds no runtime service,
database, index, connector, cache, background process, or registry migration. Existing profiles keep working as
legacy combined wikis. Team Wiki is a representable scope handled by the generic scope and change rules; no
Team-specific workflow or Team E2E execution is in scope.

## Story state

- Git base remains `00e3cac`. Story commits `0c9791b` and `f4d249d` implemented the superseded five-operation
  REQ. Their test adapter, transcript guard, probe runner, fixtures, and change-control semantics are reused;
  their lifecycle naming and single-wiki model are replaced. Commit `9468448` belongs to the
  `confirm-wiki-initialization-inputs` story and is outside this story.
- In scope at entry, uncommitted: the CR round 1–4 harness repairs under `tests/company-wiki-skill/adapter/`,
  the rewritten REQ, the untracked requirements source v0.3, the PRD v0.4 → v0.5 rename and rewrite, and the
  README PRD links. `docs/deep-research-report.md` is unrelated concurrent research and stays out of story commits. Other
  agents share this index, so story commits use explicit pathspecs.
- The earlier AR pass and CR loop are void because the REQ changed materially. The earlier probe evidence under
  `/private/tmp/company-wiki-lifecycle-probe10.VLHHxA/evidence/` proves single-turn, single-principal harness
  isolation only.

## Consequential decisions

1. **Scoped profiles.** A scoped registry profile states its scope (`company-index`, `team`, or `personal`),
   governing destination, and governing-capability route: the host-exposed permission check for that exact
   destination. Profile text records locators and expected owners only; the agent verifies identity,
   write capability, and governance capability through the provider on every durable change. A Personal
   profile may hold one contained relative link to its Company Library Index profile, and cross-scope work
   follows only that edge. Promotion additionally requires the user to name the exact destination profile.
2. **Legacy profiles.** A profile without a scope or governing-capability route is a legacy combined wiki. It
   supports Query and Validate, plus same-destination Maintain and Add Source when the provider verifies
   current-user write capability. It cannot authorize Bootstrap, shared canonical writes, promotion, or inferred
   ownership. An upgrade writes a new scoped profile from explicit scope, destination, and authority inputs and
   repoints the index link only after that write succeeds. The legacy profile file is never deleted. Standalone Curate is not available on a legacy profile. A legacy
   home without a routing outline is routed from the guides it names, plus direct source search.
3. **Setup routing.** A setup request that does not ask for a personal wiki remains company-index Init, so the
   existing four-input gate (S0–S1b) is preserved. Bootstrap runs only on an explicit personal-wiki request. It
   requires an explicitly selected Company Library Index and a separate writable personal destination. It takes
   the index either as a registered profile or as an exact native index-home locator; with a locator, it also
   registers a read-only company-index profile. Missing name or language values follow Init's extraction rules.
   Bootstrap treats the supplied index-home locator as an opaque reference: it does not read the index body,
   adopt its declared source boundary, or copy any derived route into either profile. If the Bootstrap request
   separately names an exact source location, the profile may record that locator verbatim without reading it;
   otherwise broad direct-source search remains unavailable until the user supplies one. Wiki text and setup
   approval never confer source-location authority. A raw locator that resolves to a legacy home still
   yields only a read-only index profile, and every write stays provider-verified.
4. **One durable-change protocol.** A new `references/change-protocol.md` is loaded by Init, Bootstrap, Curate,
   Add Source, Maintain, and promotion. It owns the following:
   - scope, target, and evidence proposal;
   - verification of authority and audience;
   - approval bound to principal, scope, targets, evidence versions, audience result, and proposal;
   - apply-time reread plus link, ACL, audience, and destination preflight;
   - stale-plan invalidation;
   - ordered writes that stop on the first failure;
   - current-state verification and a recovery proposal limited to the remaining work;
   - non-atomic provider-then-registry registration for setup.

   Because Init and Bootstrap generate content, both become proposal-then-approval flows. V1 defines no
   auto-apply safe-action policy and no correction shortcut. Every durable write, including a user
   correction, is proposed with its exact targets and then approved. Main-spec S4 therefore becomes two turns.
5. **Audience containment for every destination.** Source-derived knowledge is written only when the provider
   verifies two things: the writer's capability on the exact destination (governance for Team and Company
   scopes), and that the destination audience is a subset of every underlying source audience. If either fact
   is unavailable, the result is a draft or proposal and nothing is written.
   - A private Personal destination passes for any source that user can read.
   - A broader or unknown personal audience is treated as a shared audience.
   - Sanitization follows the REQ rule exactly.
   - Static Markdown cannot propagate a later source-ACL revocation without provider ACL coupling or background
     synchronization, both outside V1. Before every agent-mediated use in Bootstrap, Explore, Query, Curate, Add
     Source, Maintain, Validate, or promotion, the agent rechecks current evidence access/audience and fails closed when
     unavailable. Direct native file access remains governed by the destination ACL; documentation and reports
     state this limitation. `SKILL.md` owns this shared rule and every workflow reference inherits it.
     Bootstrap satisfies the rule by persisting only the exact user-supplied index-home locator under the generic
     label `Company Library Index`; it does not read, copy, summarize, or surface derived index routes. Query or
     Explore may expose a route only after current evidence checks.
6. **Permission-aware index without a parallel ACL system.** Each index document carries only material whose
   audience contains the document's audience, and native ACLs control reading.
   - A broader-audience document never names, links, aliases, summarizes, or relates to narrower-audience
     knowledge.
   - Responses reveal only what the provider exposes to the current principal. A title that is visible
     without read permission may be named. A hidden target is indistinguishable from an absent one.
7. **Workflow files.**
   - `SKILL.md` routes the operations.
   - `init.md` covers company-index Init.
   - New files: `bootstrap.md` (Personal Wiki), `curate.md` (curation and cross-scope promotion), and
     `change-protocol.md`.
   - Explore joins `query.md`: both are read-only and share one progressive loop, so routing separates them
     by intent.
   - `ingest.md` is renamed with `git mv` to `add-source.md`. `SKILL.md` maps `Ingest` requests to it as an
     alias.
   - `maintain.md`, `validate.md`, `registry.md`, and `document-format.md` are updated in place.
8. **Bounds.** Defaults per operation: wiki traversal depth 3, source search/list rounds 2, source documents
   opened 5, and 40,000 retrieved UTF-8 characters. When reliable token usage is exposed, a request or profile
   may set a token bound instead. Source metadata exposes content size so the agent can avoid a read that would
   exceed the remaining budget. A profile or request may set lower finite values. When a bound is exhausted, the
   agent stops, reports what remains unverified, and asks. Only the user's reply to that report expands a bound,
   and only for the current operation.
   - Init sampling, Add Source folders, and Validate drift checks obey the same limits.
   - Wiki enumeration during Validate is a listing, not traversal. Title listings do not count as opened
     documents.
   - In the test adapter, `list` stands in for native source search and counts as one search/list round.
   - A `metadata` call does not count as an opened document. Drift checks compare metadata digests with recorded
     versions.
   - Wiki traversal depth is derived from the event log:
     - the selected scope's home is depth 0;
     - the index home reached through the named edge is depth 1;
     - any other wiki read is 1 plus the depth of an already-read page that links to it.

     So personal home → index home → routing page → named node is depth 3. Validate reads of pages returned
     by a wiki `list`, and apply-time target rereads, are enumeration or verification and do not count toward
     depth.
   - Metadata sizes and read character counts use one unit: Unicode code points.
   - An operation is one user turn, and each turn's event log is the scoring unit.
   - The change protocol's apply-time reread covers only the approved evidence and targets. It counts against
     the apply turn's budget, which the approved plan already fits, and it never widens scope.
   - The character budget covers original-source content only. Wiki pages are routing context, so they count
     toward traversal depth but not toward the character budget.
9. **Provenance and freshness as readable Markdown.** V1 writes provenance near each substantive claim as
   readable signals: native source target, section, version when exposed, checked date, relationship,
   verification state, and origin (source text, agent-generated, human-authored, or verified company
   definition).
   - Front matter and `.wiki/` state are not used, which preserves the no-YAML/no-state checks.
   - Freshness states are `current`, `potentially stale`, `superseded`, and `needs review`.
   - Query and Validate report staleness read-only. State changes go through Maintain or Curate.
   - Removal and merge are document-native, and no file is deleted; native deletion stays with the user.
     - Removing a node unlinks it from the home tree and outline and rewrites it as a `Retired` stub.
     - Merging moves the approved content into the kept node and rewrites the merged-away page as a
       `Merged into` stub that links the kept node.
10. **Test identity model.** The deterministic adapter models the following:
    - authenticated principals;
    - multiple wiki roots;
    - per-principal hidden, metadata-only, and readable source access;
    - per-root write and governance capability;
    - target audiences;
    - content-digest versions and exposed content size;
    - explicit unavailable identity, capability, and audience results.

    Two principals, `admin` and `reader`, each get their own home and registry. Multi-turn scenarios use
    `codex exec resume`. The harness may change adapter configuration only between turns; each turn records a
    new baseline, and the guard pins that baseline.
11. **Retrieval model.**
    - **Router, not gate.** Missing or partial wiki coverage never blocks or narrows retrieval inside the
      registered source scope, and direct search within that scope is always available.
    - **Prior, not boundary.** The Personal Wiki ranks starting routes. It does not limit what may be searched.
    - **Tree and graph.** Each scope has a navigation tree, in which every node has one primary parent route
      from its home/map. It also has a discovery graph of cross-links, aliases, backlinks, and optional typed
      relationships, which Explore follows across branches and scopes.
    - **Proof.** Every factual answer claim cites an original document read in the same operation.
    - **One routing phase.** Each scope home carries a compact routing outline: node titles, aliases, one-line
      scope, source entry points, and each node's cross-branch and cross-scope edges in compact form (label and
      target). Graph discovery therefore happens inside the routing decision. A direct-source bypass is a
      routing decision that reads no wiki page.
      - The agent reads the personal home and, through its named edge, the index home together. When an
        outline outgrows one document, it also reads at most 3 pages per scope that the home declares as
        routing pages.
      - It chooses nodes, sources, and direct searches in one decision, then retrieves evidence. It does not
        hop home → guide → detail to find evidence.
      - Evidence retrieval may iterate inside those routes and the registered source scope, but the operation
        never returns to wiki routing or invokes a second route-selection phase. An unusable route is reported;
        a materially new route starts a new Query or Explore operation.
    - Init, Bootstrap, Curate, and Maintain keep the routing outline current within the same approved change.
      Validate checks that the outline and the tree agree.
    - The sequential flows in the requirements source (§7.2, §7.3, §12.1, §15) and in PRD §12, §18, and §22.8
      are read as the ranking order inside one routing decision, not as sequential hops.
12. **Git sources in the main spec.** The model never invokes Git directly. The adapter exposes configured
    `source:repo/...` targets through the same list, metadata, read, audience, and size-accounting boundary as
    drive sources, plus `history` and immutable `source-version:repo/<full-commit>/<path>` reads. `history`
    returns metadata only (full commit id, date, subject, and tags reachable from the allowed ref that point
    at the commit), never patches, and has a fixed 20-result maximum that
    counts as one search round. Each repository source config names one exact allowed ref. History and version
    reads accept only commits reachable from that ref; version reads additionally require a full commit id
    returned by bounded history for the contained path. The adapter internally invokes Git with fixed argument
    arrays, disables pager, external diff, and text conversion, validates ref reachability, the full commit id,
    and contained path, and returns output through the same character budget. The transcript guard rejects every
    model-issued direct `git` command.
    S1 and S3 Git expectations use these adapter operations. Lifecycle scenarios still register only the drive
    source.
13. **Harness write channels.**
    - The adapter's `write` takes `--content-file <path>` from a harness staging directory. That directory is
      inside the workspace but outside every source, wiki, and registry root. The adapter logs a digest of the
      content, and the guard accepts exactly that token shape.
    - The agent writes staging files and registry profiles with the host's file-change tool. The guard allows
      file changes only under the staging directory and the registry, and still rejects any file change that
      touches a source or wiki root.
    - On disk, the wiki roots use neutral names (`<ws>/store-a/`, `<ws>/store-b/`) that match no logical name
      or profile filename.

## Tasks

- [ ] Extend `tests/company-wiki-skill/adapter/provider_adapter.py` with a configured principal and `whoami`.
      Add named wiki roots, folder-scoped `list`, `metadata` with digest versions, `capability`, and
      `audience`; metadata also exposes content size. Enforce per-principal hidden, metadata-only, and readable
      access; a hidden target returns the same not-found result as an absent one. Enforce write capability in
      `preflight` and `write`, with an `unavailable` fault for identity, capability, and audience. Log principal,
      operation, target, result, and (for reads) the returned character count for every event. Resolve roots
      per target, so a missing repository root makes only `source:repo` targets `unavailable` (main-spec S7).
      Add the harness-only `lock_registry_after_write: N` fault, which makes the registry `wikis/` directory
      read-only right after the Nth successful write. Report sizes and character counts in Unicode code points. Extend `guard_codex_jsonl.py`'s operation allowlist and event
      correlation to the new operations. Add configured audience, size, `history`, and immutable
      `source-version:` reads for repository targets using fixed internal Git argv, one configured allowed ref,
      reachable-commit and returned-history checks, and a 20-result history cap; reject path/ref/option injection,
      unreachable commits, unreturned versions, and every model-issued direct Git command (decision 12). Add the
      decision-13 write channel:
      `write --content-file`, limited to
      the staging directory and logged with a digest, plus guard rules that allow file changes only under the
      staging directory and the registry. The guard must also reject shell writes (redirects, `tee`, `cp`,
      `mv`) into either directory. History records include tags pointing at each returned commit. Add
      two-principal unit coverage to `test_adapter.py`.
- [ ] Extend `probe_codex_adapter.py` with multi-turn `codex exec resume`. Per turn, it needs:
      - a disposable auth copy that is removed on `thread.started`;
      - a per-principal HOME and CODEX_HOME;
      - a new config baseline after any harness-only change between turns;
      - a separate adapter event log, so guard correlation and `fail_write_number` apply per turn;
      - event logs stored beside the config, outside every path the model can write;
      - turn 1 without `--ephemeral`, and the sandbox set through `-c`, because `resume` has no `--sandbox` or
        `--cd`;
      - the process working directory set to the workspace for every turn;
      - a guard run.
- [ ] Probe the harness before any product change. Pass only if all of these hold:
      - a two-turn resumed session emits complete JSONL for both turns;
      - turn 2 reports the same thread id as turn 1 and repeats a nonce given only in turn 1;
      - in turn 2, the configured sandbox denies config mutation through both absolute and relative paths, and
        an adapter write succeeds;
      - a content-file write stores exactly the staged bytes;
      - a registry profile containing `wiki:` locators, written with the file-change tool, passes the guard;
      - the resumed turn's working directory is the workspace;
      - auth is removed before model commands in each turn;
      - a harness config transition between turns passes the next turn's guard;
      - a model-side mutation of the config still fails;
      - a model-side write to an adapter event log fails;
      - `whoami`, `capability`, and `audience` differ correctly between `admin` and `reader`;
      - when only the adapter principal changes across a resume, with HOME and CODEX_HOME unchanged, `whoami`
        reflects the switch;
      - a file-change write into a registry `wikis/` directory made read-only between turns fails without
        leaving partial bytes;
      - with `lock_registry_after_write: 1`, an adapter write succeeds and the next registry file change in
        the same turn fails;
      - unavailable `whoami`, unavailable `capability`, and unavailable `audience` each fail closed with no write;
      - bounded repository history and one returned reachable version read pass, while direct Git, an unreachable
        commit, an unreturned commit, and a path escape fail;
      - a hidden target is indistinguishable from an absent one;
      - all protected checksums match.

      If any condition fails, stop dependent work, update story artifacts, and return to AR.
- [ ] Rewrite `skills/company-wiki/references/registry.md` for:
      - the scoped profile fields and the single Personal → Index edge;
      - Bootstrap storing only the opaque index-home locator and leaving direct-source search unavailable until
        the user separately supplies an exact source location;
      - exact destination-profile selection for promotion;
      - legacy capabilities and upgrade;
      - bounds configuration;
      - per-operation missing-registry fallbacks for Bootstrap, Explore, Curate, and Add Source;
      - the rule that registry text never grants authority.
- [ ] Add `skills/company-wiki/references/change-protocol.md`. It implements decisions 4–6 and decision 8's
      per-turn bound accounting for apply-time rereads.
- [ ] Rewrite `skills/company-wiki/SKILL.md`. It should cover:
      - the frontmatter description;
      - layers and roles;
      - the lifecycle and the disclosure levels (personal entry, shared index, focused node, evidence), used as
        a ranking order inside one routing decision rather than as sequential hops;
      - default bounds;
      - non-disclosure and audience rules;
      - the routing and loading table, with `change-protocol.md` loaded by every writing workflow;
      - the `Ingest` alias.
- [ ] Update `references/init.md` for company-index Init:
      - keep the four-input gate and bounded sampling;
      - verify governance and audience;
      - build a topic map rather than a file catalog;
      - exclude narrower-audience material;
      - propose before creating;
      - register a scoped profile.
- [ ] Add `references/bootstrap.md` for Personal Wiki bootstrap by reference:
      - no source reads;
      - no copied index pages;
      - a minimal personal structure containing only one opaque, user-supplied Company Library Index home link—
        no surfaced child routes—plus readable sections for pinned, temporary, personally canonical, and
        do-not-curate/stop-learning topics;
      - verbatim registration of a separately user-supplied exact source locator when present, and an explicit
        broad-direct-search-unavailable state when absent;
      - index-unavailable and legacy-profile refusals, plus the direct-source Query offer;
      - non-atomic registration of the personal profile and, when needed, a read-only index profile.
- [ ] Rewrite `references/query.md` so one reference covers Explore and Query:
      - one routing phase over the Personal Wiki (the prior) and the index routing context, including
        discovery-graph edges exposed there;
      - then bounded retrieval through likely source areas, native search, and sections, without returning to
        wiki routing;
      - Explore stays transient;
      - Query is the primary path;
      - the five direct-source bypass triggers;
      - no Add Source prerequisite;
      - bound exhaustion;
      - lazy staleness reporting;
      - Curate suggestions only, never writes.
- [ ] Add `references/curate.md` for:
      - the curation criteria;
      - the pre-change disclosure (scope, pages, evidence, conflicts, edits, preserved organization);
      - preferring small navigation knowledge;
      - honoring and updating pinned, temporary, personally canonical, and do-not-curate controls;
      - referencing shared nodes rather than copying them;
      - Personal → Team → Company promotion with reconciliation, provenance, and destination authority.
- [ ] `git mv references/ingest.md references/add-source.md` and rewrite it for:
      - explicit documents or one finite folder, with the folder enumerated and bounded before reads;
      - comparison against the Personal Wiki and the visible index;
      - handoff to Curate through the change protocol;
      - reporting of selected, changed, unchanged, skipped, unsupported, conflicting, and inaccessible
        material;
      - unchanged-evidence no-op;
      - the `Ingest` alias wording.
- [ ] Update `references/maintain.md`:
      - scope-aware authority;
      - merge, rename, hierarchy, relationship repair, summary refresh, source replacement, archive, and retire;
      - preserving user-authored organization;
      - add/remove/rename/merge/pin/mark/unmark controls and the do-not-curate list;
      - document-native removal and merge through `Retired` and `Merged into` stubs (decision 9);
      - freshness-state changes;
      - removal of the correction-is-approval shortcut, so corrections are proposed and then approved;
      - no Add Source work.
- [ ] Update `references/validate.md`:
      - independent enumeration per scope;
      - checks for provenance, freshness, duplicates and aliases, suspicious relationships, permission leakage,
        superseded knowledge, and gaps;
      - drift reads within bounds;
      - read-only by default, with repairs routed to Maintain or Curate.
- [ ] Update `references/document-format.md`:
      - scope labels and layered disclosure levels;
      - aliases resolving to canonical nodes;
      - optional typed relationships;
      - provenance and origin signals;
      - freshness states;
      - `Retired` and `Merged into` stubs;
      - separately cited conflicts;
      - Personal home sections for pins, temporary nodes, personal canonical status, and do-not-curate topics;
      - the scoped validation checklist.
- [ ] Apply decision 11 in every affected file:
      - `SKILL.md` operating rules and `references/query.md` get the router, prior, proof, and
        one-routing-phase rules, plus graph-based Explore;
      - `references/document-format.md` gets the routing outline (including each node's compact cross-branch and
        cross-scope edges), the `Routing page` marker (at most 3 per
        scope), the navigation tree, and the discovery graph. Its checklist stops requiring a
        home → guide → detail chain;
      - `init.md` and `bootstrap.md` create the routing outline;
      - `curate.md` and `maintain.md` update it within the same approved change;
      - `validate.md` checks outline–tree consistency, missing primary parent routes, and graph-only nodes.
- [ ] Update `examples/sample-company/`: its home carries a routing outline with compact cross-branch edges,
      and its pages drop hop-chain guidance. Include it in the link and contract checks.
- [ ] Update root `AGENTS.md` lifecycle data boundaries for the new operations, scope and authority
      verification, audience containment, bounds, and legacy profiles. Add the Bootstrap rule that neither wiki
      text nor setup approval supplies source-location authority: only a separately user-supplied exact source
      location can enable broad direct-source search. Record the rollback rule: after a skill revert, treat
      scoped profiles as read-only.
- [ ] Update `README.md`, `README.zh-CN.md`, and `skills/company-wiki/README.md` with:
      - the same layers;
      - the five retrieval principles, replacing the `home/map → guide → focused detail → linked source` chain;
      - the progressive lifecycle and roles;
      - Add Source semantics;
      - the labeled `Ingest` compatibility alias;
      - the new package layout.
- [ ] Reconcile `docs/company-wiki_PRD_v0.5.md` with the REQ, decisions 1–13, and the requirements source. It
      must not present the earlier single-wiki lifecycle or sequential multi-hop retrieval as current:
      - update these sections for one routing phase:
        - the §2 Product Thesis diagram;
        - §9 Level 1, including "Loaded when the personal map does not contain a sufficient route";
        - §12;
        - §13, covering its preferred order and bounds and adding the 40,000-character budget;
        - §18 item 3;
        - §22.8;
      - state in §17 that V1 uses neither `.wiki/` nor front matter;
      - retitle the `v0.5` future-directions heading in §23;
      - document personal controls, the retrieved-evidence budget, unavailable provider checks, and the
        post-publication ACL-drift limitation.
- [ ] Add fixtures under `tests/company-wiki-skill/`:
      - `lifecycle/Acquisition Planning 2026.md` (admin-only restricted source carrying the codename token
        `Project Larkspur`);
      - `lifecycle/personal/Q3 Field Priorities.md` (user-authored personal page);
      - `lifecycle/personal/controls/` (the five Personal-control pages that L29 uses alongside
        `personal/Q3 Field Priorities.md`);
      - `lifecycle/defects/` (personal page with an unsourced claim, personal duplicate of an index concept,
        index page leaking the restricted title, personal route citing a superseded standard as current,
        personal page asserting an unsupported relationship);
      - `registry/legacy-profile.md` (pre-scope profile format recording `source:drive` and `wiki:company-index`);
      - `registry/role-claim-profile.md` (company-index profile text claiming reader authority).

      The defect fixtures must let L21 Run A detect every defect within the 5-document bound. Fixtures stay free
      of package tokens. Links to generated index nodes are retargeted during scenario
      setup.
- [ ] Reconcile the main spec `tests/test-company-wiki-skill.md`:
      - lifecycle text and the scenario table;
      - C2 write rules (Init, Bootstrap, Curate, Add Source, Maintain; registry writes only by
        Init/Bootstrap/upgrade registration);
      - the C5 routing table with the new references;
      - S1/S1b as two-turn adapter runs by `admin` with governance and audience verification, including the
        git source under decision 12;
      - S2–S7 running under the adapter as `admin`, with S4 becoming a proposal turn followed by an approval
        turn;
      - S3a/e's read-order evidence rewritten for one routing phase;
      - S3j naming the metadata-visible title and route, stating an owner only if provider metadata exposes
        it, and giving no figures;
      - bounds wherever S3/S5 expectations depend on reading volume;
      - `ingest.md` → `add-source.md`.

      Also update `.docs/tests/test-confirm-wiki-initialization-inputs.md`:
      - I3 and I4 gain the proposal/approval turn. Approving a content proposal does not reconfirm the four
        inputs.
      - R3 and R6 change wherever that turn or the scoped profile fields alter their observable expectations.
        R6 injects its registry failure inside the apply turn with `lock_registry_after_write`.
- [ ] Rewrite `tests/company-wiki-skill/adapter/test_lifecycle_contract.py` to check the following:
      - the lifecycle string and routing;
      - `change-protocol.md` loaded by every writing workflow;
      - the Add Source/Ingest alias;
      - default document/search/depth/retrieved-character bound values;
      - legacy-profile limits;
      - the registry-authority disclaimer;
      - unavailable identity/capability/audience fail-closed behavior;
      - readable Personal controls and current-access rechecks after publication;
      - the five retrieval principles and the routing-phase wording in the skill, READMEs, and PRD;
      - the representable `team` scope and the rule that tree position implies no relationship;
      - EN/ZH/package documentation parity;
      - PRD lifecycle statements;
      - fixture completeness;
      - absence of fixture tokens from the package.

## Validation

- Run `python3 -m unittest discover -s tests/company-wiki-skill/adapter -p 'test_*.py'`. It covers adapter,
  guard, two-principal, and static contract tests.
- Resolve every relative Markdown link in the package, root docs, `AGENTS.md`, PRD v0.5, the requirements
  source, and the story artifacts. Confirm that no reference to `ingest.md` or `company-wiki_PRD_v0.4.md`
  remains.
- Run `git diff --check`. Inspect the complete diff from `00e3cac` and exclude `9468448` and
  `docs/deep-research-report.md`.
- ET executes L1–L30 in isolated `codex exec --json` workspaces with the extended adapter. For each turn,
  retain:
  - the prompt and report;
  - the JSONL;
  - the ordered adapter events with principal;
  - checksums before and after (sources, both wiki roots, both registries);
  - config baselines;
  - the guard result;
  - the exit status.

  Disclose that CLI evidence is weaker than native provider transcripts, and do not claim OS containment.
  Stop if resumed sessions or principal separation cannot be isolated safely.
- ET also runs the reconciled main-spec S0–S7 and the registry-story R1–R6 and I1–I4 through the same harness.
  Every skill file changes, and the main spec's rerun rule requires these runs.

## Risks

- **Scope and size.** Nine skill documents, the harness, fixtures, and both specs change together. The
  lifecycle contract test and link checks must catch stale routes, file names, and lifecycle strings.
- **Setup friction.** Two-turn Init and Bootstrap add a turn to setup. That friction is what binds approval
  to generated content.
- **Unverifiable production audiences.** Many providers cannot report destination audiences or governance
  capability. The skill then refuses shared writes, which is correct but can make shared curation look
  unavailable. Reports must name the missing capability.
- **Bounded reading.** A 5-document default can make Init and complex Query shallower. The agent must report
  exhaustion and coverage limits rather than silently exceed the bound.
- **Routing outline.** One routing phase depends on compact, current home outlines, and an oversized or stale
  outline can misroute. Direct-source search and Validate's outline checks limit the damage. An unusable route is
  reported rather than triggering a second routing phase. An outline that outgrows one document splits into a
  fixed set of routing pages.
- **Leak scope.** Per-document audience containment prevents leaks only if broad pages never reference
  narrower pages. Validate's leakage check and L21/L22 must cover titles, links, aliases, and relationships,
  not only claims.
- **ACL drift after publication.** Without background ACL synchronization, direct access to a static wiki page
  can outlive a later source revocation. V1 fails closed at write time and agent-mediated use; native destination
  ACL governance and periodic Validate remain operational requirements outside this skill's control.
- **Harness state.** Multi-turn resume and between-turn config transitions widen the harness surface. The
  probe must prove per-turn auth removal, per-turn baselines, and continued rejection of model-side config
  mutation before product work.
- **Legacy upgrade.** Upgrade touches user configuration. Preserving the legacy file and repointing the index
  only after a successful write keeps failure recoverable.
- **Rollback.** A revert restores the prior skill, which reads scoped and Personal profiles as combined wikis, so
  any shared write it then attempts is unverified. After a revert, treat scoped profiles as read-only until they
  are removed or the new skill is restored.

## Prior story evidence

- Harness guarantees established by CR rounds 1–4 still apply and must survive the extension:
  - the guard parses command input structurally, accepts one exact adapter process, and correlates operation
    and target sequences with adapter events;
  - it pins the interpreter, adapter checksum, config path, and baseline checksum;
  - it protects config and auth paths from non-adapter commands;
  - config lives outside the agent's writable workspace, with verified absolute and relative OS write denial;
  - disposable auth is removed on `thread.started`, and host-auth bytes stay unchanged.
- The first probe under `/private/tmp/company-wiki-lifecycle-probe.cgnYgI/` is invalid and unused.

## Review record

- Earlier AR rounds 1–4 and CR rounds 1–4 reviewed the superseded REQ. Their conclusions are not reused
  except for the harness guarantees above.
- AR round 1 on the new REQ blocked on six findings. The plan and E2E spec were corrected and decision 12 was
  added:
  - compatibility with the main and registry specs (S3a/e hop order, the S1 git source, the S2–S7 principal,
    I3/I4);
  - retrieval principles missing from the PRD and README tasks;
  - an L-C8 check that could not be scored;
  - an untested `unavailable` capability/audience branch;
  - weak pass criteria for the resumed-turn probe;
  - E2E masters that depended on uncontrolled L1 output.
- AR round 2 (new reviewer, full review) blocked on six findings. The plan and E2E spec were corrected, and
  decision 13 was added:
  - approved writes could not carry content through the guarded adapter;
  - the reader's registered source scope was undefined;
  - L-C8 was ambiguous for evidence linked from a routing-chosen node;
  - S4's correction shortcut conflicted with the REQ, resolved by making S4 two turns without changing the REQ;
  - compatibility reruns were not mandatory;
  - L22's reader run lacked a registry.
- AR round 3 blocked on post-publication ACL drift, unavailable identity/capability proof, a contradictory second
  routing phase, omitted personal controls, missing retrieved-context-budget verification, and missing
  principal/target drift scenarios. The REQ, plan, and E2E were revised before rerun.
- AR round 4 blocked on current-access recheck coverage, the empty-registry exception in L-C1, unsafe direct-Git
  guard scope, and non-executable L29/L30 setup/actions. Current-access rechecks now apply to every workflow;
  L-C1 names the setup exception; repository history/version reads are encapsulated by the adapter; and L29/L30
  use fixed fixtures, masters, prompts, turns, and targets.
- AR round 5 blocked because Bootstrap surfaced derived routes without rechecking evidence, the E2E adapter
  omitted repository-history/version semantics and reachability, and L29 deleted its merge destination.
  Bootstrap now persists only an opaque index-home link and never adopts an index-declared source boundary;
  repository operations are bounded to a configured ref; and L29 merges into a retained target while removing a
  separate temporary node.
- AR round 6 blocked because the Personal master inherited a no-source Bootstrap profile while its Query and
  Explore scenarios required source retrieval. L2 now separately names `source:drive` as an explicit user input
  for the Personal master, while its no-source variant proves that Bootstrap never infers the boundary from the
  index.
- AR round 7 passed after a full rerun by the reused independent reviewer.
- After round 7, the REQ Explore criterion, L5, and the `query.md` task were aligned with the no-second-routing
  rule, which voided the round-7 pass. AR round 8 (new reviewer, full review) blocked on four findings. The REQ,
  plan, and E2E spec were corrected:
  - routing outlines did not expose the cross-branch edges needed for graph discovery;
  - L-C8 contradicted direct-source bypass, and some of its bullets could not be observed;
  - L21 lacked the approved telemetry evidence;
  - repository history dropped the release tags S3g needs.
- AR round 9 (new reviewer, full review) blocked on three findings. The plan and E2E spec were corrected:
  - bound accounting across proposal and apply turns was undefined;
  - L27 Run C lacked its source;
  - removal and merge had no executable meaning.

  Several non-blocking items were also addressed: examples, S7 root resolution, event-log write protection,
  and the L8, L16, and L29 details.
- AR round 10 (new reviewer, full review; the first attempt was cut off by a usage limit) blocked on three
  findings. The plan, E2E spec, and one REQ phrase were corrected:
  - L4 injected its registry fault between turns, so a correct apply-time preflight failed the scenario;
  - main-spec S3j expected an owner that adapter metadata does not expose;
  - L-C6 wiki depth was undefined outside the routing chain.
