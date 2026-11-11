# EKOS Knowledge Quality Gate

## Checks performed
- Front matter exists and has a closing delimiter.
- Required metadata fields: `id`, `title`, `technology`, `status`, `last_reviewed`, `sources`.
- Document IDs follow uppercase, hyphen-separated format and are unique.
- Status is one of `draft`, `reviewed`, `verified`, `deprecated`.
- `last_reviewed` uses ISO `YYYY-MM-DD` format.
- Every source ID in a document exists in `sources/source-register.yml`.
- Each knowledge record has at least three second-level sections and at least one source.
- Relative Markdown links resolve to existing local files.

README and `MASTER-INDEX.md` files are treated as navigation pages and excluded from atomic-record checks.

## Commands (Windows PowerShell)
```powershell
python tools/validate_knowledge.py
python tools/validate_knowledge.py --strict
python tools/validate_knowledge.py --json
```

## Exit codes
- `0`: passed (warnings are informational unless `--strict` is used)
- `1`: errors found, or warnings found in strict mode

## Limitations
The parser intentionally supports the simple YAML front-matter subset currently used in EKOS; it is not a complete YAML parser and does not validate arbitrary nested YAML structures. It checks source IDs, not remote URL availability or claim accuracy. It does not execute workflow examples. A passing gate is not equivalent to technical review or live verification.
