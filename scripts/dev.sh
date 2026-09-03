#!/usr/bin/env bash
set -e

PORT=8080
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "========================================================================"
echo "  Starting SŪTRA Intelligence Dashboard Server"
echo "========================================================================"
echo "  URL: http://localhost:${PORT}"
echo "  Dashboard file: ${ROOT_DIR}/dashboard/index.html"
echo "  Press Ctrl+C to stop the server"
echo "========================================================================"

cd "${ROOT_DIR}"
python3 -m http.server "${PORT}" --directory dashboard
