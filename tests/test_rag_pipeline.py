import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add project directory to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR / "project"))

from rag_agent.schemas import QueryAnalysis
from rag_agent.prompts import (
    get_rewrite_query_prompt,
    get_orchestrator_prompt,
    get_aggregation_prompt,
    get_context_compression_prompt,
)
from core.chat_interface import (
    format_rewrite_content,
    parse_rewrite_json,
    make_message,
    find_msg_idx,
)
from document_chunker import DocumentChunker


class TestSchemasAndPrompts(unittest.TestCase):
    def test_query_analysis_valid(self):
        data = {
            "is_clear": True,
            "questions": ["What is dynamic programming in 137notes?", "Explain DP table."],
            "clarification_needed": "",
        }
        obj = QueryAnalysis(**data)
        self.assertTrue(obj.is_clear)
        self.assertEqual(len(obj.questions), 2)
        self.assertEqual(obj.clarification_needed, "")

    def test_query_analysis_unclear(self):
        data = {
            "is_clear": False,
            "questions": [],
            "clarification_needed": "Please specify which lecture or topic you mean.",
        }
        obj = QueryAnalysis(**data)
        self.assertFalse(obj.is_clear)
        self.assertEqual(len(obj.questions), 0)
        self.assertIn("specify", obj.clarification_needed)

    def test_prompt_generation(self):
        prompts = [
            get_rewrite_query_prompt(),
            get_orchestrator_prompt(),
            get_aggregation_prompt(),
            get_context_compression_prompt(),
        ]
        for p in prompts:
            self.assertIsInstance(p, str)
            self.assertGreater(len(p), 50)


class TestChatInterfaceHelpers(unittest.TestCase):
    def test_parse_rewrite_json_valid(self):
        raw = 'Here is the analysis: {"is_clear": true, "questions": ["query 1"], "clarification_needed": ""}'
        parsed = parse_rewrite_json(raw)
        self.assertIsNotNone(parsed)
        self.assertTrue(parsed["is_clear"])
        self.assertEqual(parsed["questions"], ["query 1"])

    def test_parse_rewrite_json_invalid(self):
        raw = "Not a json string at all"
        parsed = parse_rewrite_json(raw)
        self.assertIsNone(parsed)

    def test_format_rewrite_content_clear(self):
        raw = '{"is_clear": true, "questions": ["Concept A", "Concept B"], "clarification_needed": ""}'
        formatted = format_rewrite_content(raw)
        self.assertIn("Query is clear", formatted)
        self.assertIn("- Concept A", formatted)
        self.assertIn("- Concept B", formatted)

    def test_format_rewrite_content_unclear(self):
        raw = '{"is_clear": false, "questions": [], "clarification_needed": "Which document?"}'
        formatted = format_rewrite_content(raw)
        self.assertIn("Query is unclear", formatted)
        self.assertIn("Clarification needed: *Which document?*", formatted)

    def test_make_message_and_find_idx(self):
        msg = make_message("Hello", title="Test Title", node="rewrite_query")
        self.assertEqual(msg["role"], "assistant")
        self.assertEqual(msg["content"], "Hello")
        self.assertEqual(msg["metadata"]["title"], "Test Title")
        self.assertEqual(msg["metadata"]["node"], "rewrite_query")

        messages = [
            {"role": "user", "content": "Hi"},
            msg,
            {"role": "assistant", "content": "Final answer"},
        ]
        idx = find_msg_idx(messages, "rewrite_query")
        self.assertEqual(idx, 1)
        self.assertIsNone(find_msg_idx(messages, "non_existent_node"))


class TestDocumentChunker(unittest.TestCase):
    def setUp(self):
        self.chunker = DocumentChunker()
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_chunking_hierarchical_markdown(self):
        # Create a sample markdown file with headers and content
        sample_md_content = """# Systems Architecture Overview

This section covers the core fundamentals of distributed operating systems and microkernels.
A microkernel provides only the minimal software required for an operating system, such as low-level memory management and inter-process communication.

## Memory Management

Virtual memory management is divided into paging and segmentation. In a paged system, memory is split into fixed-size frames and virtual address spaces are partitioned into equal pages.
Page tables map virtual page numbers to physical frame numbers. Translation lookaside buffers (TLBs) act as fast associative caches for recently used mappings.

### Multi-Level Page Tables

To support massive 64-bit address spaces without wasting contiguous RAM, multi-level page tables implement hierarchical radix trees.
When a page fault occurs, the MMU signals the OS kernel to load the page from secondary storage into an available RAM frame.

## Inter-Process Communication

Processes can communicate via shared memory buffers or message passing. Message passing mechanisms offer isolation and strong synchronization boundaries.
IPC efficiency often relies on zero-copy buffers and futexes for user-space synchronization primitives.
"""
        sample_file = Path(self.temp_dir.name) / "test_notes.md"
        sample_file.write_text(sample_md_content, encoding="utf-8")

        parent_chunks, child_chunks = self.chunker.create_chunks_single(sample_file, source_name="test_notes.pdf")

        # Verify parent chunks created
        self.assertGreater(len(parent_chunks), 0)
        for parent_id, parent_doc in parent_chunks:
            self.assertTrue(parent_id.startswith("test_notes_p"))
            self.assertTrue(hasattr(parent_doc, "page_content"))
            self.assertTrue(len(parent_doc.page_content) > 0)
            self.assertIn("source", parent_doc.metadata)
            self.assertEqual(parent_doc.metadata["source"], "test_notes.pdf")

        # Verify child chunks created and linked to parent IDs
        self.assertGreater(len(child_chunks), 0)
        parent_id_set = {p_id for p_id, _ in parent_chunks}
        for child_doc in child_chunks:
            self.assertIn("parent_id", child_doc.metadata)
            self.assertIn(child_doc.metadata["parent_id"], parent_id_set)
            self.assertEqual(child_doc.metadata["source"], "test_notes.pdf")
            self.assertLessEqual(len(child_doc.page_content), 1000)


if __name__ == "__main__":
    unittest.main()
