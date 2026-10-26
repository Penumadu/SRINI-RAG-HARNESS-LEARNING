import os
import unittest
from pathlib import Path
from gradio_client import Client, handle_file

BASE_DIR = Path(__file__).resolve().parent.parent
SAMPLE_DOC = BASE_DIR / "scratch" / "test_quantum_computing.md"

class TestLiveServerEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = Client("http://localhost:7860/")

    def test_01_refresh_docs_handler(self):
        doc_list_html, analytics_html = self.client.predict(api_name="/refresh_docs_handler")
        self.assertIsInstance(doc_list_html, str)
        self.assertIn("Indexed Documents", doc_list_html)
        self.assertIn("137notes", doc_list_html)
        self.assertIsInstance(analytics_html, str)
        self.assertIn("Hierarchical", analytics_html)

    def test_02_refresh_observability_handler(self):
        search_html, obs_html, mem_html = self.client.predict(api_name="/refresh_observability_handler")
        self.assertIsInstance(search_html, str)
        self.assertIsInstance(obs_html, str)
        self.assertIn("State Machine Pipeline", obs_html)
        self.assertIsInstance(mem_html, str)
        self.assertIn("Dialogue State", mem_html)

    def test_03_flush_traces_handler(self):
        obs_html = self.client.predict(api_name="/flush_traces_handler")
        self.assertIsInstance(obs_html, str)
        self.assertIn("State Machine Pipeline", obs_html)

    def test_04_upload_document_handler(self):
        self.assertTrue(SAMPLE_DOC.exists(), f"Sample doc {SAMPLE_DOC} does not exist")
        uploaded, doc_list_html, analytics_html = self.client.predict(
            files=[handle_file(str(SAMPLE_DOC))],
            api_name="/upload_handler"
        )
        self.assertIsInstance(doc_list_html, str)
        self.assertIn("test_quantum_computing", doc_list_html)
        self.assertIn("Ready", doc_list_html)

    def test_05_clear_chat_handler(self):
        history, search_html, obs_html, mem_html = self.client.predict(api_name="/clear_chat_handler")
        self.assertEqual(history, [])
        self.assertIn("No search queries yet", search_html)

if __name__ == "__main__":
    unittest.main()
