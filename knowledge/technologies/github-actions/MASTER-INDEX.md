# GitHub Actions — Encyclopedia Master Index

Status legend: `[ ]` not started · `[~]` researching/draft · `[R]` reviewed · `[V]` verified

This is a coverage map, not a claim that every item is fully documented. Add document IDs and source references as topics are authored.

## 01. Fundamentals
- [ ] What GitHub Actions is and when to use it
- [ ] CI, CD and workflow automation concepts
- [ ] Core terminology: workflow, event, job, step, action, runner
- [ ] Repository, organization and enterprise scope
- [ ] GitHub Actions limits, quotas and billing concepts (version/date-sensitive)
- [ ] GitHub-hosted versus self-hosted execution

## 02. Architecture and execution lifecycle
- [ ] Workflow discovery and event dispatch
- [ ] Job scheduling and dependency graph
- [ ] Runner allocation and lifecycle
- [ ] Step execution and shell behavior
- [ ] Job completion, outputs and cleanup
- [ ] Cancellation, timeout and retry behavior
- [ ] Logs, status and check runs
- [ ] Service architecture: documented public model versus implementation details

## 03. Workflow syntax and YAML
- [ ] Workflow file location and naming
- [ ] Top-level keys and schema
- [ ] `name`, `run-name`, `on`, `permissions`
- [ ] `env`, `defaults`, `concurrency`
- [ ] `jobs`, `uses`, `run`, `with`
- [ ] `needs`, `if`, `continue-on-error`, `timeout-minutes`
- [ ] YAML quoting, booleans, arrays and mapping pitfalls
- [ ] Workflow validation and linting

## 04. Events and triggers
- [ ] `push`, `pull_request`, `pull_request_target`
- [ ] `workflow_dispatch`, `workflow_call`
- [ ] `schedule`, `workflow_run`
- [ ] `repository_dispatch`
- [ ] Release, issue, comment and review events
- [ ] Branch and tag filters
- [ ] Path filters and their limitations
- [ ] Activity types and event payloads
- [ ] Default branch and workflow availability requirements
- [ ] Fork and permission behavior
- [ ] Duplicate and overlapping triggers

## 05. Jobs and steps
- [ ] Job dependencies with `needs`
- [ ] Parallel jobs and DAG design
- [ ] Job outputs and step outputs
- [ ] Conditions and status-check functions
- [ ] Environment variables and environment files
- [ ] Shell selection and working directories
- [ ] Containers and service containers
- [ ] Timeouts, cancellation and continue-on-error
- [ ] Job-level versus step-level configuration

## 06. Expressions and contexts
- [ ] Expression syntax and evaluation
- [ ] `github`, `env`, `vars`, `secrets`
- [ ] `job`, `jobs`, `steps`, `runner`, `strategy`, `matrix`, `needs`
- [ ] `inputs` and `outputs`
- [ ] Functions: `contains`, `startsWith`, `endsWith`, `format`, `join`, `toJSON`, `fromJSON`
- [ ] Status functions: `success`, `failure`, `always`, `cancelled`
- [ ] Property dereferencing and index syntax
- [ ] Null, empty string, boolean and numeric coercion
- [ ] Expression injection and safe handling of untrusted input

## 07. Runners
- [ ] GitHub-hosted runner model
- [ ] Runner images and software inventory
- [ ] Self-hosted runner architecture
- [ ] Runner registration and lifecycle
- [ ] Labels and routing
- [ ] Runner groups and access controls
- [ ] Ephemeral and autoscaled runners
- [ ] Windows, Linux and macOS differences
- [ ] Network access, proxies and certificates
- [ ] Workspace cleanup and persistence
- [ ] Runner security and isolation
- [ ] Troubleshooting offline, busy and lost runners

## 08. Reusable components
- [ ] Marketplace actions and action metadata
- [ ] JavaScript actions
- [ ] Docker container actions
- [ ] Composite actions
- [ ] Reusable workflows
- [ ] Inputs, outputs and secrets
- [ ] Version pinning and update strategy
- [ ] Nested reuse and recursion/limits (verify current rules)
- [ ] Local actions and repository checkout
- [ ] Testing and debugging custom actions

## 09. Artifacts and caching
- [ ] Upload and download artifacts
- [ ] Artifact naming and cross-job transfer
- [ ] Retention and expiration
- [ ] Cache keys and restore keys
- [ ] Cache scope and access restrictions
- [ ] Cache invalidation
- [ ] Dependency caching patterns
- [ ] Artifact integrity and provenance
- [ ] Large files and performance considerations

## 10. Security
- [ ] `GITHUB_TOKEN` permissions and least privilege
- [ ] Workflow/job permissions
- [ ] Secrets scopes and inheritance
- [ ] OIDC concepts and token claims
- [ ] AWS IAM OIDC trust policies
- [ ] Forked pull request security
- [ ] `pull_request_target` risks
- [ ] Script injection
- [ ] Third-party action pinning
- [ ] Supply-chain security and attestations
- [ ] Self-hosted runner threat model
- [ ] Environment protection and approvals
- [ ] Secret masking limitations
- [ ] Secure artifact handling
- [ ] Security review checklist

