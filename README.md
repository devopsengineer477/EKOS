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


## First GitHub Actions learning path

Read these documents in order:

1. `knowledge/technologies/github-actions/fundamentals/GHA-FUND-001-what-is-github-actions.md`
2. `knowledge/technologies/github-actions/architecture/GHA-ARCH-001-core-components-and-architecture.md`
3. `knowledge/technologies/github-actions/architecture/GHA-ARCH-002-workflow-run-lifecycle.md`
4. `knowledge/technologies/github-actions/runners/GHA-RUN-001-runner-types-and-job-routing.md`
5. `knowledge/technologies/github-actions/workflow-syntax/GHA-REF-001-minimal-workflow-syntax.md`

Update the technology master index as topics are researched, reviewed and experimentally verified. Do not mark examples verified until they have been run in the stated environment.

The first practical lab is `experiments/github-actions/EXP-GHA-001-manual-dispatch.md`. Its starter workflow is also available at `code-examples/github-actions/hello-ekos.yml`. Run it in a disposable repository and only then change the experiment status to `verified`.


## Milestone 3 — Knowledge Quality Gate

The validator now checks:
- YAML front matter presence and required metadata fields
- Document ID format and duplicate IDs
- Allowed lifecycle statuses
- `last_reviewed` date format
- Source IDs against `sources/source-register.yml`
- Required document sections
- Broken relative Markdown links

### Run validation (Windows PowerShell)
```powershell
python --version
python tools/validate_knowledge.py
python tools/validate_knowledge.py --strict
python tools/validate_knowledge.py --json
```
No virtual environment or third-party dependencies are required.

### What the gate does not prove
A passing result confirms repository structure and reference integrity only. It does not fact-check technical claims, fully parse every YAML feature, execute code examples, or verify a live GitHub Actions workflow. Keep `reviewed` and `verified` statuses distinct.


## Quality-gate behavior and limitations

The validator supports EKOS's existing nested source metadata format (`sources: - id: ...`) and skips repository/technology README and master-index navigation pages. A successful run confirms structural consistency only; it does not fact-check content or run GitHub workflows.


## Milestone 4 — Local Knowledge Indexing Engine

EKOS now includes a local SQLite + FTS5 index and command-line search/navigation tools. The Markdown/YAML repository remains the source of truth; the SQLite database is generated and rebuildable.

### Build the index
```powershell
python tools/build_index.py
```

### Search and filter
```powershell
python tools/search.py search runner
python tools/search.py search workflow --technology github-actions --category architecture --status reviewed --limit 10
```

### Open document relationships and sources
```powershell
python tools/search.py show GHA-ARCH-001
python tools/search.py sources
python tools/search.py sources --query runner
```

### Run automated tests
```powershell
python -m unittest discover -s tests -v
```

No external AI provider or third-party Python package is required. Python's SQLite build must include FTS5. Rebuild the index after changing knowledge documents or the source register.


## Milestone 5 — Local Knowledge Explorer

EKOS now has a browser-based local UI served by Python's standard-library HTTP server. It uses the SQLite/FTS5 index from Milestone 4.

### Start the application (Windows PowerShell)
```powershell
.\run-ekos.ps1
```
Then open **http://127.0.0.1:8765** in your browser. Stop the server with Ctrl+C.

Alternatively:
```powershell
python tools/build_index.py
python app/server.py
```

### Included UI capabilities
- Full-text knowledge search and quick-search suggestions
- Technology, category and status filters
- Document viewer with basic Markdown rendering
- Related-document explorer
- Source library and external source links
- Retrieval-ready “Ask EKOS” panel that returns evidence documents without generating AI answers
- Local index health and document/source counts

### API endpoints
`/api/health`, `/api/search`, `/api/filters`, `/api/documents/<document-id>`, `/api/sources`.

### Run tests
```powershell
python -m unittest discover -s tests -v
python tools/validate_knowledge.py
```

No external AI provider, Node.js, npm or third-party Python package is required. The server binds to localhost only. Do not expose it to a network without adding production-grade security controls.
