#!/bin/bash

echo "Starting LegalEaseAI..."

python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

sleep 3

python -m streamlit run frontend/app.py --server.port 8501

kill $BACKEND_PID