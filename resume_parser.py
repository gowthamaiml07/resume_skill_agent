"""
resume_parser.py
================
Module for extracting, cleaning, and validating text from PDF resumes using PyMuPDF (fitz).
All operations are performed purely in memory without persisting files to disk.
"""

from __future__ import annotations

import io
import re
try:
    import pymupdf as fitz
except ImportError:
    import fitz  # Fallback for older environments


class ResumeParsingError(Exception):
    """Base exception for errors encountered during PDF resume parsing."""
    pass


class EmptyPDFError(ResumeParsingError):
    """Raised when an uploaded PDF has zero pages or is corrupted/empty."""
    pass


class ScannedPDFError(ResumeParsingError):
    """Raised when a PDF contains no digital text (e.g., scanned images or flattened canvas)."""
    pass


def clean_extracted_text(raw_text: str) -> str:
    """
    Cleans raw text extracted from a PDF:
    - Normalizes multi-spaces while preserving structured paragraph breaks.
    - Cleans up common PDF extraction artifacts (e.g., bullet symbols, excessive blank lines).
    - Strips non-printable control characters.

    Args:
        raw_text: Raw string extracted from PyMuPDF.

    Returns:
        Cleaned, normalized text string.
    """
    if not raw_text:
        return ""

    # Replace null bytes or strange control characters (except newline, tab)
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]", " ", raw_text)

    # Standardize bullet characters to standard hyphen
    cleaned = re.sub(r"[\u2022\u2023\u25E6\u2043\u2219\u25AA\u25CF\u25CB]", "\n- ", cleaned)

    # Normalize horizontal whitespace
    cleaned = re.sub(r"[ \t]+", " ", cleaned)

    # Collapse more than 2 consecutive newlines into 2
    cleaned = re.sub(r"\n\s*\n\s*\n+", "\n\n", cleaned)

    return cleaned.strip()


def extract_text_from_pdf(pdf_input: Union[bytes, BinaryIO, io.BytesIO]) -> str:
    """
    Extracts and cleans all text content from an in-memory PDF resume using PyMuPDF.

    Args:
        pdf_input: PDF file content as raw bytes or a binary stream (e.g. Streamlit's UploadedFile).

    Returns:
        The extracted and cleaned text from all pages.

    Raises:
        EmptyPDFError: If the document contains 0 pages or cannot be opened.
        ScannedPDFError: If the document contains pages but no extractable digital text.
        ResumeParsingError: For other unexpected parsing issues.
    """
    try:
        # Convert input to bytes if it is a stream
        if hasattr(pdf_input, "read"):
            if hasattr(pdf_input, "seek"):
                pdf_input.seek(0)
            pdf_bytes = pdf_input.read()
        elif isinstance(pdf_input, bytes):
            pdf_bytes = pdf_input
        else:
            raise ResumeParsingError("Invalid PDF input type. Expected bytes or binary file stream.")

        if not pdf_bytes or len(pdf_bytes) == 0:
            raise EmptyPDFError("The uploaded PDF file is empty (0 bytes). Please upload a valid resume.")

        # Open the PDF in-memory via PyMuPDF
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")

        if doc.page_count == 0:
            doc.close()
            raise EmptyPDFError("The uploaded document contains no pages.")

        extracted_pages = []
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)
            text = page.get_text("text")
            if text and text.strip():
                extracted_pages.append(text.strip())

        doc.close()

        full_raw_text = "\n\n".join(extracted_pages)
        cleaned_text = clean_extracted_text(full_raw_text)

        # Check if text was extractable (digital vs. scanned image)
        # Resumes typically have at least 50 words / 200 characters of text
        if len(cleaned_text.strip()) < 30:
            raise ScannedPDFError(
                "No readable text could be extracted from this PDF. "
                "This usually happens when the resume is a scanned image, a photo, or an image-only PDF. "
                "Please upload a text-based/digital PDF (e.g., exported from Google Docs, MS Word, or Canva)."
            )

        return cleaned_text

    except (EmptyPDFError, ScannedPDFError):
        raise
    except Exception as e:
        raise ResumeParsingError(f"Failed to process PDF resume: {str(e)}") from e


def get_pdf_metadata(pdf_input: Union[bytes, BinaryIO, io.BytesIO]) -> Dict[str, Union[int, str]]:
    """
    Extracts high-level document statistics and metadata from a PDF file.

    Args:
        pdf_input: PDF file content as raw bytes or stream.

    Returns:
        Dictionary containing page count, word count, character count, and title.
    """
    try:
        if hasattr(pdf_input, "read"):
            if hasattr(pdf_input, "seek"):
                pdf_input.seek(0)
            pdf_bytes = pdf_input.read()
        else:
            pdf_bytes = pdf_input

        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = doc.page_count
        metadata = doc.metadata or {}
        doc.close()

        # Extract text to compute word & char count
        text = extract_text_from_pdf(pdf_bytes)
        words = len(text.split())
        chars = len(text)

        return {
            "page_count": page_count,
            "word_count": words,
            "character_count": chars,
            "title": metadata.get("title", "Untitled"),
            "author": metadata.get("author", "Unknown"),
        }
    except Exception:
        return {
            "page_count": 0,
            "word_count": 0,
            "character_count": 0,
            "title": "N/A",
            "author": "N/A",
        }
