#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "========================================================================"
echo "  SŪTRA — Criminal Network Intelligence Platform"
echo "  Starting Unified Full-Stack Platform..."
echo "========================================================================"

# Ensure database is seeded with initial case data
if [ ! -f "backend/sutra.db" ]; then
    echo ">> Initializing and seeding SQLite Knowledge Store..."
    python3 backend/seed.py
fi

echo ">> Starting FastAPI Backend & Intelligence Services..."
echo "   • Interactive Dashboard:   http://localhost:8000"
echo "   • REST API Core:           http://localhost:8000/api"
echo "   • Interactive API Docs:    http://localhost:8000/docs"
echo "   • Health Check:            http://localhost:8000/api/health"
echo "========================================================================"
echo ">> Press Ctrl+C to stop the system."
echo ""

cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
