.PHONY: help start dev pipeline build backend db-up db-down test clean

help:
	@echo "========================================================================"
	@echo "  SŪTRA — Criminal Network Intelligence Platform"
	@echo "========================================================================"
	@echo "  make start      - Launch unified full-stack platform (backend + UI on 8000)"
	@echo "  make dev        - Serve the interactive dashboard on port 8080"
	@echo "  make pipeline   - Run all 7 engine data & intelligence analysis stages"
	@echo "  make build      - Rebuild dashboard/index.html bundle from engine"
	@echo "  make backend    - Start the FastAPI backend API server (port 8000)"
	@echo "  make db-up      - Start Neo4j and PostgreSQL containers via Docker"
	@echo "  make db-down    - Stop Neo4j and PostgreSQL containers"
	@echo "  make test       - Run system and data integrity test suite"
	@echo "  make clean      - Clean cache, bytecode, and temporary files"
	@echo "========================================================================"

start:
	@bash scripts/start.sh

dev:
	@bash scripts/dev.sh

pipeline:
	@bash scripts/pipeline.sh

build:
	@python3 engine/build_dashboard.py

backend:
	@cd backend && uvicorn main:app --reload --port 8000

db-up:
	@docker compose up -d neo4j postgres

db-down:
	@docker compose down

test:
	@bash scripts/test_system.sh

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@find . -type f -name ".DS_Store" -delete 2>/dev/null || true
	@echo "✓ Cleaned temporary files and bytecode caches."
