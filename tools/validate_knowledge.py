#!/usr/bin/env python3
"""Dependency-free EKOS front-matter and ID validator.

This initial validator intentionally checks a small, reliable subset. It does not
attempt to fully parse YAML. Use a proper YAML parser in the application milestone.
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge"
REQUIRED = {
    "id", "title", "technology", "category", "content_type",
    "difficulty", "status", "created", "sources", "tags"
}
ALLOWED_STATUS = {"draft", "reviewed", "verified", "deprecated"}
ID_RE = re.compile(r"^[A-Z0-9-]+$")


def parse_front_matter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None, "Missing YAML front matter opening delimiter"
    end = text.find("\n---\n", 4)
    if end < 0:
        return None, "Missing YAML front matter closing delimiter"
    block = text[4:end]
    fields = {}
    for line in block.splitlines():
        if not line or line.lstrip().startswith("#") or line.startswith(" "):
            continue
        match = re.match(r"^([A-Za-z0-9_-]+):(?:\s*(.*))?$", line)
        if match:
            fields[match.group(1)] = (match.group(2) or "").strip().strip('"').strip("'")
    return fields, None


def main():
    errors = []
    seen = {}
    docs = sorted(KNOWLEDGE.rglob("*.md"))
    for path in docs:
        fields, error = parse_front_matter(path)
        if error:
            # Index and README files are allowed to be plain Markdown.
            if path.name in {"README.md", "MASTER-INDEX.md"}:
                continue
            errors.append(f"{path.relative_to(ROOT)}: {error}")
            continue
        missing = REQUIRED - set(fields)
        if missing:
            errors.append(f"{path.relative_to(ROOT)}: missing fields: {', '.join(sorted(missing))}")
            continue
        doc_id = fields["id"]
        if not ID_RE.match(doc_id):
            errors.append(f"{path.relative_to(ROOT)}: invalid ID {doc_id!r}")
        if doc_id in seen:
            errors.append(f"Duplicate ID {doc_id}: {seen[doc_id]} and {path.relative_to(ROOT)}")
        else:
            seen[doc_id] = path.relative_to(ROOT)
        if fields["status"] not in ALLOWED_STATUS:
            errors.append(f"{path.relative_to(ROOT)}: invalid status {fields['status']!r}")
        for key in ("title", "technology", "category", "content_type", "difficulty", "created"):
            if not fields[key]:
                errors.append(f"{path.relative_to(ROOT)}: empty required field {key}")

    if errors:
        print("EKOS validation failed:")
        for item in errors:
            print(f" - {item}")
        return 1
    print(f"EKOS validation passed. Knowledge Markdown files scanned: {len(docs)}")
    print(f"Documents with metadata IDs: {len(seen)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
