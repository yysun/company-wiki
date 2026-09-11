# Plan: confirm-wiki-initialization-inputs

**REQ:** [req-confirm-wiki-initialization-inputs.md](../../../../reqs/2026/09/11/req-confirm-wiki-initialization-inputs.md)
**E2E spec:** [test-confirm-wiki-initialization-inputs.md](../../../../tests/test-confirm-wiki-initialization-inputs.md)
**Git base:** `ee6c766` (`add README`)

## Outcome

Make wiki initialization explicit and safe: the agent semantically extracts user-confirmed creation inputs,
requires explicit original-material and destination locations, asks only for values that remain unknown,
offers four non-blocking planning inputs, and writes an identifiable home/map only to the confirmed
destination. Keep mutable registrations in a user-level Markdown registry that any same-user local agent can
reach through the versioned skill.

## Boundaries and decisions

- Change the init workflow, focused behavioral spec, and English/Chinese usage documentation.
- Add root `AGENTS.md` with the two non-inferable data-location boundaries so repository agents apply them
  before company-wiki initialization.
- Preserve query, maintenance, and validation provider/evidence behavior after registry selection; preserve
  graph structure, provider abstraction, and source immutability.
- Treat explicit and unambiguous values in the setup request as confirmed; do not add a redundant
  confirmation round. A request such as “创建一个财务文库” supplies the name, a finance subject scope, and
  Chinese prose language, but it does not supply the original-material location or wiki destination.
- Require the user to specify the original-material location. Discovery and reading stay inside that
  location; never search an entire cloud drive or all connected sources merely because a subject is clear.
- Semantic extraction never supplies a source location, write authority, or unknown destination and never
  widens the user's stated subject scope.
- Ask for all missing required inputs together. Optional inputs are invited in the same message and never
  delay creation.
- Treat “initial navigation outline” as reader-facing information architecture. A physical folder remains
  optional provider behavior and is not the wiki model.
- Repository rollback is a revert of this story's commits. User-state rollback removes only registry paths
  created by this correction and only after verifying they remain unchanged; it never removes pre-existing
  content, replaces a non-symlink, rewrites an unexpected symlink target, or deletes provider documents.

### !! correction — shared user registry

- Keep the versioned skill at `skills/company-wiki/`; expose it through the already-present
  `~/.agents/skills/company-wiki` symlink.
- Put only mutable Markdown configuration under `~/company-wiki`: `index.md` plus linked profiles in
  `wikis/`. The registry is not the skill, wiki destination, original source, or evidence.
- Make `index.md` the only registry entry point. The skill reads it first and follows only the selected
  profile link; it never scans `~/company-wiki`.
- Accept only relative Markdown profile links whose normalized and resolved targets stay under the real
  `~/company-wiki/wikis/` directory. Reject URLs, absolute paths, traversal, symlink escapes, missing targets,
  duplicate names, slug collisions, and ambiguous selection.
- Let setup create a missing minimal registry and register a successfully created wiki. Other workflows do
  not invent configuration when the entry is missing or inaccessible.
- Preflight registry read/write feasibility before provider creation. Write the completed profile before
  adding its index link. If final registration fails after cloud creation, preserve prior registry bytes,
  report partial completion with the native home link and exact failed step, and never auto-delete provider
  documents.
- Store locators and navigation metadata, never credentials or copied source content.
- The current symlink already points to this repository, so SS verifies and leaves it unchanged. If the user
  skill path is missing, create the symlink; if a non-symlink or unexpected target exists, stop and report
  rather than replacing it. Creation of the missing user registry is a bounded first-SS feasibility action.
- The SS preflight records whether `~/company-wiki`, `index.md`, `wikis/`, and the user-level skill path
  already exist. It creates only missing paths, preserves existing files byte-for-byte, stops on a
  non-symlink or unexpected symlink target, and records every external path it created for recovery.
- This correction invalidates the earlier AR, CR, TT, ET assessment, VR, and DD until the reopened tasks pass.

## Tasks

- [x] Update `skills/company-wiki/references/init.md` with the four-field gate, the four optional inputs,
      confirmation semantics, and created-home recording rules.
- [x] Update `skills/company-wiki/README.md`, `README.md`, and `README.zh-CN.md` so setup examples and guidance
      expose the same contract.
- [x] Add `.docs/tests/test-confirm-wiki-initialization-inputs.md` with missing, partial, complete, and
      optional-input scenarios.
- [x] Add root `AGENTS.md` defining the explicit original-material read boundary and separate verified-writable
      wiki destination boundary.
