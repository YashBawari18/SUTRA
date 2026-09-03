# SŪTRA — Data Schemas & Knowledge Graph Artifacts

This directory houses the structured relational datasets and computed analytical outputs produced by the SŪTRA pipeline.

---

## Dataset Schema Overview

### 1. Relational Input Tables (Synthetic Data)

| File | Description | Key Fields |
|---|---|---|
| `people.csv` | Persons of interest and associates | `person_id`, `name`, `age`, `gender`, `role` |
| `phones.csv` | Registered mobile and burner devices | `phone_id`, `number`, `owner_person_id`, `service_provider` |
| `locations.csv` | Physical sites, hideouts, and business premises | `location_id`, `name`, `type`, `coordinates` |
| `vehicles.csv` | Motor vehicles identified in surveillance | `vehicle_id`, `plate_number`, `make_model`, `registered_owner_id` |
| `organizations.csv` | Front companies, shell corporations, and entities | `org_id`, `name`, `type`, `director_person_id` |
| `accounts.csv` | Financial accounts and banking details | `account_id`, `account_number`, `bank_name`, `holder_person_id` |
| `calls.csv` | Call Detail Records (CDRs) | `call_id`, `caller_phone_id`, `receiver_phone_id`, `timestamp`, `duration_seconds` |
| `transactions.csv` | Financial wire transfers and cash flows | `txn_id`, `from_account_id`, `to_account_id`, `amount`, `timestamp` |
| `visits.csv` | Physical surveillance observations | `visit_id`, `person_id`, `location_id`, `timestamp`, `notes` |
| `fir_records.csv` | Raw police reports and FIR narratives | `case_id`, `station`, `date`, `description`, `source_reliability` |

---

### 2. Computed Pipeline Artifacts (JSON Outputs)

| File | Generating Script | Contents |
|---|---|---|
| `dataset.json` | `generate_dataset.py` | Unified consolidated dictionary of all entities and relational links. |
| `entity_resolution_results.json` | `entity_resolution.py` | Disambiguation results, match confidence scores, and conflict flags. |
| `graph_analytics_results.json` | `graph_analytics.py` | Graph nodes, edges, centrality scores, and detected Louvain communities. |
| `risk_scores.json` | `risk_scoring.py` | Multi-factor risk indicators, sub-score breakdowns, and explanations. |
| `extraction_results.json` | `entity_extraction.py` | Structured entities extracted from unstructured FIR texts. |
| `investigation_report_i18n.json` | `generate_report.py` | Multi-lingual tagged investigative briefing (English, Hindi, Marathi). |
| `investigation_report.txt` | `generate_report.py` | Plaintext English copy of the investigative report. |
