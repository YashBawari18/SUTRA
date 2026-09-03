# SŪTRA — Analytics Engine & Processing Pipeline

The **Engine** module contains the mathematical, statistical, graph-theoretic, and NLP pipelines that transform raw, multi-source investigative records into an actionable intelligence graph.

---

## The 7-Stage Analytical Pipeline

The pipeline executes in sequential order, where each stage ingests outputs from `/data` and produces enriched structured artifacts:

```
[1. generate_dataset.py] ──> Relational Records (FIRs, CDRs, Bank, Visits)
           │
[2. entity_resolution.py] ──> Confidence-Weighted Alias Resolution & Disambiguation
           │
[3. graph_analytics.py] ──> NetworkX Graph Construction, Centrality & Louvain Communities
           │
[4. risk_scoring.py] ──> Multi-Factor Anomaly & Explainable Risk Indicator Calculation
           │
[5. entity_extraction.py] ──> Rule-Based NER & Gazetteer Extraction from Raw Text
           │
[6. generate_report.py] ──> Multilingual Evidentiary Reports (English, Hindi, Marathi)
           │
[7. build_dashboard.py] ──> Self-Contained Web Bundle Compilation (dashboard/index.html)
```

---

## File Breakdown

| Script | Purpose | Key Output |
|---|---|---|
| `generate_dataset.py` | Generates realistic synthetic multi-source law-enforcement records (30 entities, 107 relations). | `data/*.csv`, `data/dataset.json` |
| `entity_resolution.py` | Performs Jaro-Winkler name similarity, shared identifier corroboration, and automated conflict identification. | `data/entity_resolution_results.json` |
| `graph_analytics.py` | Computes Degree Centrality, Betweenness Centrality, PageRank, shortest connection paths, and Louvain modularity communities. | `data/graph_analytics_results.json` |
| `risk_scoring.py` | Evaluates communication burst anomalies, financial anomalies, and location/temporal proximity with source-reliability weighting. | `data/risk_scores.json` |
| `entity_extraction.py` | Regex pattern matching and gazetteer dictionary NER to extract entities from raw police FIRs. | `data/extraction_results.json` |
| `generate_report.py` | Compiles structured investigative briefs tagged with `FACT`, `AI INFERENCE`, and `INVESTIGATIVE LEAD` in 3 languages. | `data/investigation_report_i18n.json` |
| `build_dashboard.py` | Compiles all generated JSON data, client app logic, and local D3.js into the single-file dashboard distribution. | `dashboard/index.html` |
| `dashboard_app.js` | Frontend client application logic, interactive state manager, and UI event controllers. | Embedded into `dashboard/index.html` |
| `d3.v7.min.js` | Embedded local copy of D3.js v7 for zero-network force-directed network graph rendering. | Embedded into `dashboard/index.html` |

---

## Running the Pipeline

You can run the entire pipeline at once:
```bash
# Using Makefile
make pipeline

# Or using the script
bash scripts/pipeline.sh
```
