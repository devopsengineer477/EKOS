---
id: GHA-RUN-001
title: GitHub Actions Runner Types and Job Routing
technology: github-actions
category: runners
subcategory: runner-types-and-routing
content_type: technical-guide
difficulty: intermediate
version_scope:
  product: GitHub Actions
  reviewed_against: GitHub Docs as accessed 2026-11-11
status: reviewed
created: 2026-11-11
last_reviewed: 2026-11-11
review_due: 2027-02-11
sources:
  - id: SRC-GHA-HOSTED-RUNNERS
    url: https://docs.github.com/en/actions/concepts/runners/github-hosted-runners
    title: GitHub-hosted runners
    source_type: official
  - id: SRC-GHA-SELFHOSTED-REF
    url: https://docs.github.com/en/actions/reference/runners/self-hosted-runners
    title: Self-hosted runners reference
    source_type: official
  - id: SRC-GHA-CHOOSE-RUNNER
    url: https://docs.github.com/en/actions/how-tos/write-workflows/choose-where-workflows-run/choose-the-runner-for-a-job
    title: Choosing the runner for a job
    source_type: official
  - id: SRC-GHA-ARC
    url: https://docs.github.com/en/actions/concepts/runners/actions-runner-controller
    title: Actions Runner Controller
    source_type: official
tags: [runners, github-hosted, self-hosted, labels, groups, windows, linux, macos]
related_documents: [GHA-ARCH-001, GHA-ARCH-002]
---

# GitHub Actions Runner Types and Job Routing

## Summary

A runner is the machine or execution environment that runs a GitHub Actions job. The two principal operating models are GitHub-hosted runners and self-hosted runners. The job's `runs-on` configuration selects the runner requirements.

## GitHub-hosted runners

GitHub provides hosted runner environments with operating systems, tools and packages. A standard hosted job receives a newly provisioned virtual machine, and the machine is decommissioned after the job completes. GitHub maintains the hosted image environment.

Typical labels include:
- `ubuntu-latest`;
- `windows-latest`;
- `macos-latest`;
- version-specific labels such as `ubuntu-24.04` or `windows-2022` where currently available.

Do not assume `-latest` means a fixed image. It is a moving label and can change as GitHub updates the hosted image. For reproducibility-sensitive pipelines, evaluate version-specific labels and monitor image deprecation announcements.

### Basic example

```yaml
jobs:
  build:
    runs-on: windows-2022
    steps:
      - uses: actions/checkout@v4
      - name: Show OS
        shell: pwsh
        run: |
          Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion
```

Action versions in examples are illustrative. For production, review the action's security posture and pinning policy; the current recommended pinning approach is covered in the security module.

## Self-hosted runners

A self-hosted runner is a machine that you deploy and manage. It may run on-premises, in a data centre, on a cloud VM or in another supported environment.

Typical reasons to use one:
- access to private network resources;
- specialized hardware or installed software;
- controlled build environment;
- custom capacity or operating-system configuration;
- integration with internal systems.

You own the operational responsibilities:
- OS patching and hardening;
- runner software lifecycle;
- toolchain installation;
- network and proxy configuration;
- monitoring and capacity;
- workspace cleanup;
- isolation between jobs;
- incident response and credential protection.

A self-hosted runner is not automatically safer merely because it is inside a private network. It can expose internal systems if untrusted workflows or pull requests are allowed to execute on it.

## Runner selection with `runs-on`

GitHub-hosted runner:

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
```

Self-hosted runner using labels:

```yaml
jobs:
  integration-tests:
    runs-on: [self-hosted, windows, x64, integration]
```

When an array of labels is used, the runner must match all specified labels. Runner groups can also be used to control access and routing.

## Job scheduling and queued state

For self-hosted runners, a matching online and idle runner must be available. If no eligible runner is available, the job remains queued. A runner that is online but has the wrong labels is not a match.

A useful first diagnostic is to compare:
1. the job's `runs-on` values;
2. the runner's actual labels;
3. the runner group access configuration;
4. the runner's online/busy status.

GitHub's current self-hosted runner reference documents routing behavior and queue conditions. Check it when diagnosing exact timing/limits because these can change.

## GitHub-hosted versus self-hosted decision matrix

| Requirement | Prefer hosted | Consider self-hosted |
|---|---:|---:|
| Standard Linux/Windows/macOS CI | Yes | Sometimes |
| No desire to maintain runner machines | Yes | No |
| Private network access | Depends on available product options | Yes |
| Specialized licensed software or hardware | Depends on availability/licensing | Often |
| Highly controlled ephemeral build hosts | Evaluate hosted options | Possible with ephemeral/autoscaled design |
| Internal legacy integration | Depends on connectivity | Often |
| Untrusted fork PR execution | Use secure hosted isolation and event design | Avoid exposing persistent self-hosted infrastructure |

## Self-hosted runner security checklist

- Use ephemeral runners for untrusted or high-risk workloads where feasible.
- Do not run untrusted pull request code on a persistent runner with access to secrets or internal networks.
- Restrict which repositories can use runner groups.
- Separate runners by trust level and workload.
- Avoid storing long-lived cloud credentials on the runner.
- Clean workspaces and temporary credentials after each job.
- Patch the host and runner application.
- Restrict inbound access; allow only required outbound connectivity.
- Monitor runner service health and host security.
- Treat caches and artifacts as potential data-exfiltration channels.

## Scaling options

For larger fleets, organizations can implement autoscaling. GitHub documents Actions Runner Controller (ARC), a Kubernetes operator that manages runner scale sets. ARC is not a prerequisite for self-hosted runners and should only be introduced when the team has Kubernetes operational capability and a scaling requirement.

## Relevance to a Windows automation environment

For .NET/MSBuild/MSTest/VSTest workloads requiring Windows-specific tools, a Windows self-hosted runner can provide a controlled toolchain and access to internal test systems. However, it also means the team owns host patching, runner isolation, cleanup, capacity and security.

A practical design separates:
- build/test runner pool;
- deployment runner pool;
- privileged infrastructure runner pool.

Use separate runner groups/labels and permission boundaries where appropriate. Do not give every build job deployment credentials.

## Troubleshooting

| Symptom | First checks |
|---|---|
| Job stays queued | `runs-on`, labels, groups, online/idle status |
| Runner shows offline | Service/process, host connectivity, outbound HTTPS, proxy/DNS |
| Job assigned to wrong machine | Label overlap and runner group design |
| Docker/service container job fails on self-hosted | OS and Docker prerequisites |
| Job sees stale files | Workspace cleanup and isolation |
| Tool version differs | Hosted image inventory or self-hosted provisioning scripts |
| Runner compromised | Isolate host, revoke credentials, inspect logs, rebuild from trusted image |

## Sources

- SRC-GHA-HOSTED-RUNNERS
- SRC-GHA-SELFHOSTED-REF
- SRC-GHA-CHOOSE-RUNNER
- SRC-GHA-ARC