## 11. Integrations
- [ ] AWS authentication and deployment
- [ ] Azure authentication and deployment
- [ ] Google Cloud authentication and deployment
- [ ] Docker build and registry push
- [ ] Kubernetes deployment
- [ ] Terraform plan/apply workflows
- [ ] Package registries
- [ ] Test reporting and coverage
- [ ] Jira and issue-tracker integration
- [ ] Notifications and chat integrations
- [ ] GitHub API and CLI (`gh`)

## 12. Deployment and release engineering
- [ ] Build/test/package pipeline
- [ ] Environment promotion
- [ ] Deployment approvals and protection
- [ ] Release creation and tagging
- [ ] Semantic versioning
- [ ] Deployment concurrency
- [ ] Rollback and recovery
- [ ] Blue/green and canary patterns
- [ ] Multi-account and multi-region deployment
- [ ] Artifact promotion versus rebuild

## 13. Observability and debugging
- [ ] Workflow logs and annotations
- [ ] Debug logging
- [ ] Step summaries
- [ ] Job summaries and reports
- [ ] Workflow visualization
- [ ] API-based run inspection
- [ ] Failure triage workflow
- [ ] Monitoring workflow health
- [ ] Retention and auditability

## 14. Enterprise governance
- [ ] Organization and enterprise policies
- [ ] Allowed actions and reusable workflow policy
- [ ] Runner group governance
- [ ] Centralized workflow patterns
- [ ] Repository onboarding
- [ ] Policy as code
- [ ] Audit and compliance evidence
- [ ] Cost and usage governance
- [ ] Disaster recovery and continuity

## 15. Performance and reliability
- [ ] Matrix sizing and fan-out/fan-in
- [ ] Concurrency groups
- [ ] Cache effectiveness
- [ ] Artifact transfer overhead
- [ ] Runner capacity planning
- [ ] Flaky workflow diagnosis
- [ ] Idempotency
- [ ] Retry strategy and backoff
- [ ] Rate limits and API throttling
- [ ] Queue delays and bottleneck analysis

## 16. Troubleshooting catalogue
- [ ] Workflow not triggered
- [ ] Invalid workflow YAML
- [ ] Expression/context evaluation errors
- [ ] Permission denied / insufficient token scope
- [ ] Secret unavailable or empty
- [ ] OIDC token/trust failure
- [ ] Runner unavailable or offline
- [ ] Checkout/authentication failure
- [ ] Dependency installation failure
- [ ] Cache miss or stale cache
- [ ] Artifact upload/download failure
- [ ] Docker build/push failure
- [ ] AWS S3/ECR/ECS deployment failure
- [ ] Timeout and cancellation
- [ ] Matrix-only failure
- [ ] Windows/Linux shell differences
- [ ] Network, DNS, proxy and certificate failures

## 17. Edge cases and failure engineering
- [ ] Concurrent pushes to the same branch
- [ ] Cancellation while deployment is running
- [ ] Partial matrix failure
- [ ] Missing optional outputs
- [ ] Empty and null inputs
- [ ] Special characters in expressions and shell values
- [ ] Paths containing spaces
- [ ] Case sensitivity differences
- [ ] Forked PR and trusted/untrusted context boundaries
- [ ] Workflow re-run and stale artifacts
- [ ] Duplicate event delivery / idempotency
- [ ] Long-running jobs and runner interruption
- [ ] Branch deletion and renamed branches
- [ ] Tag and release race conditions

## 18. Quality engineering patterns
- [ ] Unit, integration and end-to-end test stages
- [ ] Test sharding and matrix strategy
- [ ] Browser test execution
- [ ] API and contract testing
- [ ] Database migration validation
- [ ] Test data setup and cleanup
- [ ] Flaky test quarantine
- [ ] Coverage and test report publication
- [ ] Security scan gates
- [ ] Quality gates and release readiness

## 19. Practical case studies
- [ ] .NET build, test and package
- [ ] Python pytest pipeline
- [ ] Playwright cross-browser pipeline
- [ ] Newman API testing
- [ ] Docker image build and ECR push
- [ ] AWS ECS/Fargate deployment
- [ ] Angular static site deployment to S3/CloudFront
- [ ] Terraform plan with approval and apply
- [ ] Self-hosted Windows runner
- [ ] Reusable enterprise CI template

## 20. Reference and glossary
- [ ] YAML key reference
- [ ] Context and expression reference
- [ ] Event payload reference
- [ ] Runner labels and environments
- [ ] Environment variable reference
- [ ] CLI and API reference
- [ ] Limits and quotas reference
- [ ] Glossary
- [ ] Official links and release-note index

## Coverage register

| Metric | Current |
|---|---:|
| Topics listed | 200+ |
| Documents authored | 0 |
| Reviewed documents | 0 |
| Verified examples | 0 |
| Open research gaps | To be assessed |

Update this table as documents are created. Do not count an index bullet as completed knowledge.
