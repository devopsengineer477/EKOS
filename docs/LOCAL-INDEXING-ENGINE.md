# EKOS Milestone 4 — Local Knowledge Indexing Engine

## Design
- Repository Markdown/YAML remains the source of truth.
- `tools/build_index.py` reads knowledge records and the source register.
- SQLite stores normalized document metadata, source links and relationships.
- SQLite FTS5 provides local full-text search; no hosted API or model is called.
- `tools/search.py` provides search, document detail, relationship and source navigation.
- The database is a rebuildable generated artifact at `data/ekos-index.sqlite3`.

## Windows quick start
```powershell
python --version
python tools/build_index.py
python tools/search.py search runner
python tools/search.py search workflow --technology github-actions --status reviewed
python tools/search.py show GHA-ARCH-001
python tools/search.py sources
```

## Automated tests
```powershell
python -m unittest discover -s tests -v
```

## Search behavior
Search terms are tokenized and combined with AND semantics. Filters include `--technology`, `--category`, and `--status`. Limit result count with `--limit 20`. Search is lexical/full-text, not semantic: synonyms and conceptual similarity are not inferred.

## Rebuild and freshness
Run `python tools/build_index.py` after adding or editing knowledge documents or the source register. Rebuilding replaces the generated index from the repository source files. The Markdown documents are never modified by indexing.

## SQLite / FTS5 requirement
Python must be linked to SQLite with FTS5 enabled. Most current official Python Windows builds include it. If index creation reports that FTS5 is unavailable, install a Python distribution whose SQLite build includes FTS5; no Python package install is otherwise needed.

## Limitations
- The front-matter reader supports the EKOS metadata subset, not arbitrary YAML.
- Relationship links are read from `related_documents`; missing target IDs are not inserted as document records.
- Source URLs are displayed as references; the tool does not fetch or validate them.
- This milestone is a CLI engine, not yet a graphical chat application.
