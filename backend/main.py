"""
SUTRA Backend — main.py
=========================
FastAPI application entrypoint. Run with:
    uvicorn main:app --reload --port 8000

Requires: PostgreSQL and Neo4j running (see README.md for docker-compose
setup) and a .env file with connection strings + JWT secret.

This file wires together all the routers described in the blueprint's
API design (Part 24). Each router is a thin HTTP layer over the same
engine logic already proven out in /engine (entity_resolution.py,
graph_analytics.py, risk_scoring.py, entity_extraction.py) — the
production backend re-uses that logic as importable modules rather
than reimplementing it.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import cases, upload, entities, graph, anomalies, timeline, assistant, reports, audit, evidence
from auth import router as auth_router
from database import init_db

app = FastAPI(
    title="SUTRA — Criminal Network Intelligence API",
    description="Investigative decision-support API. All outputs require human verification.",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits local dashboard file, 8080, 5173, and container origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(cases.router, prefix="/api/cases", tags=["cases"])
app.include_router(evidence.router, prefix="/api/evidence", tags=["evidence"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(entities.router, prefix="/api/entities", tags=["entities"])
app.include_router(graph.router, prefix="/api/graph", tags=["graph"])
app.include_router(anomalies.router, prefix="/api/anomalies", tags=["anomalies"])
app.include_router(timeline.router, prefix="/api/timeline", tags=["timeline"])
app.include_router(assistant.router, prefix="/api/assistant", tags=["assistant"])
app.include_router(reports.router, prefix="/api/report", tags=["reports"])
app.include_router(audit.router, prefix="/api/audit-logs", tags=["audit"])


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "service": "SUTRA Intelligence Core",
        "notice": "SUTRA is a decision-support system. All outputs require human verification."
    }


from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

DASHBOARD_DIR = Path(__file__).resolve().parent.parent / "dashboard"
if DASHBOARD_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(DASHBOARD_DIR)), name="static")

    @app.get("/")
    def index():
        index_file = DASHBOARD_DIR / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"status": "ok", "message": "SUTRA Backend Online"}

    from fastapi import Request

    @app.get("/favicon.ico", include_in_schema=False)
    def favicon():
        fav = DASHBOARD_DIR / "favicon.ico"
        if fav.exists():
            return FileResponse(str(fav))
        return FileResponse(str(DASHBOARD_DIR / "favicon.png"))

    @app.get("/favicon-32x32.png", include_in_schema=False)
    @app.get("/favicon-16x16.png", include_in_schema=False)
    @app.get("/apple-touch-icon.png", include_in_schema=False)
    @app.get("/favicon.png", include_in_schema=False)
    def favicon_png(request: Request):
        filename = request.url.path.lstrip("/")
        fav = DASHBOARD_DIR / filename
        if fav.exists():
            return FileResponse(str(fav))
        return FileResponse(str(DASHBOARD_DIR / "favicon.png"))


