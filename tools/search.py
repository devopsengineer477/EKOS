#!/usr/bin/env python3
"""Search and explore the EKOS offline knowledge index."""
from __future__ import annotations
import argparse, json, re, sqlite3, sys
from pathlib import Path
from build_index import DB_PATH, connect

def query_tokens(q):
    return [x for x in re.findall(r"[A-Za-z0-9_]+",q) if x]

def search(conn, query, technology=None, category=None, status=None, limit=10):
    terms=query_tokens(query)
    if not terms: return []
    # Quote each token so punctuation/operators in user input cannot alter FTS syntax.
    match=" AND ".join('"'+t.replace('"','""')+'"' for t in terms)
    sql="""SELECT d.id,d.title,d.path,d.technology,d.category,d.status,d.last_reviewed,
                  snippet(documents_fts,3,'[',']',' … ',18) AS excerpt,
                  bm25(documents_fts,0.0,5.0,2.0,1.0) AS score
           FROM documents_fts JOIN documents d ON d.id=documents_fts.document_id
           WHERE documents_fts MATCH ?"""
    params=[match]
    if technology: sql+=" AND lower(d.technology)=lower(?)"; params.append(technology)
    if category: sql+=" AND lower(d.category)=lower(?)"; params.append(category)
    if status: sql+=" AND lower(d.status)=lower(?)"; params.append(status)
    sql+=" ORDER BY score LIMIT ?"; params.append(limit)
    return [dict(r) for r in conn.execute(sql,params).fetchall()]

def get_document(conn, doc_id):
    row=conn.execute("SELECT * FROM documents WHERE id=?",(doc_id,)).fetchone()
    return dict(row) if row else None

def get_relationships(conn, doc_id):
    rows=conn.execute("""SELECT DISTINCT d.id,d.title,d.path,d.technology,d.category,d.status,
      r.relationship_type FROM relationships r JOIN documents d
      ON d.id=CASE WHEN r.source_document_id=? THEN r.target_document_id ELSE r.source_document_id END
      WHERE r.source_document_id=? OR r.target_document_id=? ORDER BY d.title""",
      (doc_id,doc_id,doc_id)).fetchall()
    return [dict(r) for r in rows]

def get_sources(conn, doc_id):
    return [dict(r) for r in conn.execute("""SELECT s.* FROM sources s
      JOIN document_sources ds ON ds.source_id=s.id
      WHERE ds.document_id=? ORDER BY s.title""",(doc_id,)).fetchall()]

def list_sources(conn, query=None):
    if query:
        q="%"+query+"%"
        rows=conn.execute("SELECT * FROM sources WHERE title LIKE ? OR id LIKE ? ORDER BY title",(q,q))
    else:
        rows=conn.execute("SELECT * FROM sources ORDER BY title")
    return [dict(r) for r in rows.fetchall()]

def main():
    ap=argparse.ArgumentParser(description="Search EKOS without an AI service.")
    sub=ap.add_subparsers(dest="command",required=True)
    s=sub.add_parser("search",help="Full-text search")
    s.add_argument("query"); s.add_argument("--technology"); s.add_argument("--category")
    s.add_argument("--status"); s.add_argument("--limit",type=int,default=10)
    d=sub.add_parser("show",help="Show a document and its source/relationship navigation")
    d.add_argument("document_id")
    so=sub.add_parser("sources",help="List registered sources")
    so.add_argument("--query")
    args=ap.parse_args()
    if not DB_PATH.exists():
        print("Index not found. Run: python tools/build_index.py",file=sys.stderr); return 2
    conn=connect(DB_PATH)
    if args.command=="search":
        rows=search(conn,args.query,args.technology,args.category,args.status,max(1,min(args.limit,100)))
        if not rows: print("No matching documents.")
        for i,r in enumerate(rows,1):
            print(f"{i}. [{r['id']}] {r['title']}")
            print(f"   Technology: {r['technology'] or '-'} | Category: {r['category'] or '-'} | Status: {r['status'] or '-'}")
            print(f"   File: {r['path']}")
            if r["excerpt"]: print(f"   Match: {r['excerpt']}")
    elif args.command=="show":
        doc=get_document(conn,args.document_id)
        if not doc:
            print(f"Document not found: {args.document_id}"); conn.close(); return 1
        print(f"{doc['title']} [{doc['id']}]")
        print(f"Path: {doc['path']}")
        print(f"Technology: {doc['technology']} | Category: {doc['category']} | Status: {doc['status']}")
        print("\nRELATED DOCUMENTS")
        rels=get_relationships(conn,args.document_id)
        for r in rels: print(f"- [{r['id']}] {r['title']} — {r['path']}")
        if not rels: print("- None indexed")
        print("\nSOURCES")
        srcs=get_sources(conn,args.document_id)
        for x in srcs: print(f"- [{x['id']}] {x['title']}\n  {x['url'] or '(no URL)'}")
        if not srcs: print("- None linked")
    else:
        for x in list_sources(conn,args.query):
            print(f"[{x['id']}] {x['title']}\n  {x['url'] or '(no URL)'}")
    conn.close()
    return 0
if __name__=="__main__": sys.exit(main())
