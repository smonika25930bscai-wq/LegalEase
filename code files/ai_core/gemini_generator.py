"""
LegalEaseAI - Gemini AI Generator
"""

import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()


def generate_with_gemini(
    prompt: str,
    model_name: Optional[str] = None,
) -> str:
    """
    Generate text using Google's Gemini API.
    """

    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty.")

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Gemini API key not found. "
            "Please add GEMINI_API_KEY to the .env file."
        )

    try:
        from google import genai

        client = genai.Client(api_key=api_key)

        model = model_name or os.getenv(
            "GEMINI_MODEL",
            "gemini-2.5-flash",
        )

        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        text = getattr(response, "text", None)

        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()

    except ImportError as exc:
        raise RuntimeError(
            "Google GenAI package is not installed. "
            "Run: pip install google-genai"
        ) from exc

    except Exception as exc:
        raise RuntimeError(
            f"Gemini generation failed: {exc}"
        ) from exc