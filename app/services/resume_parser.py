from __future__ import annotations

import io
from pathlib import Path

import docx
import pdfplumber

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".txt"}


def extract_text(filename: str, content: bytes) -> str:
    suffix = Path(filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise ValueError(f"Unsupported resume format: {suffix}")

    if suffix == ".pdf":
        return _extract_pdf(content)
    if suffix == ".docx":
        return _extract_docx(content)
    return content.decode("utf-8", errors="ignore")


def _extract_pdf(content: bytes) -> str:
    buffer = io.BytesIO(content)
    text_segments = []
    with pdfplumber.open(buffer) as pdf:
        for page in pdf.pages:
            text_segments.append(page.extract_text() or "")
    return "\n".join(text_segments)


def _extract_docx(content: bytes) -> str:
    buffer = io.BytesIO(content)
    document = docx.Document(buffer)
    return "\n".join(paragraph.text for paragraph in document.paragraphs)
