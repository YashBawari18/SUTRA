#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "========================================================================"
echo "  SŪTRA — System Validation & Integrity Test Suite"
echo "========================================================================"

FAILED=0

check_file() {
  if [ -f "$1" ]; then
    echo "  [PASS] File exists: $1 ($(wc -c < "$1" | tr -d ' ') bytes)"
  else
    echo "  [FAIL] Missing file: $1"
    FAILED=$((FAILED + 1))
  fi
}

echo ""
echo "Checking Required Engine Scripts..."
check_file "engine/generate_dataset.py"
check_file "engine/entity_resolution.py"
check_file "engine/graph_analytics.py"
check_file "engine/risk_scoring.py"
check_file "engine/entity_extraction.py"
check_file "engine/generate_report.py"
check_file "engine/build_dashboard.py"
check_file "engine/dashboard_app.js"
check_file "engine/d3.v7.min.js"

echo ""
echo "Checking Generated Data Outputs..."
check_file "data/dataset.json"
check_file "data/entity_resolution_results.json"
check_file "data/graph_analytics_results.json"
check_file "data/risk_scores.json"
check_file "data/extraction_results.json"
check_file "data/investigation_report_i18n.json"

echo ""
echo "Checking Dashboard Distribution..."
check_file "dashboard/index.html"

echo ""
echo "Checking Backend API Components..."
check_file "backend/main.py"
check_file "backend/auth.py"
check_file "backend/requirements.txt"
check_file "backend/schema.cypher"
check_file "backend/routers/graph.py"
check_file "backend/routers/entities.py"

echo ""
if [ $FAILED -eq 0 ]; then
  echo "========================================================================"
  echo "  ✓ All checks PASSED! System structure is intact."
  echo "========================================================================"
  exit 0
else
  echo "========================================================================"
  echo "  ✗ Test failed with ${FAILED} missing file(s)."
  echo "========================================================================"
  exit 1
fi
