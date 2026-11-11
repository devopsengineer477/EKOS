#!/usr/bin/env python3
"""Build and maintain the EKOS local SQLite knowledge index (stdlib only)."""
from __future__ import annotations
import argparse, json, re, sqlite3, sys
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "ekos-index.sqlite3"
KNOWLEDGE = ROOT / "knowledge"
SOURCE_REGISTER = ROOT / "sources" / "source-register.yml"

def parse_front_matter(text: str):
    """Parse the simple EKOS YAML subset; supports scalar/list/nested source-id metadata."""
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    block = text[4:end]
    data, in_sources = {}, False
    for raw in block.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        s=raw.strip()
        if in_sources:
            m=re.match(r"-\s*id:\s*(.+?)\s*$",s)
            if m:
                data.setdefault("sources",[]).append(m.group(1).strip("'\""))
                continue
            if raw[:1].isspace():
                continue
            in_sources=False
        if ":" not in s: continue
        k,v=s.split(":",1); k=k.strip(); v=v.strip()
        if k=="sources":
            in_sources=True; data["sources"]=[]
        elif v.startswith("[") and v.endswith("]"):
            data[k]=[x.strip().strip("'\"") for x in v[1:-1].split(",") if x.strip()]
        elif v:
            data[k]=v.strip("'\"")
    return data

def parse_source_register(path: Path):
    if not path.exists(): return []
    raw=path.read_text(encoding="utf-8")
    entries=[]
    # The register uses simple top-level list entries with scalar fields.
    for chunk in re.split(r"(?m)^\s*-\s+id:\s*", raw)[1:]:
        lines=chunk.splitlines()
        if not lines: continue
        sid=lines[0].strip().strip("'\"")
        item={"id":sid}
        for line in lines[1:]:
            m=re.match(r"^\s+([A-Za-z0-9_-]+):\s*(.*?)\s*$",line)
            if m:
                item[m.group(1)]=m.group(2).strip("'\"")
        entries.append(item)
    return entries

def strip_front_matter(text):
    if text.startswith("---\n"):
        end=text.find("\n---",4)
        if end>=0: return text[end+4:].strip()
    return text.strip()

def extract_title(meta, body, path):
    if meta.get("title"): return str(meta["title"])
    m=re.search(r"(?m)^#\s+(.+)$",body)
    return m.group(1).strip() if m else path.stem

def extract_headings(body):
    return "\n".join(re.findall(r"(?m)^#{1,4}\s+(.+)$",body))

