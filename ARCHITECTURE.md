# EKOS Architecture

## 1. Architectural vision

EKOS is a **local-first, knowledge-centred system**. The knowledge repository is the durable product; databases, indexes, UI components and language models are replaceable infrastructure.

### Non-negotiable architecture rules

1. Markdown/YAML files are canonical. Never make a database the only copy of knowledge.
2. Full-text search must work without an embedding model or LLM.
3. Local AI is optional and replaceable.
4. All generated answers must expose the documents and sources used.
5. Retrieval must not silently turn a weak match into a confident answer.
6. Indexes can always be rebuilt from canonical files.
7. Offline mode must not make network calls.
8. Version scope and review status must be visible.

## 2. Logical architecture

```text
                  LOCAL USER
                      |
              Next.js Web UI (later)
                      |
                FastAPI (later)
                      |
          +-----------+------------+
          |                        |
   Knowledge Services        Optional AI Adapter
          |                        |
   +------+------+           +-----+------+
   |      |      |           |            |
 Ingest  Search Metadata   Local LLM   Local Embeddings
   |      |      |           |            |
   +------+------|-----------+------------+
          |
   Retrieval / Answer Composer
          |
   Citations + confidence + gaps
          |
   Local response to user

Canonical storage (independent of application):
  Markdown + YAML + code examples + experiment records
          |
   Git version control
          |
   Rebuildable SQLite FTS5 index
          |
   Optional local vector index
```

## 3. Component responsibilities

| Component | Responsibility | Required in offline MVP? |
|---|---|---:|
| Knowledge repository | Canonical documents and examples | Yes |
| Metadata validator | Validate front matter and IDs | Yes |
| Ingestion/indexer | Parse files and build search index | Yes |
| SQLite FTS5 | Deterministic full-text retrieval | Yes |
| Search API | Query, filter, rank and return excerpts | Later |
| Knowledge UI | Browse, search and read | Later |
| Local embedding runtime | Semantic similarity | No |
| Vector index | Store local vectors | No |
| Local LLM adapter | Synthesize retrieved evidence | No |
| Evaluation suite | Measure retrieval quality | Introduce early; expand later |

## 4. Data flow

### Ingestion

1. Discover Markdown files under `knowledge/`.
2. Parse YAML front matter.
3. Validate required fields, allowed status and unique ID.
4. Extract title, headings, body, tags and source references.
5. Store document metadata and content in SQLite.
6. Populate FTS5 index.
7. Report invalid documents; do not silently index malformed metadata.

### Search

1. Accept a query and optional filters (technology, category, status, version).
2. Normalize query conservatively; preserve technical tokens and error strings.
3. Search FTS5.
4. Rank by relevance, with transparent boosts for exact IDs, titles and error strings.
5. Return excerpts and canonical paths.
6. Display status, version scope and sources.
7. If no strong result exists, say that the repository has no sufficiently supported answer.

### Future semantic retrieval

1. Chunk documents by headings, not arbitrary character windows where possible.
2. Keep document ID, heading path, version scope and source metadata with each chunk.
3. Generate embeddings locally.
4. Store vectors locally.
5. Combine lexical and semantic retrieval.
6. Deduplicate and rerank.
7. Preserve exact source links and document references.

### Future local RAG answer

1. Retrieve evidence.
2. Construct a prompt containing only retrieved passages and their IDs.
3. Ask the local model to answer using that evidence.
4. Require citations to EKOS document IDs and source references.
5. Validate that cited IDs exist in the retrieved set.
6. Display uncertainty and missing coverage.
7. Never claim that the model's answer is verified merely because it is fluent.

## 5. Suggested application stack

| Layer | Initial recommendation | Reason |
|---|---|---|
| UI | Next.js + Tailwind CSS | Familiar, flexible interface |
| API | Python + FastAPI | Strong parsing, search and ML ecosystem |
| Canonical content | Markdown + YAML | Portable and diff-friendly |
| Metadata/search DB | SQLite | Embedded, local and simple to back up |
| Full-text | SQLite FTS5 | No separate search server |
| Semantic search (future) | FAISS or Chroma | Local vector retrieval options |
| Embeddings (future) | Locally hosted embedding model | No remote API |
| Local LLM (future) | Ollama or llama.cpp | Replaceable local inference |
| Tests | pytest + Playwright | Backend and UI validation |
| Packaging | Native local process first; Docker Compose optional | Avoid unnecessary runtime complexity |

Do not introduce PostgreSQL, Redis, Kubernetes or a hosted vector database for the initial personal offline application unless measured requirements justify them.

## 6. Knowledge document model

Each document has:
- stable ID;
- title;
- technology;
- category and optional subcategory;
- content type;
- difficulty;
- product/version scope;
- status;
- created and reviewed dates;
- source references;
- tags;
- optional related document IDs;
- body with headings, examples, caveats and validation.

See `KNOWLEDGE-STANDARD.md` and `schemas/knowledge-document.schema.json`.

## 7. Trust and provenance model

Use these evidence labels in the body:

- **Officially documented:** supported by an authoritative source.
- **Experimentally verified:** reproduced in a recorded environment.
- **Community-reported:** reported by a community source, not independently verified.
- **Engineering recommendation:** reasoned guidance, not a vendor guarantee.
- **Unverified hypothesis:** plausible explanation requiring investigation.

A document's workflow status is separate:
- `draft`
- `reviewed`
- `verified`
- `deprecated`

`verified` means the document's stated testable claims or example were validated in the declared scope. It does not mean every possible variation is covered.

## 8. Security and privacy

- Keep the repository private if it contains internal operational knowledge.
- Exclude credentials, tokens, private keys, customer information and sensitive logs.
- Redact hostnames, account IDs, IP addresses and tenant details where appropriate.
- Do not ingest proprietary source code or internal documents unless policy permits it.
- Review third-party documentation licenses and website terms before bulk collection.
- Disable telemetry and outbound requests in offline mode.
- Treat imported documents and code as untrusted input.
- Back up the canonical repository and verify restore procedures.

## 9. Non-functional requirements

| Requirement | Target |
|---|---|
| Offline use | Core browse, search and edit workflows work without internet |
| Portability | Knowledge readable without EKOS |
| Rebuildability | Search indexes rebuilt from files |
| Traceability | Every technical guide has source metadata |
| Explainability | Search results show why they matched |
| Maintainability | Technology content independent of app code |
| Testability | Validator, indexer and retrieval have automated tests |
| Extensibility | New technology added by folder and metadata, not code changes |

## 10. Architecture decisions

- ADR-001: Markdown/YAML is the canonical knowledge format.
- ADR-002: SQLite FTS5 is the first retrieval engine.
- ADR-003: AI is optional; no LLM dependency in the offline MVP.
- ADR-004: Next.js and FastAPI are the planned application stack.
- ADR-005: Every answer must preserve document-level provenance.

## 11. Future evolution

M1: standards and repository scaffold  
M2: GitHub Actions research, source register and core knowledge documents  
M3: offline importer, metadata validation and FTS5 index  
M4: search UI and troubleshooting experience  
M5: local embeddings and hybrid retrieval  
M6: optional local LLM/RAG chat and evaluation harness
