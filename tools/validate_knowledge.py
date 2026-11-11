#!/usr/bin/env python3
"""EKOS Knowledge Quality Gate — standard-library-only structural validator."""
from __future__ import annotations
import argparse, json, re, sys
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
SOURCE_REGISTER = ROOT / "sources" / "source-register.yml"
ALLOWED_STATUS = {"draft", "reviewed", "verified", "deprecated"}
REQUIRED_FIELDS = ("id", "title", "technology", "status", "last_reviewed", "sources")
ID_RE = re.compile(r"^[A-Z0-9]+(?:-[A-Z0-9]+)*$")

def parse_front_matter(text):
    """Read the simple YAML subset used by EKOS, including nested source objects."""
    if not text.startswith("---\n"):
        return None, "missing YAML front matter"
    end = text.find("\n---", 4)
    if end < 0:
        return None, "unterminated YAML front matter"
    block = text[4:end]
    data, current_key, in_sources = {}, None, False
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if stripped.startswith("- ") and in_sources:
            # Source entries are mappings; collect their id field.
            m = re.match(r"-\s*id:\s*(.+?)\s*$", stripped)
            if m:
                data.setdefault("sources", []).append(m.group(1).strip("'\""))
            continue
        if raw[:1].isspace() and in_sources:
            continue
        if ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        key, value = key.strip(), value.strip()
        current_key = key
        in_sources = key == "sources"
        if in_sources:
            data["sources"] = []
        elif value.startswith("[") and value.endswith("]"):
            data[key] = [x.strip().strip("'\"") for x in value[1:-1].split(",") if x.strip()]
        elif value:
            data[key] = value.strip("'\"")
        else:
            data[key] = None
    return data, None

def get_source_ids():
    if not SOURCE_REGISTER.exists():
        return set(), ["source register not found"]
    content = SOURCE_REGISTER.read_text(encoding="utf-8")
    ids = set(re.findall(r"^\s*-\s*id:\s*([A-Za-z0-9_-]+)\s*$", content, re.M))
    return ids, []

def validate():
    errors, warnings, docs = [], [], []
    registered, source_errors = get_source_ids()
    errors.extend(source_errors)
    if not KNOWLEDGE.exists():
        return {"errors": ["knowledge directory not found"], "warnings": [], "documents": []}
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        # Indexes and README files are navigation/overview pages, not atomic knowledge records.
        if path.name.upper() in {"MASTER-INDEX.MD", "README.MD"}:
            continue
        text = path.read_text(encoding="utf-8")
        meta, parse_error = parse_front_matter(text)
        rel = path.relative_to(ROOT).as_posix()
        if parse_error:
            errors.append(f"{rel}: {parse_error}")
            continue
        missing = [k for k in REQUIRED_FIELDS if k not in meta or meta[k] in ("", None, [])]
        if missing:
            errors.append(f"{rel}: missing required metadata: {', '.join(missing)}")
        doc_id = meta.get("id", "")
        if doc_id and not ID_RE.fullmatch(str(doc_id)):
            errors.append(f"{rel}: invalid ID format '{doc_id}'")
        status = meta.get("status")
        if status and status not in ALLOWED_STATUS:
            errors.append(f"{rel}: invalid status '{status}'")
        if meta.get("last_reviewed"):
            try:
                date.fromisoformat(str(meta["last_reviewed"]))
            except ValueError:
                errors.append(f"{rel}: last_reviewed must use YYYY-MM-DD")
        for sid in meta.get("sources", []) if isinstance(meta.get("sources"), list) else []:
            if sid not in registered:
                errors.append(f"{rel}: source ID '{sid}' is not in source register")
        # Accept established EKOS document structures: Purpose or Summary, plus
        # a minimum of three second-level headings to avoid imposing one rigid outline.
        h2 = re.findall(r"(?m)^##\s+(.+?)\s*$", text)
        if len(h2) < 3:
            errors.append(f"{rel}: expected at least 3 second-level sections; found {len(h2)}")
        if not any(x.strip().lower() in {"purpose", "summary"} for x in h2):
            warnings.append(f"{rel}: consider adding a 'Purpose' or 'Summary' section")
        if not meta.get("sources"):
            errors.append(f"{rel}: at least one source ID is required")
        # Validate relative links; anchors and external links are intentionally skipped.
        for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local = target.split("#", 1)[0]
            if local and not (path.parent / local).resolve().exists():
                errors.append(f"{rel}: broken local link '{target}'")
        docs.append({"path": rel, "id": doc_id, "status": status})
    seen = {}
    for doc in docs:
        if doc["id"]:
            seen.setdefault(doc["id"], []).append(doc["path"])
    for doc_id, paths in seen.items():
        if len(paths) > 1:
            errors.append(f"duplicate document ID '{doc_id}': " + ", ".join(paths))
    return {"errors": errors, "warnings": warnings, "documents": docs}

def main():
    parser = argparse.ArgumentParser(description="Validate EKOS knowledge records.")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    parser.add_argument("--json", action="store_true", help="Print JSON for CI integration.")
    args = parser.parse_args()
    result = validate()
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("EKOS Knowledge Quality Gate")
        print(f"Knowledge documents scanned: {len(result['documents'])}")
        print(f"Errors: {len(result['errors'])} | Warnings: {len(result['warnings'])}")
        for e in result["errors"]: print(f"ERROR: {e}")
        for w in result["warnings"]: print(f"WARNING: {w}")
        if not result["errors"] and not (args.strict and result["warnings"]):
            print("EKOS quality gate passed.")
    return 1 if result["errors"] or (args.strict and result["warnings"]) else 0

if __name__ == "__main__":
    sys.exit(main())
