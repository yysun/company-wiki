# Bounded wiki retrieval

**REQ:** [req-bounded-wiki-retrieval.md](../../../../reqs/2026/09/14/req-bounded-wiki-retrieval.md)
**Story base:** `04aabff`

Pre-existing uncommitted work belongs to the completed wiki-update-authorization story: its plan and completion
report. Preserve it and exclude it from this story's commits.

## Decisions

Use one shared retrieval-bounds reference: default five distinct native source documents, ten evidence read calls
(including section reads/retries), two source discovery rounds, 40,000 returned Unicode source characters, and
wiki traversal depth three. Distinct revisions at one native document count as one document; separate native
version documents count separately. All returned source text counts in Unicode characters even on failed/partial operations.

For an authorized update, reserve one finite verification pass over the necessary source passages, planned from
native sizes/ranges and then refined from observed evidence. Default at most ten verification reads per operation,
no automatic replenishment, no discovery from that bucket. This allowance is separate from evidence-read calls
but not from distinct-source or total-character limits. Keep total-call caps explicitly specified by users,
profiles, or the host across both buckets. Ambiguous legacy read/open limits retain total-call semantics;
do not reinterpret them as distinct-source limits. An explicit aggregate allowance T replaces unspecified default
distinct/evidence/verification ceilings with finite ceilings derived from T, while the aggregate T still governs
all reads together. Separately explicit component caps continue to apply; character/discovery/depth caps are unchanged.
Each native discovery result-page request, including pagination, consumes one round. Unknown size uses conservative bounded reads and leaves room
for verification; if the needed work cannot fit, narrow or request a precise expansion before dependent work.
Keep accounting transient in the operation; no new state, registry fields, or approval artifacts are required.

Source intent resolves by exact locator, an unambiguous specific description established by adequate metadata,
or an explicit finite batch predicate within a concrete registered scope. Resolve and report exact native targets
before body reads. A lone hit in truncated or insufficient metadata is not proof of identity/completeness. Freeze
the enumerated batch snapshot; later matches do not join. Generic keywords/patterns without explicit batch intent
remain discovery criteria. User-requested review/selection overrides automatic resolution. Preserve hard bounds.

Routing keeps one compact initial phase, plus at most one evidence-triggered follow-up of up to three targeted
wiki pages within existing traversal depth and registered profile edges. Use known visible routes/links, including
the registered home when a direct-source bypass later needs a route; do not scan the wiki or restart full routing.
The follow-up must address an observed authority/alias/exception gap; no extra lookup for mere optimization,
learning, or provenance housekeeping. Source search and content budgets do not reset.

## Tasks

- [x] Implement shared bounds and source resolution in SKILL.md, AGENTS.md, add-source.md, query.md,
  change-protocol.md, registry.md as needed, and a linked retrieval-bounds.md reference. Preserve publication gates.
- [x] Reconcile current guides, product/article descriptions, sample home, and affected lifecycle scenarios;
  remove obsolete static wording assertions. Preserve historical results and explicitly stricter benchmark
  contracts, documenting the distinction rather than rewriting old measurements.
- [x] Run applicable adapter/contract and benchmark unit suites, skill validation, changed-link/whitespace checks,
  and the independent decision cases in [the story spec](../../../../tests/test-bounded-wiki-retrieval.md).

## Verification

Non-low risk: source selection authority and bounded retrieval behavior change. Independent AR/CR/VR applies.
The repository implements instructions; its adapter lacks production identity/audience/conditional-write support.
Use independent isolated read-only decisions for the planned ET surface; no live provider or registry operations.
Give the evaluator raw case inputs and skill only, not expected answers or author conclusions.

Commands: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests/company-wiki-skill/adapter -p 'test_*.py' -v`;
the equivalent discovery under `tests/rag-quality`; skill-creator `quick_validate.py`; added Markdown-link checks;
and `git diff --check`. Do not run paid/live CLI benchmark sessions or update their historical output.

## Review evidence

AR passed: no blocking architecture flaws

AR risk: non-low — changes source-selection authority and bounded retrieval behavior.
AR review round: 1; reviewer: reused (`authorization_review`)

Independent review found the finite budgets, legacy-cap compatibility, resolved selection, targeted follow-up,
and isolated decision coverage feasible, with no blocking architecture flaws.

Implementation verification: all 23 adapter/contract tests and 19 benchmark/report unit tests pass (42 total).
Skill validation, 27 added Markdown links, and diff whitespace checks pass. The unchanged benchmark runner retains
its explicit five-read and initial-only routing overrides; no historical result was rewritten. Independent B1–B16
interpretation evaluation passed all B1–B16 core decisions from raw inputs and current skill files only. No provider
operations ran. CR round 1 passed; a focused compatibility case reopened CR in round 2 because an explicit
twenty-open allowance could still be constrained by new D5/E10 defaults. The aggregate precedence rule above
resolves that restriction. B17/B18 cover higher caps, separately explicit component limits, and pagination.
AR round 2 passed the focused correction before implementation; prior unrelated review conclusions remain valid.

AR passed: no blocking architecture flaws

AR risk: non-low — compatibility of authorized retrieval limits.
AR review round: 2; reviewer: reused (`authorization_review`)

Implementation milestone: `64ed423` — first three restriction fixes, shared bounds, and reconciled guides/scenarios.
At commit: all 42 local tests, skill validation, 27 added links, and whitespace checks passed. Subsequent focused
checks confirmed skill/link/whitespace validity after the aggregate-limit correction. No executable test/runner
changed afterward, so the unit evidence remains applicable.

Independent evaluation completed all 18 cases and variants, including supplemental B17/B18 and affected B3/B5
rechecks. The execution record states concrete observed decisions and provider/quality-evaluation limits.

CR passed: no major findings

CR risk: non-low — source-selection authority and retrieval-limit compatibility.
CR review round: 3; reviewer: reused (`authorization_review`)

The aggregate-limit ambiguity and pagination definition are resolved; prior source-selection, routing, publication,
and approval conclusions remain valid. All implementation/verification tasks are complete.

VR passed: all acceptance criteria complete

VR risk: non-low — source-selection authority and retrieval-limit compatibility.
VR review round: 1; reviewer: reused (`authorization_review`)

Independent VR marked all six criteria complete. Evidence establishes package validity and instruction
interpretation; live-provider execution/enforcement and retrieval-quality improvements remain untested.
The completion report preserves the full final VR result.

Correction milestone: `a0554d9` — preserve explicit aggregate allowances, count discovery pagination,
and record completed verification. DD is complete; stopped before GC, with no release or push.