def connect(db_path=DB_PATH):
    db_path.parent.mkdir(parents=True,exist_ok=True)
    conn=sqlite3.connect(db_path)
    conn.row_factory=sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def create_schema(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS documents (
      id TEXT PRIMARY KEY, path TEXT NOT NULL UNIQUE, title TEXT NOT NULL,
      technology TEXT, category TEXT, subcategory TEXT, content_type TEXT,
      difficulty TEXT, status TEXT, version_scope TEXT, last_reviewed TEXT,
      body TEXT NOT NULL, headings TEXT, indexed_at TEXT NOT NULL
    );
    CREATE TABLE IF NOT EXISTS sources (
      id TEXT PRIMARY KEY, title TEXT, url TEXT, publisher TEXT,
      source_type TEXT, accessed TEXT, scope TEXT, notes TEXT
    );
    CREATE TABLE IF NOT EXISTS document_sources (
      document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
      source_id TEXT NOT NULL REFERENCES sources(id) ON DELETE CASCADE,
      PRIMARY KEY(document_id, source_id)
    );
    CREATE TABLE IF NOT EXISTS relationships (
      source_document_id TEXT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
      target_document_id TEXT NOT NULL,
      relationship_type TEXT NOT NULL DEFAULT 'related',
      PRIMARY KEY(source_document_id,target_document_id,relationship_type)
    );
    CREATE VIRTUAL TABLE IF NOT EXISTS documents_fts USING fts5(
      document_id UNINDEXED, title, headings, body,
      tokenize='unicode61 remove_diacritics 2'
    );
    CREATE INDEX IF NOT EXISTS idx_documents_technology ON documents(technology);
    CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
    CREATE INDEX IF NOT EXISTS idx_documents_status ON documents(status);
    CREATE INDEX IF NOT EXISTS idx_sources_title ON sources(title);
    """)
    conn.commit()

def build_index(root=ROOT, db_path=DB_PATH):
    root=Path(root)
    conn=connect(Path(db_path))
    create_schema(conn)
    # Rebuild as a deterministic snapshot of the current repository.
    conn.execute("DELETE FROM document_sources")
    conn.execute("DELETE FROM relationships")
    conn.execute("DELETE FROM documents")
    conn.execute("DELETE FROM sources")
    conn.execute("DELETE FROM documents_fts")
    sources=parse_source_register(root/"sources"/"source-register.yml")
    for s in sources:
        conn.execute("""INSERT OR REPLACE INTO sources
          (id,title,url,publisher,source_type,accessed,scope,notes)
          VALUES (?,?,?,?,?,?,?,?)""",
          (s.get("id"),s.get("title"),s.get("url"),s.get("publisher"),
           s.get("source_type"),s.get("accessed"),s.get("scope"),s.get("notes")))
    docs=[]
    for p in sorted((root/"knowledge").rglob("*.md")):
        if p.name.lower() in {"readme.md","master-index.md"}: continue
        raw=p.read_text(encoding="utf-8")
        meta=parse_front_matter(raw)
        doc_id=meta.get("id")
        if not doc_id: continue
        body=strip_front_matter(raw)
        rel=p.relative_to(root).as_posix()
        title=extract_title(meta,body,p)
        headings=extract_headings(body)
        version=meta.get("version_scope")
        if isinstance(version,dict): version=json.dumps(version,ensure_ascii=False)
        elif version is None: version=meta.get("version_context")
        category=meta.get("category") or meta.get("domain")
        subcategory=meta.get("subcategory")
        content_type=meta.get("content_type") or meta.get("type")
        docs.append((doc_id,rel,title,meta.get("technology"),category,subcategory,
                     content_type,meta.get("difficulty"),meta.get("status"),
                     str(version) if version else None,meta.get("last_reviewed"),
                     body,headings))
    now=datetime.now(timezone.utc).isoformat(timespec="seconds")
    for d in docs:
        conn.execute("""INSERT INTO documents
          (id,path,title,technology,category,subcategory,content_type,difficulty,status,
           version_scope,last_reviewed,body,headings,indexed_at)
          VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",d+(now,))
    idset={d[0] for d in docs}
    for d in docs:
        meta=parse_front_matter((root/d[1]).read_text(encoding="utf-8"))
        for sid in meta.get("sources",[]) if isinstance(meta.get("sources"),list) else []:
            if conn.execute("SELECT 1 FROM sources WHERE id=?",(sid,)).fetchone():
                conn.execute("INSERT OR IGNORE INTO document_sources VALUES (?,?)",(d[0],sid))
        rels=meta.get("related_documents",[])
        if isinstance(rels,list):
            for target in rels:
                # Existing relationships are stored as directed edges; search displays both directions.
                conn.execute("INSERT OR IGNORE INTO relationships VALUES (?,?,?)",(d[0],target,"related"))
    # FTS5 contentless table is populated explicitly.
    for d in docs:
        conn.execute("INSERT INTO documents_fts(document_id,title,headings,body) VALUES (?,?,?,?)",
                     (d[0],d[2],d[12],d[11]))
    conn.commit()
    counts={"documents":len(docs),"sources":len(sources),
            "document_source_links":conn.execute("SELECT COUNT(*) FROM document_sources").fetchone()[0],
            "relationships":conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0],
            "database":str(Path(db_path))}
    conn.close()
    return counts

def main():
    ap=argparse.ArgumentParser(description="Build the EKOS local SQLite search index.")
    ap.add_argument("--db",default=str(DB_PATH),help="Optional database path")
    args=ap.parse_args()
    try:
        result=build_index(ROOT,Path(args.db))
    except sqlite3.OperationalError as e:
        print(f"Index build failed: {e}",file=sys.stderr)
        if "fts5" in str(e).lower(): print("This Python SQLite build lacks FTS5 support.",file=sys.stderr)
        return 1
    print("EKOS index built successfully")
    for k,v in result.items(): print(f"{k}: {v}")
    return 0
if __name__=="__main__": sys.exit(main())
