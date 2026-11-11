import importlib.util
import json
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("ekos_web_server", ROOT / "app" / "server.py")
web = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(web)

class EkosWebApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = web.ThreadingHTTPServer(("127.0.0.1", 0), web.Handler)
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.httpd.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()
        cls.thread.join(timeout=3)

    def get_json(self, path):
        with urllib.request.urlopen(self.base + path, timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))

    def test_health_reports_local_ai_independent_index(self):
        data = self.get_json("/api/health")
        self.assertEqual(data["status"], "ok")
        self.assertEqual(data["ai_provider"], "none")
        self.assertGreater(data["documents"], 0)

    def test_search_returns_matching_documents(self):
        data = self.get_json("/api/search?q=runner")
        self.assertGreater(data["count"], 0)
        self.assertTrue(any(x["id"] == "GHA-RUN-001" for x in data["results"]))

    def test_document_includes_relationships_and_sources(self):
        data = self.get_json("/api/documents/GHA-ARCH-001")
        self.assertEqual(data["id"], "GHA-ARCH-001")
        self.assertGreater(len(data["relationships"]), 0)
        self.assertGreater(len(data["sources"]), 0)

    def test_invalid_document_id_is_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(self.base + "/api/documents/../../README.md", timeout=3)
        self.assertEqual(ctx.exception.code, 400)

    def test_static_ui_is_served(self):
        with urllib.request.urlopen(self.base + "/", timeout=3) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("text/html", response.headers["Content-Type"])

if __name__ == "__main__":
    unittest.main()
