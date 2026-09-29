"""
LegalEaseAI - Document Generator

Common document-generation helpers used by the LegalEaseAI project.
"""

from pathlib import Path
from typing import Optional


def generate_document(
    content: str,
    output_path: str,
    title: str = "LegalEaseAI Document",
) -> str:
    """
    Save generated legal content as a plain text document.

    Args:
        content: The generated document content.
        output_path: Destination file path.
        title: Document title.

    Returns:
        Absolute path of the created document.
    """

    if not content or not content.strip():
        raise ValueError("Document content cannot be empty.")

    path = Path(output_path)

    # Create parent folders automatically.
    path.parent.mkdir(parents=True, exist_ok=True)

    document_text = (
        f"{title}\n"
        f"{'=' * len(title)}\n\n"
        f"{content.strip()}\n"
    )

    path.write_text(document_text, encoding="utf-8")

    return str(path.resolve())


def clean_generated_text(text: Optional[str]) -> str:
    """
    Clean AI-generated text before saving or displaying it.
    """

    if not text:
        return ""

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    return text.strip()