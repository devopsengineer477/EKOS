---
id: GHA-EXP-001
title: First GitHub Actions Workflow Using Manual Dispatch
technology: github-actions
category: experiments
subcategory: workflow-basics
content_type: experiment
difficulty: beginner
version_scope:
  product: GitHub Actions
  environment: GitHub repository with Actions enabled
status: draft
created: 2026-11-11
last_reviewed: null
review_due: null
sources:
  - id: SRC-GHA-WORKFLOW-SYNTAX
    url: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax
    title: Workflow syntax for GitHub Actions
    source_type: official
  - id: SRC-GHA-UNDERSTAND
    url: https://docs.github.com/en/actions/get-started/understand-github-actions
    title: Understanding GitHub Actions
    source_type: official
tags: [lab, workflow_dispatch, first-workflow, beginner]
related_documents: [GHA-FUND-001, GHA-REF-001]
---

# First GitHub Actions Workflow Using Manual Dispatch

## Objective

Create a minimal workflow, trigger it manually, and identify the workflow run, job, runner and step in the GitHub Actions UI.

## Safety

This lab runs only an `echo` command. It does not access secrets, deploy software or modify cloud resources. Use a personal/disposable repository if possible and follow your organization's repository policy.

## Prerequisites

- A GitHub repository where you are permitted to add workflow files.
- Git installed locally, or permission to create files through the GitHub web UI.
- GitHub Actions enabled for the repository.

## Step 1 — Create the workflow file

Create this path in the repository:

`.github/workflows/hello-ekos.yml`

Add:

```yaml
name: Hello EKOS

on:
  workflow_dispatch:

permissions:
  contents: read

jobs:
  hello:
    name: First learning job
    runs-on: ubuntu-latest
    steps:
      - name: Print a greeting
        run: echo "Hello from EKOS and GitHub Actions"

      - name: Show run context
        run: |
          echo "Repository: $GITHUB_REPOSITORY"
          echo "Commit: $GITHUB_SHA"
          echo "Runner OS: $RUNNER_OS"
```

## Step 2 — Commit the file

Commit the file to the repository's default branch. For this first exercise, using the default branch avoids introducing branch-specific workflow discovery questions.

## Step 3 — Trigger manually

1. Open the repository on GitHub.
2. Open the Actions tab.
3. Select `Hello EKOS`.
4. Select `Run workflow` if available.
5. Choose the branch and start the run.

Repository settings, permissions and workflow availability can affect whether the manual trigger is available.

## Step 4 — Inspect the run

Record:
- workflow name;
- run number and URL;
- triggering event;
- commit SHA;
- job name;
- runner label;
- step names;
- console output;
- final conclusion.

## Expected result

The run should contain one job with two steps. Both steps should succeed and display the expected greeting and context values.

## Step 5 — Explain what happened

Answer these questions in your experiment notes:

1. What is the difference between the workflow file and the workflow run?
2. What caused this workflow to start?
3. What does `runs-on: ubuntu-latest` select?
4. Why is `permissions: contents: read` declared?
5. Which values are supplied by the runner environment?
6. What would change if a second job were added?
7. Would a file created by one job automatically exist in another job?

## Evidence to capture

- Redacted screenshot of the workflow run summary.
- Run URL and commit SHA (do not include private repository details in public EKOS content).
- Relevant step output.
- Date and repository visibility type.
- Any deviations from the expected result.

## Completion criteria

- [ ] Workflow file committed under `.github/workflows/`.
- [ ] Manual workflow run started.
- [ ] Job and steps completed successfully.
- [ ] Run metadata recorded.
- [ ] Questions answered.
- [ ] Evidence reviewed and sensitive data removed.

After successful execution, update this document with the tested date/environment and change its status to `verified`. Do not mark it verified before the experiment is actually run.
