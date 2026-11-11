# EKOS — Engineering Knowledge Operating System

**Milestone 1: Foundation, architecture, knowledge standard and repository scaffold**

EKOS is a local-first engineering knowledge platform. Its permanent asset is a version-controlled, human-readable knowledge repository. Search and retrieval must work without an AI model or internet connection. A local LLM may be added later as an optional interface, never as a requirement for reading, searching, editing, exporting or backing up knowledge.

## Project goals

1. Preserve engineering knowledge in portable Markdown and YAML.
2. Organize knowledge consistently across technologies.
3. Make claims traceable to sources and distinguish documented, observed and verified facts.
4. Retrieve relevant knowledge offline using deterministic full-text search first.
5. Add semantic retrieval and a local LLM later without coupling the knowledge to either.
6. Build a durable learning asset that can be maintained as technologies evolve.

## Initial decisions

| Area | Decision |
|---|---|
| First technology | GitHub Actions |
| Encyclopedia scope | Balanced: fundamentals, feature reference, implementation, edge cases, troubleshooting and practical patterns |
| Initial mode | Fully offline; no AI or network dependency at runtime |
| Knowledge format | Markdown with YAML front matter |
| Source control | Git |
| Initial metadata/index store | SQLite |
| Initial search | SQLite FTS5 / BM25 |
| Future semantic search | Local embedding model + local vector index |
| Future local assistant | Optional Ollama or llama.cpp |
| UI/API (later milestone) | Next.js + Tailwind; Python + FastAPI |
| Primary platform | Windows development environment |

## Repository map

```text
ekos/
├── README.md
├── ARCHITECTURE.md
├── KNOWLEDGE-STANDARD.md
├── CONTRIBUTING.md
├── ROADMAP.md
├── CHANGELOG.md
├── LICENSE
├── .gitignore
├── config/
│   ├── taxonomy.yml
│   └── quality-gates.yml
├── schemas/
│   └── knowledge-document.schema.json
├── templates/
│   ├── topic.md
│   ├── feature-reference.md
│   ├── implementation-guide.md
│   ├── troubleshooting.md
│   ├── edge-case.md
│   ├── case-study.md
│   └── experiment-record.md
├── knowledge/
│   ├── README.md
│   ├── technologies/
│   │   └── github-actions/
│   │       ├── README.md
│   │       ├── MASTER-INDEX.md
│   │       ├── fundamentals/
│   │       ├── architecture/
│   │       ├── workflow-syntax/
│   │       ├── events-and-triggers/
│   │       ├── jobs-and-steps/
│   │       ├── expressions-and-contexts/
│   │       ├── runners/
│   │       ├── reusable-components/
│   │       ├── artifacts-and-caching/
│   │       ├── security/
│   │       ├── integrations/
│   │       ├── deployment/
│   │       ├── observability/
│   │       ├── troubleshooting/
│   │       ├── edge-cases/
│   │       ├── patterns/
│   │       └── case-studies/
│   ├── engineering-patterns/
│   └── glossary/
├── sources/
│   ├── README.md
│   └── source-register.yml
├── experiments/
│   └── README.md
├── code-examples/
│   └── README.md
├── tools/
│   ├── README.md
│   └── validate_knowledge.py
├── app/                         # Reserved for later milestones
│   ├── web/
│   └── api/
├── indexing/                    # Reserved for later milestones
│   ├── fts/
│   └── semantic/
├── tests/
│   ├── knowledge/
│   └── retrieval/
└── backups/
    └── README.md
```

## How to use the repository

### Add a knowledge document

1. Select the correct technology and category folder.
2. Copy the closest template from `templates/`.
3. Assign a unique, stable document ID.
4. Add source references and a version scope.
5. Mark the document `draft` until reviewed.
6. Validate metadata and links.
7. Review technical claims against primary sources.
8. Set `verified` only after the stated behavior or example has been tested.
9. Commit the document with a meaningful Git message.

### Search in the initial offline phase

The first search implementation will index Markdown files into SQLite FTS5. Search results must show:
- document title and ID;
- matching excerpt;
- category and tags;
- verification status;
- source references;
- relative file path.

The index is disposable and rebuildable. Markdown files are the source of truth.

### Runtime independence

The repository can be browsed with any text editor and searched with local command-line tools. No hosted service, API key, telemetry, or model download is required to use the knowledge.

## Quality principles

- Prefer official vendor documentation for product behavior.
- Never invent a feature, option, limit, error message or fix.
- Separate fact, inference, recommendation and experiment.
- Record the product/version scope for version-sensitive claims.
- Preserve exact error messages when available.
- Include diagnostic evidence and validation steps in troubleshooting entries.
- Record unresolved uncertainty explicitly.
- Respect licenses, copyright, terms of service and confidential information. Prefer original summaries and short quotations with attribution; do not mirror entire documentation sites.
- Never store secrets, credentials, customer data or proprietary source code without authorization.

## Milestones

See [`ROADMAP.md`](ROADMAP.md). Milestone 1 establishes the foundation. The next milestone begins the GitHub Actions encyclopedia with a source-backed master index and initial topic documents.

## Current status

**Milestone 1 — Foundation:** scaffold and standards defined.  
**Milestone 2 — GitHub Actions knowledge acquisition:** not started.

## Windows quick start

```powershell
# From the parent directory
Expand-Archive .\EKOS-Milestone-1.zip -DestinationPath .
Set-Location .\EKOS-Milestone-1

# Initialize Git
git init
git add .
git commit -m "chore: initialize EKOS knowledge foundation"
```

No Python packages or external services are required for the documentation repository itself.
