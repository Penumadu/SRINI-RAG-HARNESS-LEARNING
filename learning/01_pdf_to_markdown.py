"""
==============================================================================
01_pdf_to_markdown.py — PDF to Markdown Conversion for RAG Systems
==============================================================================
Converted from notebooks/pdf_to_markdown.ipynb.

This module demonstrates how to convert PDF documents into structured Markdown
tailored for Hierarchical RAG chunking. It categorizes PDFs into three tiers:

  1. Category 1: Simple PDFs (Fast digital text extraction via PyMuPDF4LLM)
  2. Category 2: Medium Complexity PDFs (Scanned pages / tables via Docling)
  3. Category 3: Complex PDFs (Visual layouts / charts via Vision-Language Models)

It also includes:
  - validate_markdown_quality(): Audits conversion quality (word count, headers, tables)
  - smart_convert_pdf(): Intelligently selects the best tool based on PDF properties

Usage:
  python learning/01_pdf_to_markdown.py --help
  python learning/01_pdf_to_markdown.py --demo
  python learning/01_pdf_to_markdown.py --input path/to/doc.pdf --method smart --output markdown_docs/
  python learning/01_pdf_to_markdown.py --validate markdown_docs/sample.md
==============================================================================
"""

import os
import sys
import argparse
from pathlib import Path

# Ensure workspace root is in sys.path
_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from learning import config


# ==============================================================================
# Category 1: Simple PDFs — PyMuPDF4LLM
# Fast, lightweight extraction preserving headers and tables for native digital PDFs
# ==============================================================================