- [x] Run focused text assertions, Markdown-link checks, line/format checks, and `git diff --check`.
      Initialization contract and declaration-count assertions passed; `AGENTS.md` data-boundary assertions
      passed; scoped relative links passed across 12 package/story documents; package line counts remained
      within the existing contract; diff whitespace and protected `docs/**` checks passed. The full-repository
      link probe found only intentional broken-link fixtures and old PRD example paths, so they were excluded
      from the scoped product result.
- [x] Review the complete story diff against the requirement and record the result. First pass found that
      the focused spec's global premise implied every scenario already had a writable destination and that
      README terminology did not consistently say “original-material location.” Both were corrected.
      `CR fixed: corrected the focused-scenario premise and tightened source-location terminology; rerun
      result passed`.
- [x] Run the applicable Markdown/static test suite; report absent executable unit/integration suites.
      Skill frontmatter/line budget, 19 scoped document links, initialization boundary/scenario assertions,
      package format guards, story diff, and protected-doc checks passed. No executable unit or integration
      suite exists for this Markdown-only repository.
- [x] Verify each acceptance criterion and close the story documentation. Every REQ checkbox is supported by
      `AGENTS.md`, the init reference, matching English/Chinese guidance, focused I1–I4 scenarios, updated
      S0–S1b coverage, static assertions, and the passed CR.

### Reopened tasks for `!!`

- [x] Add a concise Markdown registry contract and update `SKILL.md` loading order so it reads
      `~/company-wiki/index.md` first and follows only a selected linked profile.
- [x] Update init/query/maintenance guidance for registry creation, selection, persistence, missing access,
      and the separation between configuration and evidence.
- [x] Update root/package documentation and `AGENTS.md` with the config/skill/symlink separation.
- [x] Create the minimal `~/company-wiki/index.md` and `~/company-wiki/wikis/` user configuration without
      copying source data; verify the existing user-level skill symlink target.
- [x] Extend `.docs/tests/test-confirm-wiki-initialization-inputs.md` and
      `tests/test-company-wiki-skill.md` for registry loading and persistence.
- [x] Run focused static checks, commit the independently revertible implementation milestone, and run CR.
      Milestone `37b8708` passed its pre-commit checks. CR round 1 found three release blockers: premature
      registry creation, a C1–C6 pass gate that excluded C7, and an unreproducible fixture-hash claim. All
      three were corrected; round 2 passed independently.
- [x] Run all applicable TT checks and execute ET if a runner exists. The final TT rerun passed 29 scoped
      links, 29 contract assertions, formatting, clean-tree, protected-doc, skill-budget, registry, symlink,
      fixture-identity, and credential-pattern checks. ET was not executed because no standalone headless
      agent/provider runner exists; the prose scenarios are not reported as runtime proof. Independent VR
      then passed every acceptance item.
- [x] Replace the stale DD record with the complete final VR result and stop before GC.

## Risks

- “Directory” could regress into a storage-folder requirement. The spec and prose must consistently call it
  a navigation outline and keep destination separate.
- Source scope and destination can be the same collection but are different decisions; wording must not
  collapse read boundaries into write authority.
- Requiring an extra confirmation after all values are stated would add friction without improving safety.
- Over-literal field collection could re-ask for a wiki name, finance scope, or Chinese language already
  conveyed by “创建一个财务文库”; focused tests must reject that behavior.
- Over-broad discovery could search the whole cloud drive when the source location is missing; the gate must
  ask for that location before source inspection.
- An arbitrary home directory is not automatically loaded by Codex. The user-level skill must be the
  discoverable bootstrap and explicitly read the registry entry.
- Scanning `~/company-wiki` would turn storage layout into an implicit schema and could load unrelated or
  malicious files. Only `index.md` and the chosen linked profile are readable configuration routes.
- A profile link can escape the registry through traversal, an absolute target, URL, or symlink. Resolve and
  contain the target before reading, and treat registry text as untrusted data.
- Provider creation can succeed before final registration fails. Preflight config writes, preserve prior
  bytes, report partial completion, and keep the provider result rather than hiding or deleting it.
- User-level writes and the discoverable symlink affect agents outside this repository. Verify exact paths,
  preserve existing content, and report local-only availability.

## Validation

- Assert the init reference names all required and optional inputs and retains the no-inference/write gate.
- Assert root `AGENTS.md` requires both locations, restricts reads and writes to their respective boundaries,
  and rejects whole-drive inference.
