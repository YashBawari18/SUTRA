# SŪTRA — Intelligence Dashboard Web Application

The **Dashboard** is the primary visual interface for investigators and analysts. It provides an intuitive workspace for network visualization, case exploration, document extraction, and report analysis.

---

## Architectural Principles

1. **Zero External Dependencies (Air-Gapped Ready)**:
   - Contains 100% embedded assets, including D3.js and system font stacks.
   - Requires zero external CDNs, making it safe and compliant for restricted or offline government networks.
2. **Interactive Force-Directed Knowledge Graph**:
   - Visualizes multi-entity networks (Persons, Phones, Bank Accounts, Locations, Vehicles, Organizations).
   - Dynamic node inspection with contextual risk dossiers, connection paths, and evidence traces.
3. **Multi-Language Accessibility (i18n)**:
   - Instant live language toggle between **English**, **Hindi (हिंदी)**, and **Marathi (मराठी)** across all UI elements and analytical reports.
4. **Human-in-the-Loop Decision Support**:
   - Interactive merge confidence thresholds and conflict resolution workflows.
   - Clear evidentiary tagging (`FACT`, `AI INFERENCE`, `INVESTIGATIVE LEAD`) to prevent automated bias.

---

## Workspace Modules

- **Command Center**: High-level statistical indicators, real-time investigation alerts, and detected network clusters.
- **Network Explorer**: Interactive graph workspace with search, zoom, filter, and detailed entity dossier inspection.
- **Entity Profiles**: Grid view of persons of interest, known aliases, last-known locations, and calculated risk indicators.
- **Data Lab**: Document inspector with highlighted entity extraction and live interactive NER testing sandbox.
- **AI Assistant**: Natural language query interface for evidence-grounded queries across the knowledge graph.
- **Analytics Report**: Formal multi-language intelligence report ready for export and human review.

---

## Running Locally

To serve the dashboard:
```bash
# Using Makefile
make dev

# Or using script
bash scripts/dev.sh
```
Open **`http://localhost:8080`** in any modern web browser.
