"""
LegalEaseAI - Application Configuration
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent


# Load environment variables from .env
load_dotenv(BASE_DIR / ".env")


# Application settings
APP_NAME = os.getenv("APP_NAME", "LegalEaseAI")
APP_VERSION = os.getenv("APP_VERSION", "1.0.0")


# Gemini settings
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
).strip()


# Backend settings
BACKEND_HOST = os.getenv(
    "BACKEND_HOST",
    "127.0.0.1",
)

BACKEND_PORT = int(
    os.getenv(
        "BACKEND_PORT",
        "8000",
    )
)


# Frontend settings
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    f"http://{BACKEND_HOST}:{BACKEND_PORT}",
).rstrip("/")


def validate_config() -> None:
    """
    Validate required application configuration.
    """

    if not GEMINI_API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. "
            "Please add it to your local .env file."
        )