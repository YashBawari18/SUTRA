# SUTRA Backend — Setup Guide

This is the **production-shaped** backend (FastAPI + Neo4j + PostgreSQL +
LLM-based assistant). It needs internet access to install packages and
run a database, so it can't run inside a sandboxed chat environment —
run it on your own machine, a cloud VM, or inside **Claude Code**
(recommended: Claude Code can install everything below itself and run/debug
it interactively, which is much easier than doing this manually if you're
new to backend development).

## What you need installed

- Python 3.11+
- Docker (easiest way to run Neo4j + PostgreSQL locally without manual install)

## 1. Start the databases

```bash
docker run -d --name sutra-neo4j -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/sutra-dev-password neo4j:5

docker run -d --name sutra-postgres -p 5432:5432 \
  -e POSTGRES_PASSWORD=sutra-dev-password -e POSTGRES_DB=sutra postgres:16
```

## 2. Set up the Python environment

```bash
cd backend
python3 -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## 3. Configure environment variables

Create a `.env` file in `backend/`:

```
SUTRA_JWT_SECRET=replace-with-a-long-random-string
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sutra-dev-password
POSTGRES_URL=postgresql://postgres:sutra-dev-password@localhost:5432/sutra
ANTHROPIC_API_KEY=your-key-here   # only needed for the AI assistant endpoint
```

## 4. Load the graph schema

```bash
# Open http://localhost:7474 (Neo4j Browser), log in with neo4j/sutra-dev-password,
# then paste and run the contents of schema.cypher
```

## 5. Run the API

```bash
uvicorn main:app --reload --port 8000
```

Visit `http://localhost:8000/docs` for the interactive API documentation
(FastAPI generates this automatically from the router code).

## 6. Load the demo dataset

The synthetic dataset and all the analysis engines already work standalone
in `/engine` (no database needed) — run those first to confirm the logic,
then port the data-loading step into the Neo4j/PostgreSQL connections here
once your databases are running.

## Login (demo users, defined in auth.py)

| Username | Password | Role |
|---|---|---|
| demo_investigator | demo-password | investigator |
| demo_admin | demo-password | admin |

**Change these before any real deployment.**
