> Illustrative example only; this is not an organization's catalog.

# Competency questions

Each record is a small test of whether the schema can route and answer a recurring question.

## CQ-LOOKUP-001

```yaml
id: CQ-LOOKUP-001
question: What is the current vacation-policy?
intent: authoritative_lookup
domain: [people]
expected_problem_pattern: authoritative-lookup
required_evidence: [current approved policy]
authority_expectation: [canonical, approved]
review_status: confirmed
evidence: user-supplied question
```

## CQ-LOOKUP-002

```yaml
id: CQ-LOOKUP-002
question: What is the official definition of an active-customer?
intent: authoritative_lookup
domain: [customers]
expected_problem_pattern: authoritative-lookup
required_evidence: [business definition]
authority_expectation: [canonical]
review_status: confirmed
evidence: user-supplied question
```

## CQ-LOOKUP-003

```yaml
id: CQ-LOOKUP-003
question: How is churn-rate calculated?
intent: authoritative_lookup
domain: [customers]
expected_problem_pattern: authoritative-lookup
required_evidence: [metric definition, numerator, denominator]
authority_expectation: [canonical, approved]
review_status: confirmed
evidence: user-supplied question
```
