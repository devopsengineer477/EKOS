---
id: GHA-FUND-001
title: What Is GitHub Actions?
technology: github-actions
category: fundamentals
subcategory: purpose-and-capabilities
content_type: concept
difficulty: beginner
version_scope:
  product: GitHub Actions
  reviewed_against: GitHub Docs as accessed 2026-11-11
status: reviewed
created: 2026-11-11
last_reviewed: 2026-11-11
review_due: 2027-05-11
sources:
  - id: SRC-GHA-UNDERSTAND
    url: https://docs.github.com/en/actions/get-started/understand-github-actions
    title: Understanding GitHub Actions
    source_type: official
  - id: SRC-GHA-CONCEPTS
    url: https://docs.github.com/en/actions/concepts
    title: Concepts for GitHub Actions
    source_type: official
tags: [ci, cd, automation, workflows, fundamentals]
related_documents: [GHA-ARCH-001, GHA-ARCH-002]
---

# What Is GitHub Actions?

## Summary

GitHub Actions is GitHub's automation platform for running workflows in response to repository and external events, on demand, or on a schedule. It is commonly used for continuous integration (CI), continuous delivery/deployment (CD), repository automation, release workflows, security automation and engineering operations.

A workflow is declared as YAML in a repository. An event can trigger a workflow run; the run contains one or more jobs; jobs execute on runners; and each job contains ordered steps that run shell commands or reusable actions.

## Why it matters to a test engineer

GitHub Actions can make quality checks repeatable and visible at the same point in the software delivery lifecycle where code changes are proposed or integrated.

Examples:
- Build a .NET, Java, Python or Node.js application.
- Run unit, API, UI, contract or regression tests.
- Publish test reports and coverage artifacts.
- Run SAST/SCA checks.
- Build and push a Docker image.
- Deploy an approved artifact to a test or production environment.
- Notify a team when a workflow fails.

## Core terminology

| Term | Meaning | Practical interpretation |
|---|---|---|
| Event | Activity or condition that starts a workflow | Push, pull request, release, schedule or manual dispatch |
| Workflow | YAML-defined automated process | A CI pipeline or deployment pipeline |
| Workflow run | One execution of a workflow | A specific run with an event, status, logs and jobs |
| Job | A group of steps executed on one runner | Build job, test job, deploy job |
| Step | One task within a job | Run a command or invoke an action |
| Action | Reusable automation component | Checkout source, configure toolchain, upload artifact |
| Runner | Machine or execution environment that runs a job | GitHub-hosted VM or self-hosted machine |
| Artifact | File(s) retained and shared from a workflow run | Test report, package, build output |
| Context | Runtime information exposed to workflow expressions | Event, repository, runner, job and step data |
| Expression | Dynamic expression evaluated by GitHub Actions | Conditional logic or dynamic values |

## Typical CI lifecycle

1. A developer pushes a commit or opens/updates a pull request.
2. GitHub receives the event and evaluates workflow trigger configuration.
3. A matching workflow run is created.
4. GitHub schedules eligible jobs, considering dependencies and runner requirements.
5. A suitable runner receives a job.
6. The runner checks out code and executes the job's steps.
7. Job results are reported to the workflow run.
8. Dependent jobs may proceed, or the run ends according to the result and configured conditions.

This is the documented conceptual model. It is not a claim about every internal service or private implementation detail behind GitHub's hosted control plane.

## GitHub Actions is broader than CI/CD

The platform can automate issue triage, labels, repository maintenance, scheduled operations, release tasks, security checks and other GitHub-connected processes. CI/CD is a major use case, not the only use case.

## When to use it

Use GitHub Actions when:
- the source code and workflow should be versioned together;
- automation should respond to GitHub events;
- teams need visible checks on pull requests;
- repeatable build/test/release processes are required;
- reusable workflows or actions can reduce duplication.

Evaluate other systems or a hybrid design when requirements include specialized orchestration, extensive legacy infrastructure integration, unusual network isolation, long-running workloads, or operational controls not met by the available runner model.

## GitHub-hosted versus self-hosted at a glance

| Consideration | GitHub-hosted | Self-hosted |
|---|---|---|
| Machine ownership | GitHub provisions the environment | Organization/user operates the machine |
| Maintenance | GitHub maintains hosted images | You maintain OS, tools and runner host |
| Custom hardware/network | Limited to available hosted options | Greater control, with greater responsibility |
| Isolation/lifecycle | Standard hosted jobs use fresh provisioned environments | Depends on your runner architecture and cleanup |
| Typical use | Standard CI and deployment tasks | Private network access, specialized tools or controlled hardware |

Check current runner documentation and plan-specific availability before making a cost or capability decision.

## Common misunderstandings

**Misunderstanding:** A workflow is the same as a job.  
**Correction:** A workflow contains one or more jobs; jobs contain steps.

**Misunderstanding:** Every job in a workflow shares one machine.  
**Correction:** Each job is assigned a runner. Jobs should not rely on another job's local filesystem; use artifacts or other explicit transfer mechanisms.

**Misunderstanding:** Actions are the same as shell commands.  
**Correction:** A step can run a shell command (`run`) or invoke a reusable action (`uses`).

**Misunderstanding:** GitHub Actions only runs after a push.  
**Correction:** Workflows can be triggered by many event types, manual dispatch, schedules and supported external dispatch mechanisms.

## Practical learning exercise

Create a disposable repository and add `.github/workflows/hello.yml`:

```yaml
name: Hello EKOS

on:
  workflow_dispatch:

jobs:
  hello:
    runs-on: ubuntu-latest
    steps:
      - name: Print a message
        run: echo "Hello from GitHub Actions"
```

Expected observations:
- The workflow appears under the repository's Actions tab.
- A manual run can be started if repository settings and permissions allow it.
- The run contains one job and one step.
- The step log shows the command output.

Do not place secrets in the YAML file or echo secret values into logs.

## Limitations and version notes

- Available runner images, labels, software, quotas, pricing and product capabilities can change.
- Organization and repository policies may restrict Actions or runner use.
- Some features depend on repository visibility, plan, organization policy or event context.
- Use the current official reference for exact syntax and availability.

## Related documents

- [GHA-ARCH-001 — Core components and conceptual architecture](../architecture/GHA-ARCH-001-core-components-and-architecture.md)
- [GHA-ARCH-002 — Workflow run and job execution lifecycle](../architecture/GHA-ARCH-002-workflow-run-lifecycle.md)
- [GHA-REF-001 — Minimal workflow syntax reference](../workflow-syntax/GHA-REF-001-minimal-workflow-syntax.md)

## Sources

- SRC-GHA-UNDERSTAND — primary explanation of GitHub Actions and core terms.
- SRC-GHA-CONCEPTS — product concept taxonomy.