def convert_simple_pdf_pymupdf4llm(pdf_path: str, output_dir: str = None) -> str:
    """
    Converts a digital PDF to Markdown using PyMuPDF4LLM.
    
    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory where the .md file should be saved (default: config.MARKDOWN_DIR)
        
    Returns:
        The markdown string content.
    """
    out_dir = Path(output_dir or config.MARKDOWN_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_p = Path(pdf_path)

    try:
        import pymupdf4llm
    except ImportError:
        raise ImportError(
            "pymupdf4llm is required for simple PDF extraction.\n"
            "Install it via: pip install pymupdf4llm"
        )

    print(f"📄 [Category 1 - PyMuPDF4LLM] Converting: {pdf_p.name}...")
    markdown_text = pymupdf4llm.to_markdown(
        str(pdf_p),
        header=False,
        footer=False,
        page_separators=True
    )

    output_path = out_dir / f"{pdf_p.stem}.md"
    output_path.write_text(markdown_text, encoding="utf-8")
    print(f"✓ Saved Markdown: {output_path} ({len(markdown_text)} chars)")
    return markdown_text


# ==============================================================================
# Category 2: Medium Complexity PDFs — Docling
# OCR + Document Structure Analysis for scanned docs and complex tables
# ==============================================================================

def convert_medium_pdf_docling(pdf_path: str, output_dir: str = None) -> str:
    """
    Converts a scanned or complex-table PDF using Docling OCR & Layout Parser.
    
    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory where the .md file should be saved
        
    Returns:
        The markdown string content.
    """
    out_dir = Path(output_dir or config.MARKDOWN_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_p = Path(pdf_path)

    try:
        from docling.document_converter import DocumentConverter
    except ImportError:
        raise ImportError(
            "docling is required for medium complexity OCR extraction.\n"
            "Install it via: pip install docling"
        )

    print(f"📄 [Category 2 - Docling] Converting (OCR & Tables): {pdf_p.name}...")
    converter = DocumentConverter()
    result = converter.convert(str(pdf_p))
    markdown_text = result.document.export_to_markdown()

    output_path = out_dir / f"{pdf_p.stem}.md"
    output_path.write_text(markdown_text, encoding="utf-8")
    print(f"✓ Saved Markdown: {output_path} ({len(markdown_text)} chars)")
    return markdown_text


# ==============================================================================
# Category 3: Complex PDFs — Vision-Language Models (VLM)
# Multimodal reasoning for dense diagrams, mathematical proofs, and charts
# ==============================================================================

VLM_SYSTEM_PROMPT = """You are an expert document parser specializing in converting PDF pages to markdown format.

**Your task:**
Convert the provided document page into clean, well-formatted markdown while preserving ALL information, structural hierarchy, and meaning.

**Formatting Rules:**
1. Maintain proper markdown headings (# H1 for title, ## H2 for sections, ### H3 for subsections)
2. Format tables cleanly using standard markdown table syntax (| Header 1 | Header 2 |)
3. For mathematical equations, use LaTeX notation ($inline$ or $$block$$)
4. For code blocks, specify the appropriate language (```python, ```bash, etc.)
5. For diagrams/charts: Describe key insights, trendlines, and metrics in bullet points
6. Emphasize key terms using bold (**term**) or italics (*term*)
7. NEVER omit information or summarize sections unless explicitly requested
8. Output ONLY clean markdown text without meta-commentary
"""

def convert_complex_pdf_vlm(pdf_path: str, output_dir: str = None, api_key: str = None) -> str:
    """
    Converts a visually complex PDF page-by-page using Google Gemini Vision.
    
    Args:
        pdf_path: Path to the input PDF file
        output_dir: Directory where the .md file should be saved
        api_key: Google Gemini API key (or GOOGLE_API_KEY from environment)
        
    Returns:
        The combined markdown content.
    """
    out_dir = Path(output_dir or config.MARKDOWN_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    pdf_p = Path(pdf_path)

    key = api_key or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise ValueError("GOOGLE_API_KEY is required for VLM conversion.")

    try:
        import fitz  # PyMuPDF
        from google import genai
        from google.genai import types
        from PIL import Image
        import io
    except ImportError:
        raise ImportError(
            "PyMuPDF, google-genai, and Pillow are required for VLM parsing.\n"
            "Install via: pip install PyMuPDF google-genai pillow"
        )

    print(f"📄 [Category 3 - VLM Gemini] Converting multimodal pages: {pdf_p.name}...")
    ai_client = genai.Client(api_key=key)
    doc = fitz.open(str(pdf_p))

    page_markdowns = []
    for page_idx in range(doc.page_count):
        page = doc[page_idx]
        pix = page.get_pixmap(dpi=200)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        print(f"   Analyzing page {page_idx + 1}/{doc.page_count} with Gemini Vision...")
        response = ai_client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[VLM_SYSTEM_PROMPT, img]
        )
        page_md = response.text or ""
        page_markdowns.append(f"<!-- Page {page_idx + 1} -->\n\n{page_md}")

    doc.close()
    combined_md = "\n\n---\n\n".join(page_markdowns)
    output_path = out_dir / f"{pdf_p.stem}.md"
    output_path.write_text(combined_md, encoding="utf-8")
    print(f"✓ Saved Markdown: {output_path} ({len(combined_md)} chars)")
    return combined_md


# ==============================================================================
# Smart Router & Quality Auditor
# ==============================================================================

def smart_convert_pdf(pdf_path: str, output_dir: str = None, api_key: str = None) -> str:
    """
    Intelligently inspects the PDF structure and routes to the best converter:
      - Low text density (< 50 chars/page) -> Docling (Scanned document OCR)
      - High image count (> 2 per page) -> VLM / Gemini (Complex diagrams)
      - Standard digital text -> PyMuPDF4LLM (Fast & lean)
    """
    try:
        import fitz
    except ImportError:
        # Fall back to PyMuPDF4LLM directly
        return convert_simple_pdf_pymupdf4llm(pdf_path, output_dir)

    doc = fitz.open(pdf_path)
    sample_page = doc[0] if doc.page_count > 0 else None
    
    if not sample_page:
        doc.close()
        raise ValueError(f"PDF has no pages: {pdf_path}")

    text = sample_page.get_text()
    is_scanned = len(text.strip()) < 50
    has_many_images = len(sample_page.get_images()) > 2
    doc.close()

    if is_scanned:
        print(f"🔍 Routing '{Path(pdf_path).name}' -> Category 2: Docling (Detected Scanned Text)")
        try:
            return convert_medium_pdf_docling(pdf_path, output_dir)
        except Exception as e:
            print(f"⚠️ Docling fallback warning: {e}. Attempting PyMuPDF4LLM...")
            return convert_simple_pdf_pymupdf4llm(pdf_path, output_dir)
    elif has_many_images:
        vlm_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if vlm_key:
            print(f"🔍 Routing '{Path(pdf_path).name}' -> Category 3: VLM Gemini (Detected Charts/Images)")
            return convert_complex_pdf_vlm(pdf_path, output_dir, api_key=vlm_key)
        else:
            print(f"ℹ️ High image count detected, but no GOOGLE_API_KEY provided. Using PyMuPDF4LLM.")
            return convert_simple_pdf_pymupdf4llm(pdf_path, output_dir)
    else:
        print(f"🔍 Routing '{Path(pdf_path).name}' -> Category 1: PyMuPDF4LLM (Native Digital Text)")
        return convert_simple_pdf_pymupdf4llm(pdf_path, output_dir)


def validate_markdown_quality(md_path: Path | str) -> dict:
    """
    Checks markdown conversion quality metrics:
      - Word count & line metrics
      - Structural headers (# H1, ## H2, ### H3)
      - Table markers (|)
      - LaTeX formula markers ($)
    """
    p = Path(md_path)
    if not p.exists():
        raise FileNotFoundError(f"File not found: {p}")

    content = p.read_text(encoding="utf-8")
    words = content.split()
    total_lines = max(content.count("\n"), 1)
    empty_lines = content.count("\n\n")

    return {
        "file": p.name,
        "word_count": len(words),
        "total_characters": len(content),
        "has_headers": "#" in content,
        "header_count": sum(1 for line in content.splitlines() if line.strip().startswith("#")),
        "has_tables": "|" in content,
        "has_formulas": "$" in content,
        "avg_line_length": round(len(content) / total_lines, 1),
        "empty_ratio": round(empty_lines / total_lines, 3),
    }


# ==============================================================================
# CLI Entrypoint & Demo
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="PDF to Markdown Conversion for Hierarchical RAG"
    )
    parser.add_argument("--input", "-i", type=str, help="Path to input PDF file")
    parser.add_argument("--output", "-o", type=str, default=config.MARKDOWN_DIR, help="Output directory")
    parser.add_argument("--method", "-m", choices=["pymupdf", "docling", "vlm", "smart"], default="smart")
    parser.add_argument("--validate", "-v", type=str, help="Validate an existing Markdown file")
    parser.add_argument("--demo", action="store_true", help="Run demonstration and inspect existing sample docs")

    args = parser.parse_args()

    if args.validate:
        metrics = validate_markdown_quality(args.validate)
        print("\n📊 Markdown Quality Audit:")
        for k, val in metrics.items():
            print(f"  • {k:20s}: {val}")
        return

    if args.demo:
        print("=" * 70)
        print(" Demonstration: Auditing Sample Markdown Documents for RAG")
        print("=" * 70)
        # Ensure sample docs exist
        from learning.sample_docs import create_sample_documents
        create_sample_documents()

        md_files = list(Path(config.MARKDOWN_DIR).glob("*.md"))
        print(f"\nAuditing {len(md_files)} markdown files in '{config.MARKDOWN_DIR}':\n")
        for md in md_files:
            m = validate_markdown_quality(md)
            print(f"📄 {m['file']:<25} | Words: {m['word_count']:<6} | Headers: {m['header_count']:<3} | Tables: {str(m['has_tables']):<5} | Empty Ratio: {m['empty_ratio']}")
        print("\n✅ Markdown documents are ready for Hierarchical Chunking.")
        return

    if args.input:
        if args.method == "pymupdf":
            convert_simple_pdf_pymupdf4llm(args.input, args.output)
        elif args.method == "docling":
            convert_medium_pdf_docling(args.input, args.output)
        elif args.method == "vlm":
            convert_complex_pdf_vlm(args.input, args.output)
        else:
            smart_convert_pdf(args.input, args.output)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
