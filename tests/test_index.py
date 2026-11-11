import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"tools"))
from build_index import build_index
from search import search, get_relationships, get_sources
import sqlite3

class EkosIndexTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        (self.root/"knowledge/demo").mkdir(parents=True)
        (self.root/"sources").mkdir()
        (self.root/"sources/source-register.yml").write_text(
            "sources:\n  - id: SRC-1\n    title: Demo Source\n    url: https://example.test/docs\n",encoding="utf-8")
        doc="""---
id: DEMO-001
title: Demo Workflow Runner
technology: demo
category: runners
status: reviewed
last_reviewed: 2026-01-01
sources:
  - id: SRC-1
related_documents: [DEMO-002]
---
# Demo Workflow Runner
## Purpose
A demo runner document.
## Runner execution
This document describes runner scheduling and execution.
## Sources
SRC-1
"""
        doc2=doc.replace("DEMO-001","DEMO-002").replace("Demo Workflow Runner","Demo Job Scheduling").replace("related_documents: [DEMO-002]","related_documents: [DEMO-001]").replace("runner scheduling and execution","task orchestration and queue management").replace("## Runner execution","## Task orchestration")
        (self.root/"knowledge/demo/one.md").write_text(doc,encoding="utf-8")
        (self.root/"knowledge/demo/two.md").write_text(doc2,encoding="utf-8")
        self.db=self.root/"test.sqlite3"
        build_index(self.root,self.db)
        self.conn=sqlite3.connect(self.db); self.conn.row_factory=sqlite3.Row
    def tearDown(self):
        self.conn.close(); self.tmp.cleanup()
    def test_full_text_and_filters(self):
        rows=search(self.conn,"runner execution",technology="demo",category="runners",status="reviewed")
        self.assertEqual(len(rows),1)
        self.assertEqual(rows[0]["id"],"DEMO-001")
    def test_relationship_navigation(self):
        rels=get_relationships(self.conn,"DEMO-001")
        self.assertEqual({r["id"] for r in rels},{"DEMO-002"})
    def test_source_navigation(self):
        sources=get_sources(self.conn,"DEMO-001")
        self.assertEqual(sources[0]["id"],"SRC-1")

if __name__=="__main__": unittest.main()
