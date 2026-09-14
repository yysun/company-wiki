# Retrieval and verification bounds

Use these operation-wide defaults unless the user, selected profile, or host supplies applicable limits. Bounds
control effort; they never grant source access, change a registered boundary, or establish completeness.

| Resource | Default |
|---|---|
| Distinct original sources | 5 native documents across evidence and verification |
| Evidence reads | 10 source document/range requests, including retries and passage expansion |
| Update verification reads | At most 10 additional requests to recheck already-used source evidence |
| Source discovery | 2 native list/search rounds combined |
| Returned original-source content | 40,000 Unicode characters across discovery, evidence, and verification |
| Wiki traversal depth | 3 from the selected home; its named Company Index home is one edge |

Query/Explore use the evidence allowance, including any reread needed to resolve source-version drift; they get
no update-verification allowance. Init, Bootstrap, Curate, Add Source, and Maintain reserve verification only for
an authorized durable-change workflow; it does not authorize publication or bypass proposal approval when required.

## Count work without resetting it

- Count a native source document once even when reading several sections or revisions of that same document.
  An older version stored as a separate native document counts separately. Deduplicate by exact native identity,
  not title or similarity. Count attempted source targets and failed reads conservatively.
- Each requested source document or range consumes one read from the applicable allowance. Batched requests
  charge each document/range separately; batching cannot hide reads. Failed attempts, retries, and overlapping
  passages consume reads. Do not turn body reads into uncounted metadata operations.
- Count all returned original-source characters, including search snippets, repeated/overlapping text, and partial
  or failed responses. Full-document responses count in full even if only one passage is used. Search returning
  full source bodies also consumes distinct-source and evidence-read allowances; it is not free discovery.
- Each native list/search result-page request consumes one discovery round, including continuation pages of the
  same query. Pagination cannot provide unlimited enumeration inside one round. If remaining requests cannot
  establish complete batch membership, refine/select explicitly or request a bounded expansion before continuing.
- Verification may only recheck evidence already used for the planned update. Newly needed sources or additional
  passages needed to establish a new claim consume evidence reads, even if discovered during verification.
  All sources still count against the distinct-source limit and every returned character against the shared cap.
- Selection, review/approval, passage expansion, the routing follow-up, replanning, and recovery continue the same
  operation counters. A retry never replenishes an allowance. Keep counters in working context, not a persistent
  ledger or registry field. A distinct new task starts new counters; an explicit expansion changes only the stated
  limit and preserves consumption so far. If prior consumption is unknown, do not assume a fresh budget.

## Reserve verification before consuming its capacity

For an update, budget the initial evidence reads and one required verification pass over its contributing
evidence before starting reconciliation. Use available native sizes/ranges and conservative estimates; refine the
planned reads as evidence is inspected. Preserve enough remaining verification, character, and any total-read
capacity for the mandatory rechecks. Do not spend that capacity on optional evidence or discover only at apply
time that the planned checks cannot fit. If a required read cannot be bounded to fit, narrow the work or request
the specific expansion before that read or dependent writes.

The applicable verification cap is fixed for the operation, not a new grant per source, plan, or retry. Under the
defaults, an initial plan needing three rechecks reserves three of ten verification reads; remaining capacity can cover necessary rechecks on
the same evidence during drift/recovery. It cannot fund new discovery or refill consumed reads. Stop when any
applicable cap would be exceeded. Small updates therefore have room for their rechecks without a new approval,
while large bodies, extra evidence, or repeated failures can still need a bounded expansion.

## Preserve explicit limits

An explicit total source-read allowance T governs evidence and verification together. It replaces unspecified
default distinct-source, evidence-read, and verification-read ceilings: each is finitely bounded by T, and their
combined reads must still fit T. Separately explicit component caps also apply. Do not add D5/E10/V10 defaults
on top of an existing aggregate allowance that never specified those components. Character, discovery, depth,
and explicit actual tool-call limits keep their independent meanings and are not increased by T.

A source-open/read limit whose legacy wording does not distinguish documents from repeated reads retains these
aggregate semantics; do not silently reinterpret `source documents opened: 5` as five distinct sources with twenty
allowed reads. Conversely, `total source opens: 20` with no separate component caps permits six sources plus six
rechecks, or twelve section reads, within twenty total reads and the unchanged character/search/depth limits.
An explicitly configured distinct-source cap of five or evidence-read cap of ten would still constrain those tasks.
Limits expressly stated in actual tool calls count invocations in addition to applicable document/range accounting.
Never rewrite the profile to adopt defaults. Explicit limits and stricter benchmark contracts remain binding
unless changed by their governing authority.

Three 1,000-character sources can use three evidence reads and three verification reads: three distinct sources
and 6,000 returned characters. An explicit five-total-read cap would still require expansion or a smaller task.
Six short section reads of one source consume six evidence reads and one distinct source. Verification never
bypasses the common character cap. Report the actual limiting resource and a precise expansion when needed;
an exhausted limit is not evidence that a source, fact, or alternative route does not exist.
