---
id: GHA-ARCH-002
title: Workflow Run and Job Execution Lifecycle
technology: github-actions
category: architecture
subcategory: execution-lifecycle
content_type: technical-guide
difficulty: intermediate
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
  - id: SRC-GHA-WORKFLOW-SYNTAX
    url: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    title: Workflow syntax for GitHub Actions
    source_type: official
  - id: SRC-GHA-EVENTS
    url: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
    title: Events that trigger workflows
    source_type: official
  - id: SRC-GHA-TROUBLESHOOT
    url: https://docs.github.com/en/actions/how-tos/troubleshoot-workflows
    title: Troubleshooting workflows
    source_type: official
tags: [lifecycle, workflow-run, scheduling, jobs, runner, troubleshooting]
related_documents: [GHA-ARCH-001, GHA-REF-001, GHA-RUN-001]
---

# Workflow Run and Job Execution Lifecycle

## Summary

This document describes the observable, documented lifecycle from an event to workflow execution and final status. It is a practical troubleshooting model, not a claim to expose GitHub's private internal scheduler implementation.

## Lifecycle overview

```mermaid
sequenceDiagram
    participant Actor as User / GitHub event
    participant GH as GitHub Actions service
    participant Runner as Selected runner
    participant Job as Job steps
    Actor->>GH: Event or manual dispatch
    GH->>GH: Evaluate workflow trigger and filters
    GH->>GH: Create workflow run and determine eligible jobs
    GH->>Runner: Assign job matching runs-on
    Runner->>Job: Execute steps in order
    Job-->>Runner: Step and job result
    Runner-->>GH: Report job result and logs
    GH->>GH: Evaluate dependent jobs and final run result
```

## Stage 1 — Event occurs

An event may originate from a repository activity, a schedule, a manual invocation or a supported external dispatch. The event determines the event context and payload available to the workflow.

Examples:
- `push`;
- `pull_request`;
- `workflow_dispatch`;
- `schedule`;
- `release`;
- `workflow_run`.

Not all event types have identical payloads, permissions or branch behavior.

## Stage 2 — Trigger and filter evaluation

GitHub evaluates whether the workflow should run based on the workflow's `on` configuration and applicable conditions such as:
- event type;
- activity type;
- branch or tag filters;
- path filters;
- workflow enabled state;
- repository/default-branch requirements;
- event-specific rules;
- skip annotations in commit messages.

Important troubleshooting facts documented by GitHub:
- Some events, including `schedule`, require the workflow file to exist on the default branch.
- A `pull_request` workflow may not run when the PR has merge conflicts.
- Push/pull-request workflows may be skipped when commit messages contain supported skip annotations.
- Workflows can be disabled.

Always inspect the current event documentation for event-specific behavior.

## Stage 3 — Workflow run and job graph

A matching trigger creates a workflow run. The workflow defines one or more jobs.

By default, jobs without dependencies can run in parallel. A job that declares `needs` waits for its dependency jobs to complete. Conditional expressions can further control whether a job runs.

For a simple pipeline:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - run: echo "Build"

  test:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - run: echo "Test"

  package:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: echo "Package"
```

The dependency graph is `build → test → package`. Each job has its own runner assignment; do not assume that files created in `build` automatically exist in `test` or `package`. Transfer files explicitly, commonly with artifacts.

## Stage 4 — Runner matching and job dispatch

The job's `runs-on` field selects the required runner environment. For self-hosted runners, labels and groups determine eligibility. A job can remain queued when no matching online, idle runner is available.

For a self-hosted runner, investigate:
- runner process/service state;
- online/offline state;
- labels and groups;
- repository or organization access policy;
- host capacity;
- outbound HTTPS connectivity;
- firewall, proxy and DNS;
- runner application logs.

## Stage 5 — Job execution

A job runs on its assigned runner. Its steps execute in order by default. Each step can execute a shell command or invoke an action.

Within one job:
- steps use the same runner workspace;
- step processes are distinct;
- environment changes made only inside one shell process do not automatically persist to another step;
- use `$GITHUB_ENV`, `$GITHUB_OUTPUT` or documented mechanisms for supported cross-step data passing.

Between jobs:
- local files are not automatically shared;
- use artifacts, caches for their intended purpose, external storage or explicit job outputs for small values.

## Stage 6 — Result evaluation

A step/job can succeed or fail. Job dependencies and conditional expressions influence subsequent jobs. Workflow status is derived from the jobs and workflow conditions.

For troubleshooting, distinguish:
- a step failure;
- a job skipped due to condition/dependency;
- a job waiting for a runner;
- a workflow that never triggered;
- a run cancelled or timed out.

Do not diagnose all missing downstream work as a runner problem.

## Stage 7 — Re-runs, cancellation and side effects

Re-running a workflow or job can repeat side effects. Deployment, database migration, package publishing and infrastructure operations should be designed for idempotency or have explicit safeguards.

Before enabling automatic retries, determine:
- whether the operation is safe to repeat;
- whether partial work may already have completed;
- whether duplicate artifacts/releases/resources can be created;
- whether a concurrent run can target the same environment.

## Troubleshooting decision tree

```text
Did a workflow run appear?
  No  -> inspect event, on:, filters, default branch, skip rules, enabled state
  Yes ->
    Is the job queued?
      Yes -> inspect runs-on, labels/groups, runner online state, capacity, policy
      No  ->
        Did a step fail?
          Yes -> inspect exact log, shell, tool version, permissions, network
          No  ->
            Was a dependent job skipped?
              Yes -> inspect needs, outputs, if conditions and status functions
              No  -> inspect final run summary and event-specific behavior
```

## Practical diagnostic checklist

- [ ] Confirm the workflow file exists under `.github/workflows/`.
- [ ] Confirm the workflow is enabled.
- [ ] Confirm the actual event and activity type.
- [ ] Inspect branch, tag and path filters.
- [ ] Check default-branch requirements for the event.
- [ ] Check commit skip annotations.
- [ ] Confirm a run was created.
- [ ] If queued, verify `runs-on` and matching runner availability.
- [ ] If running, identify the first failing step.
- [ ] Check whether required files were transferred between jobs.
- [ ] Check permissions and secret availability without printing secret values.
- [ ] Check `needs` and `if` for skipped jobs.
- [ ] Record run URL, commit SHA, workflow file revision and timestamps.

## Related documents

- GHA-ARCH-001 — Core Components and Conceptual Architecture
- GHA-REF-001 — Minimal Workflow Syntax Reference
- GHA-RUN-001 — Runner Types and Job Routing

## Sources

- SRC-GHA-UNDERSTAND
- SRC-GHA-WORKFLOW-SYNTAX
- SRC-GHA-EVENTS
- SRC-GHA-TROUBLESHOOT
