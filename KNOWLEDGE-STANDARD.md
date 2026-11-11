# EKOS Knowledge Documentation Standard (EKDS)

Version: 1.0  
Applies to: all technologies, engineering patterns, troubleshooting records and experiments.

## 1. Purpose

Create consistent, searchable, maintainable and source-backed engineering knowledge. Documents must help an engineer understand, implement, diagnose, validate and make decisions—not merely repeat a tutorial.

## 2. Document principles

- One primary subject per document.
- Use a stable, unique ID that does not change when the title changes.
- Prefer official documentation for product behavior.
- State product and version scope.
- Explain prerequisites and assumptions.
- Include working examples where practical.
- Explain failure modes and diagnostic evidence.
- Distinguish fact from inference and recommendation.
- Cite sources close to the claims they support.
- Record test environment and validation date for verified examples.
- Keep documents focused; link related topics rather than duplicating large sections.

## 3. Required front matter

```yaml
---
id: GHA-ARCH-001
title: GitHub Actions Workflow Execution Lifecycle
technology: github-actions
category: architecture
subcategory: execution-lifecycle
content_type: technical-guide
difficulty: intermediate
version_scope:
  product: GitHub Actions
  versions: ["current at review date"]
status: draft
created: 2026-11-11
last_reviewed: null
review_due: null
sources:
  - id: SRC-GHA-DOCS
    url: https://docs.github.com/en/actions
    title: GitHub Actions documentation
    source_type: official
tags:
  - workflow
  - runner
  - execution
related_documents: []
---
```

Required fields: `id`, `title`, `technology`, `category`, `content_type`, `difficulty`, `status`, `created`, `sources`, `tags`.

Allowed status: `draft`, `reviewed`, `verified`, `deprecated`.

Allowed difficulty: `beginner`, `intermediate`, `advanced`, `expert`.

## 4. Recommended body structure

Not every document needs every heading. Select the structure that fits its content.

1. Summary
2. Why this matters
3. Prerequisites and assumptions
4. Core concepts
5. How it works
6. Configuration/reference
7. Implementation
8. Example
9. Expected result
10. Failure modes and edge cases
11. Security considerations
12. Troubleshooting
13. Validation evidence
14. Limitations and version notes
15. Related documents
16. Sources

## 5. Evidence labels

Use explicit labels when a statement's status matters:

- `Officially documented`
- `Experimentally verified`
- `Community-reported`
- `Engineering recommendation`
- `Unverified hypothesis`

Do not label a whole document `verified` if only one code snippet was tested. Explain what was tested and what remains unverified.

## 6. Source quality hierarchy

1. Official product documentation and specifications.
2. Official source code, release notes and security advisories.
3. Maintainer-authored explanations and issue discussions.
4. Reputable technical publications.
5. Community answers and personal blogs.

Community sources can be valuable for failure symptoms and workarounds, but corroborate them before marking a solution verified.

## 7. Troubleshooting record requirements

A troubleshooting document should include:

- stable problem ID;
- exact error text (redacted where necessary);
- affected product/version and environment;
- symptoms and impact;
- prerequisites and reproduction steps;
- diagnostic commands/log locations;
- likely causes, separated from confirmed root cause;
- solution and why it works;
- validation and regression checks;
- alternatives/workarounds;
- security or operational risks;
- sources and verification evidence.

Never present a possible cause as the confirmed root cause without evidence.

## 8. Edge-case record requirements

Describe:
- triggering conditions;
- expected behavior;
- actual behavior;
- boundary or race condition;
- reproducibility;
- impact;
- mitigation;
- regression test;
- version scope.

## 9. Code and command standards

- Include language/shell and platform.
- Mark placeholders clearly, e.g. `<AWS_ACCOUNT_ID>`.
- Never include real secrets.
- State where commands must run.
- Include expected output or observable success criteria.
- Prefer minimal, runnable examples.
- Explain destructive commands and provide safe alternatives.
- Pin dependencies/actions where security or reproducibility requires it.

## 10. Naming and IDs

Recommended prefixes:
- `GHA-FUND-###` fundamentals
- `GHA-ARCH-###` architecture
- `GHA-REF-###` reference
- `GHA-IMPL-###` implementation
- `GHA-SEC-###` security
- `GHA-TROUBLE-###` troubleshooting
- `GHA-EDGE-###` edge cases
- `GHA-CASE-###` case studies
- `GHA-EXP-###` experiments

IDs are unique and permanent. Do not reuse a retired ID.

## 11. Review lifecycle

`draft` → `reviewed` → `verified` (where testable) → `deprecated` (when superseded).

- Draft: collected or authored, not fully checked.
- Reviewed: source and technical review completed.
- Verified: behavior/example tested in stated environment.
- Deprecated: no longer recommended or no longer applicable; link to replacement.

Set `last_reviewed` when a meaningful review occurs. Set `review_due` according to volatility:
- high volatility/security: 30–90 days;
- moderate volatility: 6 months;
- stable concepts: 12 months.

These are suggested review intervals, not guarantees.

## 12. Quality checklist

- [ ] Unique stable ID
- [ ] Required metadata complete
- [ ] Scope/version stated
- [ ] Claims supported by sources or labeled as recommendations/hypotheses
- [ ] Steps are reproducible
- [ ] Commands and code are safe and syntactically checked
- [ ] Exact errors preserved where useful and safe
- [ ] Root cause distinguished from possible causes
- [ ] Validation criteria included
- [ ] Related topics linked
- [ ] No secrets or confidential information
- [ ] Status accurately reflects review and testing
