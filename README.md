# SŪTRA — Criminal Network Intelligence Platform
> **Uncovering the Invisible Threads of Organized Crime**  
> *A unified decision-support platform for entity resolution, knowledge-graph analytics, and evidence-backed investigative leads — built for institutional accountability, not automated accusation.*

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/your-username/sutra.git
cd sutra

# 2. Launch the interactive intelligence dashboard (No setup required!)
make dev
# Opens at http://localhost:8080
```

---

## 🏛️ System Architecture

```
                                  ┌───────────────────────────────┐
                                  │   Multi-Source Ingestion      │
                                  │   (FIRs, CDRs, Bank, Visits)  │
                                  └───────────────┬───────────────┘
                                                  │
                                  ┌───────────────▼───────────────┐
                                  │   NLP Entity Extraction &     │
                                  │   Confidence Resolution       │
                                  └───────────────┬───────────────┘
                                                  │
                  ┌───────────────────────────────┴───────────────────────────────┐
                  │                                                               │
   ┌──────────────▼──────────────┐                                 ┌──────────────▼──────────────┐
   │     Graph Analytics Engine  │                                 │   Explainable Risk Engine   │
   │  • Network Centrality       │                                 │  • Communication Bursts     │
   │  • Louvain Communities      │                                 │  • Financial Anomalies      │
   │  • Shortest Connection Path │                                 │  • Source-Reliability Weight│
   └──────────────┬──────────────┘                                 └──────────────┬──────────────┘
                  │                                                               │
                  └───────────────────────────────┬───────────────────────────────┘
                                                  │
                                  ┌───────────────▼───────────────┐
                                  │   Investigative Workspace     │
                                  │  • Network Explorer (D3 Graph)│
                                  │  • Evidence-Grounded AI Asst  │
                                  │  • Multilingual Briefs (EN/HI)│
                                  └───────────────────────────────┘
```

---

## 📁 Repository Structure

```
sutra/
├── .editorconfig              # Consistent code style across editors
├── .gitattributes             # Git normalization rules for LF and binary files
├── .gitignore                 # Comprehensive Git ignore rules
├── Makefile                   # Quick developer shortcuts (dev, pipeline, backend, clean)
├── README.md                  # Project overview, architecture, and instructions
├── docker-compose.yml         # Container orchestration for Neo4j + PostgreSQL + Backend
│
├── backend/                   # FastAPI Production Backend & Database Layer
│   ├── .env.example           # Template environment variables
│   ├── Dockerfile             # Backend container definition
│   ├── README.md              # API documentation & database setup instructions
│   ├── auth.py                # Role-Based Access Control (RBAC) & JWT auth
│   ├── main.py                # FastAPI entrypoint & router aggregator
│   ├── requirements.txt       # Backend dependencies
│   ├── schema.cypher          # Neo4j graph schemas & indices
│   └── routers/               # Modular API endpoints (graph, entities, timeline, audit)
│
├── dashboard/                 # Frontend Web Application (Distribution)
│   ├── README.md              # Dashboard design & offline architecture
│   └── index.html             # Standalone, zero-CDN, interactive intelligence dashboard
│
├── data/                      # Synthetic Datasets & Pipeline Artifacts
│   ├── README.md              # Data dictionary & relational schema docs
│   ├── dataset.json           # Consolidated intelligence graph dataset
│   ├── *.csv                  # Relational tables (people, calls, transactions, visits)
│   └── *.json                 # Computed graph, risk, and entity resolution outputs
│
├── docs/                      # Comprehensive Architecture & Pitch Materials
│   ├── README.md              # Documentation index
│   ├── blueprint.md           # 40-part system design specification & SIH Q&A
│   └── presentation/          # SIH pitch deck slides and generator script
│
├── engine/                    # Core Analytics, Graph, Risk, & NLP Engines
│   ├── README.md              # Detailed breakdown of the 7 pipeline stages
│   ├── build_dashboard.py     # Compiles and bundles dashboard/index.html
│   ├── d3.v7.min.js           # Embedded local D3.js library (air-gapped ready)
│   ├── dashboard_app.js       # Client frontend logic & state management
│   ├── entity_extraction.py   # Rule-based NLP entity extractor
│   ├── entity_resolution.py   # Confidence-weighted alias resolution
│   ├── generate_dataset.py    # Synthetic investigation dataset generator
│   ├── generate_report.py     # Multilingual evidentiary report generator
│   ├── graph_analytics.py     # Centrality & Louvain community detection
│   └── risk_scoring.py        # Explainable anomaly & risk scoring formula
│
└── scripts/                   # Automated CLI Helper Scripts
    ├── dev.sh                 # Start local dashboard web server
    ├── pipeline.sh            # Run all 7 engine analysis stages in sequence
    └── test_system.sh         # End-to-end system validation test suite
```

---

## 🚀 Key Modules & Capabilities

### 1. Interactive Knowledge Graph (Network Explorer)
- Force-directed multi-entity graph powered by local D3.js.
- Inspect persons of interest, phone links, financial transactions, organizations, and location visits.
- Filter by node types, search by name/alias/phone, and trace connection pathways.

### 2. Multi-Factor Explainable Risk Scoring
- Transparent mathematical formulation combining:
  - **Communication Bursts** (CDR anomaly detection)
  - **Financial Irregularities** (High-value transaction outliers)
  - **Network Centrality** (Degree, Betweenness, PageRank)
  - **Temporal & Location Proximity** (Surveillance correlations)
  - **Source-Reliability Multipliers** (High / Medium / Low source weighting)
- Explicit institutional disclaimer: **All scores are decision-support indicators requiring human verification.**

### 3. Entity Resolution & Disambiguation
- Multi-signal matching (Jaro-Winkler string distance + phone/location corroboration).
- Interactive confidence threshold with human-in-the-loop review for conflicting matches.

### 4. Zero-CDN, Air-Gapped Security Architecture
- Embeds all visual engines (D3.js) and system font stacks inline.
- Operates 100% offline with zero external network requests — built specifically for restricted government environments.

### 5. Multilingual Intelligence Reports
- Instant translation across **English**, **Hindi (हिंदी)**, and **Marathi (मराठी)**.
- Standardized evidentiary tagging: `FACT`, `AI INFERENCE`, and `INVESTIGATIVE LEAD`.

---

## 🛠️ Developer Commands (`Makefile`)

| Command | Action |
|---|---|
| `make dev` | Serves the interactive dashboard locally at `http://localhost:8080`. |
| `make pipeline` | Runs all 7 data generation, entity resolution, and graph analytics stages. |
| `make build` | Rebuilds the single-file dashboard bundle from `engine/` source files. |
| `make test` | Executes the system verification and file integrity test suite. |
| `make db-up` | Launches Neo4j and PostgreSQL containers via Docker Compose. |
| `make db-down` | Stops and removes database containers. |
| `make backend` | Starts the FastAPI production backend server on port 8000. |
| `make clean` | Cleans `__pycache__`, temporary files, and OS artifacts. |

---

## 🔒 Security & Compliance Principles

- **Human-in-the-Loop Protocol**: AI suggests connections and computes risk flags; final investigative decisions always require human confirmation.
- **Audit Logging**: Structured trails recording every data upload, entity merge, and analysis execution.
- **Air-Gapped Compliant**: Zero external CDN calls or unvetted third-party telemetry.
- **Synthetic Data Demonstration**: Case files and identity records in this repository are synthetically generated for prototype demonstration.
