# EKOS Roadmap

## M1 — Foundation (current)

- [x] Project purpose and offline-first principles
- [x] Logical architecture
- [x] Knowledge documentation standard
- [x] Repository scaffold
- [x] GitHub Actions master index
- [x] Reusable templates
- [x] Metadata schema
- [x] Initial validation utility

## M2 — GitHub Actions encyclopedia

- [x] Establish official source register
- [x] Map the initial product documentation taxonomy
- [x] Research and document fundamentals and architecture (five reviewed documents)
- [~] Document minimal workflow syntax; detailed syntax and event catalog remain
- [ ] Document jobs, steps, expressions and contexts
- [ ] Document runners and reusable components
- [ ] Document artifacts, caching and security
- [ ] Document integrations and deployment patterns
- [ ] Build troubleshooting and edge-case catalogue
- [ ] Verify selected examples in a test repository (GHA-EXP-001 is ready to run)

## M3 — Offline ingestion and search

- [ ] Markdown/YAML parser
- [ ] Metadata validation in CI
- [ ] SQLite schema and migrations
- [ ] FTS5 index builder
- [ ] Search ranking and filters
- [ ] Search evaluation dataset
- [ ] Rebuild and backup/restore tests

## M4 — Local application

- [ ] FastAPI search endpoints
- [ ] Next.js knowledge explorer
- [ ] Search result excerpts and citations
- [ ] Technology/category/status filters
- [ ] Troubleshooting view
- [ ] Import and re-index workflow

## M5 — Semantic retrieval

- [ ] Local embedding runtime
- [ ] Heading-aware chunking
- [ ] Local vector index
- [ ] Hybrid lexical + semantic retrieval
- [ ] Retrieval evaluation and tuning

## M6 — Optional local assistant

- [ ] Local LLM adapter
- [ ] Evidence-grounded answer prompts
- [ ] Citation validation
- [ ] Abstention when evidence is insufficient
- [ ] Conversation context kept local
- [ ] Offline/network-isolation tests

## Definition of done for a technology encyclopedia

A technology is not complete merely because its table of contents is large. Completion requires:
- taxonomy mapped against authoritative documentation;
- core features documented;
- key configuration/reference topics covered;
- practical examples;
- common failure modes and edge cases;
- security and operational considerations;
- sources and version scope;
- validation evidence for selected examples;
- coverage gaps explicitly recorded.


### M2 Phase 1 — completed deliverables

- [x] GHA-FUND-001 — What Is GitHub Actions?
- [x] GHA-ARCH-001 — Core Components and Conceptual Architecture
- [x] GHA-ARCH-002 — Workflow Run and Job Execution Lifecycle
- [x] GHA-RUN-001 — Runner Types and Job Routing
- [x] GHA-REF-001 — Minimal Workflow Syntax Reference

Phase 1 documents are source-reviewed. Practical workflow examples remain unverified until executed in a disposable GitHub repository.
