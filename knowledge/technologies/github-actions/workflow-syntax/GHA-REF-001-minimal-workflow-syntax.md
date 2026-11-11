---
id: GHA-REF-001
title: Minimal GitHub Actions Workflow Syntax Reference
technology: github-actions
category: workflow-syntax
subcategory: workflow-file-structure
content_type: feature-reference
difficulty: beginner
version_scope:
  product: GitHub Actions
  reviewed_against: GitHub Docs as accessed 2026-11-11
status: reviewed
created: 2026-11-11
last_reviewed: 2026-11-11
review_due: 2027-05-11
sources:
  - id: SRC-GHA-WORKFLOW-SYNTAX
    url: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    title: Workflow syntax for GitHub Actions
    source_type: official
  - id: SRC-GHA-CONTEXTS
    url: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts
    title: Contexts reference
    source_type: official
tags: [yaml, workflow-syntax, jobs, steps, runs-on, permissions]
related_documents: [GHA-FUND-001, GHA-ARCH-001, GHA-ARCH-002]
---

# Minimal GitHub Actions Workflow Syntax Reference

## Purpose

This guide introduces the structure of a workflow file. It is not a complete YAML or GitHub Actions reference. Consult the official syntax reference for every supported key, data type, default and availability constraint.

## File location

Workflow files are stored in:

```text
.github/workflows/
```

They use `.yml` or `.yaml` extensions.

## Minimal workflow

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read

jobs:
  build:
    name: Build and test
    runs-on: ubuntu-latest

    steps:
      - name: Check out source
        uses: actions/checkout@v6

      - name: Show commit
        run: echo "Building commit $GITHUB_SHA"
```

The `actions/checkout@v6` reference is an illustrative major-version tag, not a universal security recommendation. Review and pin third-party actions according to your organization's policy.

## Common top-level keys

| Key | Purpose |
|---|---|
| `name` | Display name of the workflow |
| `run-name` | Display name for an individual run; may use expressions where supported |
| `on` | Events and filters that trigger the workflow |
| `permissions` | Default `GITHUB_TOKEN` permissions for the workflow |
| `env` | Environment variables at workflow scope |
| `defaults` | Defaults such as shell and working directory |
| `concurrency` | Controls overlapping workflow runs/jobs |
| `jobs` | Map of job definitions |

## Common job keys

| Key | Purpose |
|---|---|
| `name` | Display name of the job |
| `runs-on` | Runner type, label or group selection |
| `needs` | Job dependencies |
| `if` | Conditional job execution |
| `permissions` | Job-specific token permissions |
| `environment` | Deployment environment and protection rules |
| `env` | Job-level environment variables |
| `steps` | Ordered list of steps |
| `strategy` | Matrix or fail-fast behavior |
| `timeout-minutes` | Job timeout configuration |
| `continue-on-error` | Controls how a job failure affects the workflow result |

## Common step keys

| Key | Purpose |
|---|---|
| `name` | Human-readable step name |
| `id` | Identifier for referencing step outputs |
| `if` | Conditional execution |
| `uses` | Invoke an action |
| `run` | Execute a shell command |
| `shell` | Select shell |
| `working-directory` | Set command working directory |
| `env` | Step-level environment variables |
| `with` | Inputs passed to an action |

A step generally uses `uses` or `run`; do not combine them as if they were one operation.

## Job dependencies

Jobs without dependencies can run in parallel. Use `needs` to establish ordering:

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
      - run: echo "Test after build"
```

Remember that `test` runs as a separate job and does not automatically inherit files from `build`. Use artifacts or another explicit transfer mechanism.

## Shell and operating-system considerations

The default shell can differ by runner OS and by explicit shell selection. For portable workflows:
- explicitly select a shell when behavior matters;
- quote values safely;
- avoid assuming Bash syntax works in PowerShell or `cmd`;
- use `pwsh` for PowerShell Core where appropriate;
- use OS-specific jobs or matrix strategies when validating multiple platforms.

Example:

```yaml
- name: Print on Windows
  if: runner.os == 'Windows'
  shell: pwsh
  run: |
    Write-Host "Running on Windows"
```

The `runner` context is available in supported expression locations; consult the contexts reference for exact availability.

## YAML pitfalls

1. Indentation is structural; use consistent spaces, not tabs.
2. Quote values when YAML typing or special characters could cause ambiguity.
3. Be careful with the `on` key when parsing workflow YAML using generic YAML tooling: YAML 1.1 parsers may interpret `on` as a boolean key. Use a YAML 1.2-compatible parser or configure the parser appropriately.
4. Use `${{ ... }}` expressions only in supported contexts and fields.
5. Avoid interpolating untrusted event data directly into shell scripts; pass values through environment variables and quote/validate them.
6. Minimize token permissions and explicitly declare the required scope.

## Safe test workflow

```yaml
name: EKOS syntax practice

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  inspect:
    runs-on: ubuntu-latest
    steps:
      - name: Print runner information
        run: |
          echo "Operating system: $RUNNER_OS"
          echo "Repository: $GITHUB_REPOSITORY"
```

This workflow does not check out code or access secrets. It is suitable for a first syntax experiment.

## Validation tools

- GitHub's workflow editor and Actions UI provide workflow feedback.
- `actionlint` is a community-maintained static checker; evaluate its version and rules separately.
- YAML syntax validation alone is insufficient: a YAML file can parse but still violate GitHub Actions schema or context rules.

## Sources

- SRC-GHA-WORKFLOW-SYNTAX
- SRC-GHA-CONTEXTS
