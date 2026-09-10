> Illustrative example only; this is not an organization's schema.

# Authoritative lookup

```yaml
id: authoritative-lookup
name: Authoritative Lookup
intent: Find the current authoritative answer to a specific fact, policy, ownership, or definition question.
trigger_examples:
  - What is the current vacation-policy?
requires:
  - target concept
  - authoritative source
  - effective date when relevant
investigation:
  - resolve terminology
  - identify the authoritative route
  - retrieve current evidence
  - check scope and effective date
  - answer with a source citation
competency_questions: [CQ-LOOKUP-001, CQ-LOOKUP-002]
review_status: confirmed
confirmed_by: user
```