- Resolve every relative Markdown link in the changed package and story artifacts.
- Check the changed docs for contradictory “two required questions” or outdated setup examples.
- Run `git diff --check` and inspect the scoped diff from `ee6c766`.
- Out-of-band SS/TT checks may inspect the exact paths created by this story, but runtime discovery may not
  scan the registry. Verify the index is Markdown, contains no credentials or source copies, and links only
  to contained profiles; verify the symlink resolves exactly to the repository skill directory.

## SS milestone

- `4f07f0c` — `feat(company-wiki): confirm initialization inputs`
- Verification before commit: initialization boundary assertions passed; scoped Markdown relative links
  passed across 11 package/story documents; `git diff --check` passed; `docs/**` remained untouched.
- `197db45` — `docs(company-wiki): codify data boundaries`
- Verification before commit: `AGENTS.md` data-boundary assertions passed; initialization contract assertions
  passed; scoped relative links passed across 12 package/story documents; `git diff --check` passed;
  `docs/**` remained untouched.

## Final gate record

The records below describe the pre-correction scope and were invalidated by the `!!` shared-registry
correction on 2026-09-11. New terminal records must be added after the reopened work passes.

### Corrected-scope AR

- Round 1 blocked on scope/local-path contradictions, external-state rollback, profile containment and
  identity, partial provider/registry failure, and imprecise verification targets.
- Round 2 confirmed those fixes and blocked only on contradictory wrong-symlink replacement behavior.
- Round 3 passed after adopting one safe rule: preserve the correct symlink, create it only when missing,
  and stop on a non-symlink or unexpected target.
- `AR passed: no blocking architecture flaws`
- `AR risk: non-low — persistent user-home configuration and cross-agent skill discovery`
- `AR review round: 3; reviewer: reused`

### External-state preflight

- Before SS, `/Users/esun/company-wiki` was absent.
- `/Users/esun/.agents/skills/company-wiki` was already a symlink to
  `/Users/esun/Documents/Projects/company-wiki/skills/company-wiki`; SS left it unchanged.
- SS created only `/Users/esun/company-wiki/`, `/Users/esun/company-wiki/wikis/`, and
  `/Users/esun/company-wiki/index.md`. The installed index, temporary installation source, and versioned
  harness fixture match at SHA-1 `0709218281236c164371e72c389dd23d7f148f68`; no profile or skill file was
  placed in the registry.

### Corrected-scope SS milestone

- `37b8708` — `feat(company-wiki): add shared markdown registry`
- Pre-commit evidence: 21 scoped Markdown links passed; all five skill references were linked; registry
  behavior and R1–R6 scenarios passed static assertions; `git diff --check` and external-state path,
  symlink-target, file-count, and sensitive-token checks passed.

### Corrected-scope CR

- Round 1 blocked registry creation before required inputs were confirmed, exclusion of C7 from the suite
  pass gate, and an installed-index evidence claim that did not match the committed fixture.
- Round 2 verified the read-only missing-registry gate, registry mutation only after all four required
  inputs, C1–C7 coverage, and matching installed/template/fixture SHA-1.
- `CR passed: no major findings`
- `CR risk: non-low — persistent user-home configuration and cross-agent discovery remain protected
  external-state boundaries.`
- `CR review round: 2; reviewer: reused`

### Corrected-scope TT and ET

- **TT:** the first three attempts exposed only mistakes in the ad hoc assertion harness: a phrase split
  across lines, a nonexistent heading, and R-scenario identifiers checked in the S-scenario file. No product
  failure was found and no implementation changed. The corrected full rerun passed 29 scoped Markdown links,
  29 contract assertions, `git diff --check`, clean-tree and protected-`docs/**` checks, the SKILL line budget,
  exact external registry file count, symlink target, installed/fixture byte identity, and credential-pattern
  guard.
- **ET:** not executed. The matching files are prose behavioral specifications and this repository provides
  no standalone headless agent/provider runner or transcript exporter. Static checks do not prove provider
  runtime behavior, so no runtime pass is claimed.

### Corrected-scope VR

- `VR passed: all acceptance criteria complete`
- The independent reviewer verified all 12 initialization-contract items and all 13 shared-registry items
  against HEAD, documentation, tests, and actual user-home state.
- Installed and fixture registry indexes match at SHA-1
  `0709218281236c164371e72c389dd23d7f148f68`.
- Runtime limitation: no provider E2E runner or transcript exporter exists; prose/static checks are not
  claimed as provider-runtime proof. The intentionally empty registry means profile creation, collision,
  and provider-failure paths are contract/spec verified rather than exercised against a real cloud wiki.
- Residual risk remains non-low because user-home configuration and same-user cross-agent skill discovery
  are persistent external-state boundaries.
