# LegalEase

LegalEase is an AI-assisted legal document drafting application. It provides a FastAPI backend for document generation and export, plus a Streamlit frontend for collecting document details, previewing drafts, and downloading TXT, DOCX, or PDF files.

> **Notice:** LegalEase produces AI-assisted drafts, not legal advice. Have generated documents reviewed by a qualified legal professional before relying on or signing them.

## Project layout

- `code files/backend/` — FastAPI application and API routes
- `code files/frontend/` — Streamlit user interface
- `code files/ai_core/` — Gemini and document-generation helpers
- `code files/requirements.txt` — Python dependencies
- `code files/.env.example` — safe configuration template
- `code files/run.sh` — local launcher for the backend and frontend

## Run locally

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   cd "code files"
   python -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt
   ```

3. Create `.env` from the template and add your Gemini API key:

   ```bash
   cp .env.example .env
   ```

4. Start the application:

   ```bash
   ./run.sh
   ```

The API listens on port `8000` and the Streamlit interface listens on port `8501`.
