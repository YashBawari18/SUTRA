#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT_DIR}"

echo "========================================================================"
echo "  SŪTRA — Running Full Intelligence & Data Analytics Pipeline"
echo "========================================================================"

echo ""
echo "[Step 1/7] Generating synthetic case dataset..."
python3 engine/generate_dataset.py

echo ""
echo "[Step 2/7] Running entity resolution & alias matching..."
python3 engine/entity_resolution.py

echo ""
echo "[Step 3/7] Building knowledge graph & computing network metrics..."
python3 engine/graph_analytics.py

echo ""
echo "[Step 4/7] Computing multi-factor explainable risk scores..."
python3 engine/risk_scoring.py

echo ""
echo "[Step 5/7] Extracting structured entities from raw FIR text..."
python3 engine/entity_extraction.py

echo ""
echo "[Step 6/7] Generating multilingual evidentiary reports (EN, HI, MR)..."
python3 engine/generate_report.py

echo ""
echo "[Step 7/7] Bundling and rebuilding dashboard web application..."
python3 engine/build_dashboard.py

echo ""
echo "========================================================================"
echo "  ✓ Pipeline completed successfully! Dashboard updated in dashboard/"
echo "========================================================================"
