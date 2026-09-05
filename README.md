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

---

## 🧰 Technologies & Frameworks

> Every technology below was chosen with a specific purpose inside SŪTRA — not just because it is popular.

---

### 🖥️ Frontend — *How investigators see and interact with intelligence*

| Technology | Used For in SŪTRA |
|---|---|
| **HTML5 / CSS3 / Vanilla JS** | Entire dashboard is a **single self-contained file** — no build step, no CDN, works completely offline in restricted government environments. |
| **D3.js v7** *(embedded locally)* | Renders the **interactive force-directed knowledge graph** — nodes are persons, phones, orgs, locations; edges are real investigated links. |
| **Three.js** *(embedded locally)* | Powers the **3D rotating globe** for spatial crime mapping across cities and districts. |
| **Web Workers** *(browser-native)* | Runs heavy graph layout calculations **off the main thread** so the UI never freezes during large network expansions. |

---

### ⚙️ Backend — *The secure API layer that gates all data access*

| Technology | Used For in SŪTRA |
|---|---|
| **Python 3.11+** | Core language for the entire backend and all 7 analytics pipeline stages. |
| **FastAPI** `v0.115` | Exposes all intelligence endpoints (`/graph`, `/entities`, `/reports`, `/upload`) with **automatic OpenAPI docs** for team integration. |
| **Uvicorn** `v0.30` | Production ASGI server — handles **concurrent investigator sessions** without blocking. |
| **Pydantic** `v2.9` | Strictly **validates every API request and response** — malformed case data is rejected before it enters the pipeline. |
| **SQLAlchemy** `v2.0` | ORM for all relational queries (people, calls, transactions, visits) against SQLite in dev or PostgreSQL in production. |
| **python-jose + Passlib** | Issues **JWT tokens** and hashes passwords for the **Role-Based Access Control (RBAC)** system — analysts vs. supervisors vs. admins. |
| **python-multipart** | Handles **FIR document and CDR file uploads** (PDF, CSV, images) from the dashboard. |

---

### 🗄️ Databases — *Where criminal network data lives*

| Technology | Used For in SŪTRA |
|---|---|
| **SQLite** | Lightweight **local development store** — zero setup, ships inside the repo as `sutra.db`. |
| **PostgreSQL** | **Production-grade relational backend** for persisting persons, calls, transactions, and full audit logs at scale. |
| **Neo4j** | **Native graph database** that stores and queries the criminal network as a true graph — shortest paths, common contacts, and community clusters run natively in Cypher. |

---

### 🔬 AI / ML & Analytics — *The intelligence engine*

| Technology | Used For in SŪTRA |
|---|---|
| **Anthropic Claude API** | The **evidence-grounded AI assistant** — answers investigator questions using only confirmed case facts, never hallucinated context. |
| **spaCy** `v3.7` | **NLP entity extraction** from raw FIR text — automatically identifies named persons, locations, phone numbers, and organizations from unstructured police reports. |
| **NetworkX** `v3.3` | Computes **graph centrality metrics** (Degree, Betweenness, PageRank) to rank who is the most connected and influential node in a network. |
| **Louvain Algorithm** *(via NetworkX)* | **Community detection** — automatically groups tightly connected suspects into criminal clusters without any manual labelling. |
| **Jaro-Winkler Distance** *(custom)* | **Entity disambiguation** — resolves aliases like "Ravi Kumar", "R. Kumar", and "Ravi K." to a single canonical identity with a confidence score. |
| **scikit-learn** `v1.5` | Flags **statistical outliers** in communication and financial patterns — e.g., a sudden spike in calls before an incident. |
| **NumPy + Pandas** | Powers the **multi-factor risk scoring formula** — ingests CDRs, bank transactions, and surveillance logs as structured arrays and computes weighted risk indicators. |

---

### 📄 Document Processing — *Turning paper FIRs into structured intelligence*

| Technology | Used For in SŪTRA |
|---|---|
| **PyMuPDF (fitz)** `v1.24` | **Parses uploaded PDF FIR documents** — extracts raw text from digital police reports for the NLP pipeline. |
| **pytesseract** `v0.3` | **OCR for scanned or handwritten FIRs** — converts image-based documents into machine-readable text before entity extraction. |

---

### 🐳 DevOps & Infrastructure — *How the system is deployed and run*

| Technology | Used For in SŪTRA |
|---|---|
| **Docker** | Each service (backend, Neo4j, PostgreSQL) runs in its **own isolated container** — reproducible across any deployment environment. |
| **Docker Compose** | **Single command orchestration** (`make db-up`) — spins up Neo4j + PostgreSQL + the FastAPI backend together in the correct startup order. |
| **GNU Make** | Developer-friendly **shortcut commands** — `make dev`, `make pipeline`, `make build`, `make test` abstract away complex multi-step workflows. |
| **Bash Scripts** | **Automated pipeline runner** (`pipeline.sh`) executes all 7 analytics stages in sequence; `test_system.sh` validates full system integrity before deployment. |

---

### 🌐 Multilingual Output — *Intelligence without language barriers*

| Language | Used For in SŪTRA |
|---|---|
| **English** | Primary interface language and default investigative report format. |
| **Hindi (हिंदी)** | Full intelligence report translation for Hindi-speaking investigators and senior officers. |
| **Marathi (मराठी)** | Full intelligence report translation for Maharashtra state law enforcement deployments. |
