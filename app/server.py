#!/usr/bin/env python3
"""EKOS local web application. Python standard library only; no external AI calls."""
from __future__ import annotations
import json, mimetypes, re, sqlite3, sys
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs, unquote

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "ekos-index.sqlite3"
STATIC = Path(__file__).resolve().parent / "static"
KNOWLEDGE = ROOT / "knowledge"
HOST, PORT = "127.0.0.1", 8765

def db():
    if not DB_PATH.exists():
        raise FileNotFoundError("EKOS index is missing. Run python tools/build_index.py first.")
    conn=sqlite3.connect(f"file:{DB_PATH.as_posix()}?mode=ro",uri=True)
    conn.row_factory=sqlite3.Row
    return conn

def rowdict(row):
    return dict(row) if row else None

def search_docs(conn, query="", technology="", category="", status="", limit=20):
    query=query.strip()
    if not query:
        sql="SELECT id,title,path,technology,category,status,last_reviewed,substr(body,1,260) AS excerpt FROM documents WHERE 1=1"
        params=[]
    else:
        terms=re.findall(r"[A-Za-z0-9_]+",query)
        if not terms: return []
        match=" AND ".join('"'+x.replace('"','""')+'"' for x in terms)
        sql="""SELECT d.id,d.title,d.path,d.technology,d.category,d.status,d.last_reviewed,
          snippet(documents_fts,3,'[',']',' … ',24) AS excerpt
          FROM documents_fts JOIN documents d ON d.id=documents_fts.document_id
          WHERE documents_fts MATCH ?"""
        params=[match]
    if technology: sql+=" AND lower(technology)=lower(?)"; params.append(technology)
    if category: sql+=" AND lower(category)=lower(?)"; params.append(category)
    if status: sql+=" AND lower(status)=lower(?)"; params.append(status)
    if query: sql+=" ORDER BY bm25(documents_fts,0.0,5.0,2.0,1.0)"
    else: sql+=" ORDER BY title COLLATE NOCASE"
    sql+=" LIMIT ?"; params.append(max(1,min(int(limit),100)))
    return [dict(x) for x in conn.execute(sql,params).fetchall()]

def get_document(conn, doc_id):
    d=rowdict(conn.execute("SELECT id,title,path,technology,category,subcategory,content_type,difficulty,status,version_scope,last_reviewed,body,headings FROM documents WHERE id=?",(doc_id,)).fetchone())
    if not d: return None
    d["relationships"]=[dict(x) for x in conn.execute("""SELECT DISTINCT d.id,d.title,d.path,d.technology,d.category,d.status
      FROM relationships r JOIN documents d ON d.id=CASE WHEN r.source_document_id=? THEN r.target_document_id ELSE r.source_document_id END
      WHERE r.source_document_id=? OR r.target_document_id=? ORDER BY d.title""",(doc_id,doc_id,doc_id)).fetchall()]
    d["sources"]=[dict(x) for x in conn.execute("""SELECT s.id,s.title,s.url,s.publisher,s.source_type,s.scope
      FROM sources s JOIN document_sources ds ON ds.source_id=s.id WHERE ds.document_id=? ORDER BY s.title""",(doc_id,)).fetchall()]
    return d

def source_list(conn, query=""):
    if query:
        like="%"+query+"%"
        rows=conn.execute("SELECT id,title,url,publisher,source_type,scope FROM sources WHERE title LIKE ? OR id LIKE ? ORDER BY title",(like,like))
    else:
        rows=conn.execute("SELECT id,title,url,publisher,source_type,scope FROM sources ORDER BY title")
    return [dict(x) for x in rows.fetchall()]

class Handler(BaseHTTPRequestHandler):
    server_version="EKOSLocal/1.0"
    def log_message(self, fmt, *args):
        # Keep local server logs compact.
        sys.stdout.write("[EKOS] "+fmt%args+"\n")
    def send_json(self, data, status=200):
        body=json.dumps(data,ensure_ascii=False).encode("utf-8")
        self.send_response(status); self.send_header("Content-Type","application/json; charset=utf-8")
        self.send_header("Content-Length",str(len(body))); self.send_header("Cache-Control","no-store")
        self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        parsed=urlparse(self.path); path=parsed.path
        params=parse_qs(parsed.query)
        try:
            if path=="/api/health":
                with closing(db()) as c:
                    self.send_json({"status":"ok","documents":c.execute("SELECT COUNT(*) FROM documents").fetchone()[0],
                                    "sources":c.execute("SELECT COUNT(*) FROM sources").fetchone()[0],
                                    "engine":"SQLite FTS5","ai_provider":"none"})
                return
            if path=="/api/search":
                with closing(db()) as c:
                    rows=search_docs(c,params.get("q",[""])[0],params.get("technology",[""])[0],
                                     params.get("category",[""])[0],params.get("status",[""])[0],
                                     params.get("limit",["20"])[0])
                    self.send_json({"results":rows,"count":len(rows)})
                return
            if path.startswith("/api/documents/"):
                doc_id=unquote(path[len("/api/documents/"):])
                if not re.fullmatch(r"[A-Za-z0-9_-]{1,100}",doc_id):
                    self.send_json({"error":"Invalid document ID"},400); return
                with closing(db()) as c: doc=get_document(c,doc_id)
                if not doc: self.send_json({"error":"Document not found"},404)
                else: self.send_json(doc)
                return
            if path=="/api/sources":
                with closing(db()) as c: items=source_list(c,params.get("q",[""])[0])
                self.send_json({"sources":items,"count":len(items)}); return
            if path=="/api/filters":
                with closing(db()) as c:
                    def vals(col):
                        return [r[0] for r in c.execute(f"SELECT DISTINCT {col} FROM documents WHERE {col} IS NOT NULL AND {col}<>'' ORDER BY {col}")]
                    self.send_json({"technologies":vals("technology"),"categories":vals("category"),"statuses":vals("status")})
                return
            if path=="/":
                self.serve_static("index.html"); return
            if path in ("/app.js","/styles.css"):
                self.serve_static(path[1:]); return
            self.send_json({"error":"Not found"},404)
        except FileNotFoundError as e:
            self.send_json({"error":str(e)},503)
        except sqlite3.OperationalError as e:
            self.send_json({"error":f"Search index error: {e}"},500)
        except (ValueError,TypeError) as e:
            self.send_json({"error":str(e)},400)
    def serve_static(self, name):
        allowed={"index.html","app.js","styles.css"}
        if name not in allowed:
            self.send_error(404); return
        p=STATIC/name
        if not p.exists(): self.send_error(404); return
        body=p.read_bytes()
        ctype=mimetypes.guess_type(str(p))[0] or "application/octet-stream"
        if name.endswith(".js"): ctype="text/javascript"
        self.send_response(200); self.send_header("Content-Type",ctype+"; charset=utf-8")
        self.send_header("Content-Length",str(len(body))); self.send_header("X-Content-Type-Options","nosniff")
        self.end_headers(); self.wfile.write(body)

def main():
    if not DB_PATH.exists():
        print("Index not found. Run: python tools/build_index.py",file=sys.stderr); return 2
    httpd=ThreadingHTTPServer((HOST,PORT),Handler)
    print(f"EKOS is running locally: http://{HOST}:{PORT}")
    print("Local-only binding. No external AI provider is configured.")
    try: httpd.serve_forever()
    except KeyboardInterrupt: print("\nStopping EKOS...")
    finally: httpd.server_close()
    return 0
if __name__=="__main__": sys.exit(main())
