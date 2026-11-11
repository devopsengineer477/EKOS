# EKOS Milestone 5 — Local Knowledge Explorer

## Overview
Milestone 5 adds a browser UI served only on `127.0.0.1`. It uses the Milestone 4 SQLite/FTS5 index and Python standard-library HTTP server. No JavaScript package manager, framework, external service or AI provider is required.

## Start on Windows
Recommended:
```powershell
.\run-ekos.ps1
```
Or:
```powershell
python tools/build_index.py
python app/server.py
```
Open `http://127.0.0.1:8765`. Stop with Ctrl+C.

## Features
- Full-text search and quick search suggestions
- Technology, category and document-status filters
- Document viewer with basic Markdown rendering
- Related-document navigation
- Registered source navigation with external source links
- Retrieval-ready question box that returns matching evidence documents, not generated answers
- Local index health/count display

## API endpoints
- `GET /api/health`
- `GET /api/search?q=runner&technology=github-actions&category=runners&status=reviewed&limit=20`
- `GET /api/filters`
- `GET /api/documents/GHA-ARCH-001`
- `GET /api/sources?q=runner`

## Security and privacy
- The server binds to `127.0.0.1`, not `0.0.0.0`; it is intended for the same computer only.
- The SQLite database is opened read-only by the web server.
- Document IDs are validated before lookup.
- Static file serving is restricted to the three bundled UI assets.
- Source links are opened in a new tab with `noopener noreferrer`.
- Do not expose this development server to a LAN or public network. Add authentication, TLS and production-grade security before remote deployment.

## Retrieval-ready interface
The “Ask EKOS” panel accepts a natural-language question and retrieves documents using FTS5 keyword matching. It deliberately does not synthesize an answer. A later optional local-model milestone can use retrieved documents as grounded context.

## Automated tests
```powershell
python -m unittest discover -s tests -v
python tools/validate_knowledge.py
```

## Known limitations
- Search is lexical, not semantic; query terms are AND-matched.
- Markdown rendering is lightweight, not a full CommonMark implementation.
- The chat-ready panel retrieves evidence but does not generate a conversational answer.
- This is a local development application, not a hardened multi-user production deployment.
