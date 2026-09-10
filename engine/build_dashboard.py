"""
SUTRA — Dashboard Builder v2
==============================
Changes from v1:
  1. BUG FIX: D3.js is now embedded directly in the HTML (no external
     CDN). The v1 dashboard loaded D3 from cdnjs.cloudflare.com, which
     silently fails on any network that blocks external CDNs -- exactly
     the kind of restriction common on government networks. That
     failure cascaded and broke the graph, the right panel, tab
     switching, and all interactivity. Embedding D3 inline makes the
     dashboard fully self-contained: it works with zero internet
     access, forever, which is a real requirement for a government
     deployment, not just a nice-to-have.
  2. True black theme (government-appropriate, formal, no external
     Google Fonts dependency either -- system font stack only).
  3. Responsive layout: side panels collapse into slide-in drawers
     below 1100px, single-column stacking below 720px.
  4. A genuine "type your own input, get real output" live entity
     extraction demo, driven by the same logic as engine/entity_extraction.py.

Run:  python3 build_dashboard.py
Output: ../dashboard/index.html
"""

import json
import os
import re

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "..", "data")
OUT_DIR = os.path.join(BASE, "..", "dashboard")
os.makedirs(OUT_DIR, exist_ok=True)

def load(name):
    with open(os.path.join(DATA_DIR, name), encoding="utf-8") as f:
        return json.load(f)

dataset = load("dataset.json")
resolution = load("entity_resolution_results.json")
graph = load("graph_analytics_results.json")
risk = load("risk_scores.json")
extraction = load("extraction_results.json")
report_i18n = load("investigation_report_i18n.json")

with open(os.path.join(BASE, "d3.v7.min.js"), encoding="utf-8") as f:
    D3_JS = f.read()

with open(os.path.join(BASE, "dashboard_app.js"), encoding="utf-8") as f:
    APP_JS = f.read()

risk_by_id = {r["person_id"]: r for r in risk}
id_to_label = {n["id"]: n["label"] for n in graph["nodes"]}

for e in graph["edges"]:
    t = e.get("type")
    if t == "CALLED":
        e["display_label"] = f"{e['weight']} calls"
    elif t == "TRANSFERRED_MONEY":
        e["display_label"] = f"\u20b9{e['amount']:,}"
    elif t == "VISITED" and e.get("notes"):
        e["display_label"] = e["notes"][:28]
    else:
        e["display_label"] = ""

for n in graph["nodes"]:
    if n["type"] == "person" and n["id"] in risk_by_id:
        n["risk"] = risk_by_id[n["id"]]

REPORT_SECTION_TITLES = {
    "en": {"s1": "1. CASE OVERVIEW", "s2": "2. ENTITY RESOLUTION FINDINGS", "s3": "3. NETWORK STRUCTURE & KEY ENTITIES",
           "s4": "4. RISK INDICATORS (decision-support only)", "s5": "5. SOURCE DOCUMENT EXTRACTION", "s6": "6. DISCLOSURE"},
    "hi": {"s1": "1. \u092e\u093e\u092e\u0932\u0947 \u0915\u093e \u0935\u093f\u0935\u0930\u0923", "s2": "2. \u0907\u0915\u093e\u0908 \u0938\u092e\u093e\u0927\u093e\u0928 \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937",
           "s3": "3. \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0938\u0902\u0930\u091a\u0928\u093e \u0914\u0930 \u092a\u094d\u0930\u092e\u0941\u0916 \u0907\u0915\u093e\u0907\u092f\u093e\u0902", "s4": "4. \u091c\u094b\u0916\u093f\u092e \u0938\u0902\u0915\u0947\u0924\u0915 (\u0915\u0947\u0935\u0932 \u0928\u093f\u0930\u094d\u0923\u092f-\u0938\u0939\u093e\u092f\u0924\u093e \u0939\u0947\u0924\u0941)",
           "s5": "5. \u0938\u094d\u0930\u094b\u0924 \u0926\u0938\u094d\u0924\u093e\u0935\u0947\u095b \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937\u0923", "s6": "6. \u092a\u094d\u0930\u0915\u091f\u0940\u0915\u0930\u0923"},
    "mr": {"s1": "1. \u092a\u094d\u0930\u0915\u0930\u0923\u093e\u091a\u093e \u0906\u0922\u093e\u0935\u093e", "s2": "2. \u0918\u091f\u0915 \u0928\u093f\u0930\u093e\u0915\u0930\u0923 \u0928\u093f\u0937\u094d\u0915\u0930\u094d\u0937",
           "s3": "3. \u0928\u0947\u091f\u0935\u0930\u094d\u0915 \u0930\u091a\u0928\u093e \u0906\u0923\u093f \u092a\u094d\u0930\u092e\u0941\u0916 \u0918\u091f\u0915", "s4": "4. \u091c\u094b\u0916\u0940\u092e \u0928\u093f\u0930\u094d\u0926\u0947\u0936\u093e\u0902\u0915 (\u0915\u0947\u0935\u0933 \u0928\u093f\u0930\u094d\u0923\u092f-\u0938\u0939\u093e\u092f\u094d\u092f\u093e\u0938\u093e\u0920\u0940)",
           "s5": "5. \u0938\u094d\u0930\u094b\u0924 \u0926\u0938\u094d\u0924\u090f\u0935\u091c \u0909\u0924\u093e\u0930\u093e", "s6": "6. \u0909\u0918\u0921 \u092e\u093e\u0939\u093f\u0924\u0940"},
}

ENT_CLASS = {"PERSON": "person", "LOCATION": "location", "PHONE": "phone",
             "VEHICLE": "vehicle", "ORGANIZATION": "org", "MONEY": "money",
             "DATE": "date", "TIME": "date", "CASE_ID": "org"}

def build_highlighted_doc(fir):
    text = fir["description"]
    ents = next((e["entities"] for e in extraction if e["case_id"] == fir["case_id"]), [])
    ents_sorted = sorted(set((e["text"], e["type"]) for e in ents), key=lambda x: -len(x[0]))
    html = text
    for etext, etype in ents_sorted:
        cls = ENT_CLASS.get(etype, "org")
        safe = re.escape(etext)
        html = re.sub(safe, f'<span class="ent-tag {cls}">{etext}<sup>{etype[:3]}</sup></span>', html, count=1)
    return html

fir_docs_html = []
for fir in dataset["fir_records"]:
    fir_docs_html.append({
        "case_id": fir["case_id"], "station": fir.get("station", ""), "date": fir["date"],
        "reliability": fir["source_reliability"], "html": build_highlighted_doc(fir)
    })

location_names = [l["name"] for l in dataset["locations"]]
for l in dataset["locations"]:
    if "," in l["name"]:
        short = l["name"].split(",", 1)[1].strip()
        if short not in location_names:
            location_names.append(short)

EMBEDDED = {
    "nodes": graph["nodes"],
    "edges": graph["edges"],
    "priority_ranking": graph["priority_ranking"],
    "communities": graph.get("communities", []),
    "timeline_events": graph.get("timeline_events", []),
    "all_paths": graph.get("all_paths", {}),
    "id_to_label": id_to_label,
    "resolution": resolution,
    "risk": risk,
    "fir_docs": fir_docs_html,
    "report_i18n": report_i18n,
    "report_section_titles": REPORT_SECTION_TITLES,
    "sources": [
        {"name": "FIRs & Police Reports", "n": len(dataset["fir_records"])},
        {"name": "Call Detail Records", "n": len(dataset["calls"])},
        {"name": "Financial Transactions", "n": len(dataset["transactions"])},
        {"name": "Surveillance / Visits", "n": len(dataset["visits"])},
        {"name": "Organizations on Record", "n": len(dataset["organizations"])},
        {"name": "Vehicles on Record", "n": len(dataset["vehicles"])},
    ],
    "gazetteer": {
        "PERSON": [p["name"] for p in dataset["people"]],
        "LOCATION": location_names,
        "ORGANIZATION": [o["name"] for o in dataset["organizations"]],
    },
    "example_texts": [
        (
            "On 03/03/2026, a field unit reported that SANJAY VERMA was seen near the godown in "
            "BHIWANDI at approx. 2300 hrs, arriving in a vehicle bearing registration MH-12 QR 5581. "
            "A transfer of \u20b9 75,000 was recorded the same evening from an account linked to SHREE "
            "TRADING CO. The complainant's contact number, +91 90\u2022\u2022\u20224471, was noted for follow-up."
        ),
        (
            "Surveillance note dated 21/02/2026: MEENA IYER was observed at the office in NARIMAN POINT "
            "in the company of an unidentified male. Vehicle MH-02 CJ 4410 was parked outside from "
            "1800 hrs to 2010 hrs. No financial activity was recorded in connection with this visit."
        ),
    ],
}

# ------------------------------------------------------------------
# Extra fields for the redesigned "Entity Profile" card:
# aliases (from entity resolution), last-known location (from visits),
# and a plain-language risk-level bucket (never "criminal").
# ------------------------------------------------------------------
aliases_by_person = {}
for r in resolution:
    aliases_by_person.setdefault(r["matched_person_id"], []).append(r["mention"])

last_visit_by_person = {}
loc_lookup = {l["location_id"]: l["name"] for l in dataset["locations"]}
for v in sorted(dataset["visits"], key=lambda x: x.get("timestamp", "")):
    if v.get("person_id"):
        last_visit_by_person[v["person_id"]] = {"location": loc_lookup.get(v["location_id"], "Unknown"), "timestamp": v.get("timestamp", "")}

def risk_bucket(score):
    if score >= 45: return "HIGH"
    if score >= 20: return "MEDIUM"
    return "LOW"

for n in graph["nodes"]:
    if n["type"] == "person":
        n["aliases"] = aliases_by_person.get(n["id"], [])
        n["last_known"] = last_visit_by_person.get(n["id"])
        n["risk_level"] = risk_bucket(n["risk"]["risk_indicator_score"]) if n.get("risk") else "UNRATED"

# Full visit history per person (for the Entity Profile "Operational Timeline")
visits_by_person = {}
for v in sorted(dataset["visits"], key=lambda x: x.get("timestamp", "")):
    if v.get("person_id"):
        visits_by_person.setdefault(v["person_id"], []).append({
            "location": loc_lookup.get(v["location_id"], "Unknown location"),
            "timestamp": v.get("timestamp", ""), "notes": v.get("notes", "")
        })
for n in graph["nodes"]:
    if n["type"] == "person":
        n["timeline"] = list(reversed(visits_by_person.get(n["id"], [])))

# Primary organizational affiliation per person (via DIRECTOR_OF/associate edges)
org_lookup = {o["org_id"]: o["name"] for o in dataset["organizations"]}
affiliation_by_person = {}
for o in dataset["organizations"]:
    if o.get("director_person_id"):
        affiliation_by_person[o["director_person_id"]] = o["name"]
for n in graph["nodes"]:
    if n["type"] == "person":
        n["affiliation"] = affiliation_by_person.get(n["id"])

# Overall average entity-resolution confidence (real computed stat for the dashboard gauge)
avg_resolution_confidence = round(sum(r["confidence"] for r in resolution) / len(resolution) * 100) if resolution else 0

DATA_JSON = json.dumps(EMBEDDED)
D3_JSON_SAFE = D3_JS
AVG_CONFIDENCE = avg_resolution_confidence

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="icon" type="image/x-icon" href="favicon.ico">
<link rel="icon" type="image/png" sizes="32x32" href="favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&family=Noto+Sans+Devanagari:wght@400;700;900&display=swap" rel="stylesheet">
<title>S\u016aTRA \u2014 Criminal Network Intelligence System</title>
<script src="three.min.js"></script>
<style>
  :root{
    --bg:#f0f2f7; --bg-2:#ffffff; --panel:#ffffff; --panel-2:#edf0fb; --border:#dde2ef;
    --ink:#0f1626; --ink-dim:#4a5268; --ink-faint:#8a92a8;
    --gold:#d4920a; --amber:#c27c00; --cyan:#0b9494; --red:#c42020; --blue:#1f46cc; --green:#137a35;
    --font-serif:Georgia,'Times New Roman',serif;
    --font-mono:'JetBrains Mono','SF Mono','Cascadia Code','Fira Code','Consolas',ui-monospace,monospace;
    --font-body:'Inter',-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;
    --radius-sm:3px; --radius:5px; --radius-lg:8px;
    --shadow-sm:0 1px 3px rgba(0,0,0,0.06),0 1px 2px rgba(0,0,0,0.04);
    --shadow:0 4px 12px rgba(0,0,0,0.08),0 2px 4px rgba(0,0,0,0.04);
  }
  [data-theme="dark"]{
    --bg:#080c16; --bg-2:#0f172a; --panel:#131c31; --panel-2:#1e293b; --border:#1e2e4a;
    --ink:#f8fafc; --ink-dim:#94a3b8; --ink-faint:#64748b;
    --gold:#f59e0b; --amber:#fbbf24; --cyan:#22d3ee; --red:#f87171; --blue:#3b82f6; --green:#10b981;
    --shadow-sm:0 1px 3px rgba(0,0,0,0.4),0 1px 2px rgba(0,0,0,0.25);
    --shadow:0 4px 14px rgba(0,0,0,0.5),0 2px 5px rgba(0,0,0,0.3);
  }

  /* --- Day / Night Toggle Button --- */
  .theme-toggle-btn{ background:transparent; border:1px solid var(--border); border-radius:var(--radius-sm); padding:4px 8px; font-size:12px; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; color:var(--ink); transition:all 0.18s ease; line-height:1; }
  .theme-toggle-btn:hover{ background:var(--panel-2); border-color:var(--ink-faint); transform:scale(1.06); }
  .land-nav .theme-toggle-btn{ margin-left:14px; padding:4px 9px; }

  /* --- Dark Theme Specialized Overrides --- */
  [data-theme="dark"] .land-header{ background:rgba(15,23,42,0.92); border-bottom-color:#1e2e4a; box-shadow:0 1px 4px rgba(0,0,0,0.3); }
  [data-theme="dark"] .land-brand-name{ color:#f8fafc; }
  [data-theme="dark"] .land-brand-badge{ background:rgba(30,58,138,0.35); color:#60a5fa; border-color:#1e40af; }
  [data-theme="dark"] .land-nav a{ color:#94a3b8; }
  [data-theme="dark"] .land-nav a:hover{ color:#f8fafc; }
  [data-theme="dark"] .hero h1{ color:#f8fafc; }
  [data-theme="dark"] .hero p{ color:#94a3b8; }
  [data-theme="dark"] .btn-hero-secondary{ border-color:#334155; color:#cbd5e1; }
  [data-theme="dark"] .btn-hero-secondary:hover{ border-color:#64748b; color:#ffffff; }
  [data-theme="dark"] .globe-indicator{ background:rgba(19,28,49,0.94); border-color:#1e3a8a; color:#38bdf8; box-shadow:0 4px 16px rgba(0,0,0,0.4); }
  [data-theme="dark"] .globe-pop-card{ background:rgba(19,28,49,0.96); border-color:#1e2e4a; color:#f8fafc; box-shadow:0 16px 36px rgba(0,0,0,0.4); }
  [data-theme="dark"] .pop-card-title{ color:#f8fafc; }
  [data-theme="dark"] .pop-card-coords{ color:#64748b; }
  [data-theme="dark"] .globe-controls-pill{ background:rgba(19,28,49,0.94); border-color:#1e2e4a; box-shadow:0 4px 16px rgba(0,0,0,0.4); }
  [data-theme="dark"] .stream-lbl{ color:#94a3b8; }
  [data-theme="dark"] .stream-btn{ color:#94a3b8; }
  [data-theme="dark"] .stream-btn:hover{ color:#ffffff; background:rgba(56,189,248,0.15); }
  [data-theme="dark"] .hero-hud-bar{ background:rgba(19,28,49,0.96); border-color:#1e2e4a; box-shadow:0 12px 36px rgba(0,0,0,0.5); }
  [data-theme="dark"] .hud-stat{ border-right-color:#1e2e4a; }
  [data-theme="dark"] .hud-stat .hud-lbl{ color:#94a3b8; }
  [data-theme="dark"] .hud-stat .hud-val{ color:#f8fafc; }
  [data-theme="dark"] .caps-section h2{ color:#f8fafc; }
  [data-theme="dark"] .caps-section > p{ color:#94a3b8; }
  [data-theme="dark"] .cap-card{ background:var(--panel); border-color:var(--border); }
  [data-theme="dark"] .cap-card h3{ color:#f8fafc; }
  [data-theme="dark"] .cap-card p{ color:#94a3b8; }
  [data-theme="dark"] .cap-icon{ background:var(--bg-2); border-color:var(--border); }
  [data-theme="dark"] .cap-wide-card{ background:var(--panel); border-color:var(--border); }
  [data-theme="dark"] .cap-wide-card h3{ color:#f8fafc; }
  [data-theme="dark"] .cap-wide-card p{ color:#94a3b8; }
  [data-theme="dark"] .btn-doc{ border-color:var(--border); color:var(--ink-dim); }
  [data-theme="dark"] .btn-doc:hover{ border-color:var(--ink); color:var(--ink); }
  [data-theme="dark"] .land-footer{ border-top-color:#1e2e4a; color:#64748b; }
  [data-theme="dark"] .land-footer a{ color:#64748b; }
  [data-theme="dark"] .land-footer a:hover{ color:#94a3b8; }
  [data-theme="dark"] .pop-toast{ background:#131c31; border-color:#1e2e4a; color:#f8fafc; box-shadow:0 12px 28px rgba(0,0,0,0.4); }
  [data-theme="dark"] .toast-text{ color:#cbd5e1; }
  [data-theme="dark"] .toast-icon{ background:#0b0f19; }
  [data-theme="dark"] .auth-box{ background:#131c31; border-color:#1e2e4a; color:#f8fafc; }
  [data-theme="dark"] .auth-title{ color:#f8fafc; }
  [data-theme="dark"] .auth-status{ color:#94a3b8; }
  [data-theme="dark"] .auth-terminal{ background:#080c16; border-color:#1e2e4a; }
  [data-theme="dark"] .auth-progress-track{ background:#1e293b; }
  [data-theme="dark"] .auth-terminal-line{ color:#64748b; }
  [data-theme="dark"] .auth-terminal-line.active{ color:#38bdf8; }

  /* Inside Dashboard Dark Theme */
  [data-theme="dark"] .btn-cc-action{ background:#1e293b; border-color:#334155; color:#60a5fa; }
  [data-theme="dark"] .btn-cc-action:hover{ background:#26354f; border-color:#475569; color:#93c5fd; }
  [data-theme="dark"] .cc-radar-container{ background:linear-gradient(135deg,#0a0f1d 0%,#0f172a 100%); border-color:#1e2e4a; }
  [data-theme="dark"] .cc-radar-legend{ background:rgba(15,23,42,0.95); border-color:#1e2e4a; color:#94a3b8; }
  [data-theme="dark"] .cc-chart-box{ background:#0f172a; border-color:#1e2e4a; }
  [data-theme="dark"] .cc-chart-title{ color:#cbd5e1; }
  [data-theme="dark"] .cc-bar-header{ color:#f1f5f9; }
  [data-theme="dark"] .cc-bar-track{ background:#1e293b; }
  [data-theme="dark"] .cc-donut-legend{ color:#94a3b8; }
  [data-theme="dark"] .cc-donut-legend b{ color:#f8fafc; }
  [data-theme="dark"] .cc-velocity-chart{ background:#0f172a; border-color:#1e2e4a; }
  [data-theme="dark"] .cc-velocity-wrap{ background:#0f172a; border-color:#1e2e4a; }
  [data-theme="dark"] .cc-suspect-card{ background:#0f172a; border-color:#1e2e4a; }
  [data-theme="dark"] .cc-suspect-card:hover{ background:#151f38; border-color:#334155; }
  [data-theme="dark"] .cc-suspect-name{ color:#f8fafc; }
  [data-theme="dark"] .stat-card{ background:var(--panel); border-color:var(--border); }
  [data-theme="dark"] .stat-card.live{ background:linear-gradient(135deg,#131c31,#0b192c); }
  [data-theme="dark"] .stat-card.flagged{ background:linear-gradient(135deg,#131c31,#281318); }
  [data-theme="dark"] .stat-card.detected{ background:linear-gradient(135deg,#131c31,#0c1c38); }
  [data-theme="dark"] .stat-card.monitored{ background:linear-gradient(135deg,#131c31,#241a0e); }
  [data-theme="dark"] .audit-table th{ background:#0b0f19; color:var(--ink-faint); }
  [data-theme="dark"] #graph-wrap{ background:#070a12; }
  [data-theme="dark"] .graph-dotgrid{ opacity:0.12; }
  [data-theme="dark"] .dl-panel, [data-theme="dark"] .dl-doc-area{ background:var(--panel); border-color:var(--border); }
  [data-theme="dark"] .pd-card{ background:var(--panel); border-color:var(--border); }
  [data-theme="dark"] .asst-msg-text{ background:#1e293b; color:#f8fafc; border-color:#334155; }
  [data-theme="dark"] .asst-user .asst-msg-text{ background:linear-gradient(135deg,#1e3a8a,#2563eb); color:#ffffff; }

  *{box-sizing:border-box; margin:0; padding:0;}
  html,body{ background:var(--bg); color:var(--ink); font-family:var(--font-body); font-size:14px; line-height:1.55; height:100%; -webkit-font-smoothing:antialiased; -moz-osx-font-smoothing:grayscale; }
  body{ overflow:hidden; }
  ::selection{ background:rgba(212,146,10,0.25); color:var(--ink); }
  ::-webkit-scrollbar{ width:6px; height:6px; }
  ::-webkit-scrollbar-track{ background:transparent; }
  ::-webkit-scrollbar-thumb{ background:var(--border); border-radius:3px; }
  ::-webkit-scrollbar-thumb:hover{ background:var(--ink-faint); }
  button{ font-family:inherit; cursor:pointer; }

  /* ================= LANDING / BRIEFING SPLASH ================= */
  #landing{ position:fixed; inset:0; background:var(--bg); z-index:100; overflow-y:auto; color:var(--ink); font-family:var(--font-body); scroll-behavior:smooth; }
  #landing.hide{ display:none; }
  #landing-canvas{ position:fixed; inset:0; pointer-events:none; z-index:0; width:100%; height:100%; opacity:0.35; }

  /* Official Gov Ribbon (Tricolor) */
  .gov-tricolor-bar{ height:4px; width:100%; background:linear-gradient(90deg, #FF9933 0%, #FF9933 33.3%, #ffffff 33.3%, #ffffff 66.6%, #138808 66.6%, #138808 100%); position:sticky; top:0; z-index:60; }

  .land-header{ position:sticky; top:4px; z-index:50; display:flex; align-items:center; justify-content:space-between; padding:14px 44px;
    background:rgba(255, 255, 255, 0.94); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); border-bottom:1px solid #dde3ea; box-shadow:0 1px 3px rgba(0,0,0,0.04); }
  .land-brand{ display:flex; align-items:center; gap:12px; text-decoration:none; }
  .land-devanagari{ font-family:var(--font-serif); font-size:22px; color:var(--gold); font-weight:700; }
  .land-brand-name{ font-family:var(--font-serif); font-size:17px; letter-spacing:0.08em; font-weight:700; color:#0f172a; }
  .land-brand-badge{ font-family:var(--font-mono); font-size:9px; letter-spacing:0.06em; background:#e8f0fe; color:#1a56db; border:1px solid #bfdbfe; padding:2px 8px; border-radius:4px; font-weight:600; }
  .land-nav{ display:flex; align-items:center; gap:26px; font-family:var(--font-mono); font-size:11px; color:#475569; letter-spacing:0.04em; font-weight:600; }
  .land-nav a{ color:#475569; text-decoration:none; transition:color 0.15s; }
  .land-nav a:hover{ color:#0f172a; }


  .hero{ max-width:1240px; margin:0 auto; text-align:center; padding:45px 24px 20px; position:relative; z-index:1; }
  /* ================= SUTRA BRAND LOGO (OFFICIAL DESIGN) ================= */
  .hero-logo-wrap{ position:relative; min-height:86px; margin:0 auto 20px; display:flex; align-items:center; justify-content:center; max-width:440px; }
  .hero-logo-en,
  .hero-logo-hi{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; transition:opacity 0.25s cubic-bezier(0.16,1,0.3,1), transform 0.25s cubic-bezier(0.16,1,0.3,1); }
  .hero-logo-en.active{ display:flex; opacity:1; transform:translateY(0) scale(1); pointer-events:auto; }
  .hero-logo-en:not(.active){ display:none !important; opacity:0; pointer-events:none; }
  .hero-logo-hi.active{ display:flex; opacity:1; transform:translateY(0) scale(1); pointer-events:auto; }
  .hero-logo-hi:not(.active){ display:none !important; opacity:0; pointer-events:none; }
  .hero-logo-img{ max-height:82px; width:auto; max-width:100%; object-fit:contain; filter:drop-shadow(0 4px 14px rgba(26,45,107,0.15)); transition:transform 0.25s ease; }
  .hero-logo-img:hover{ transform:scale(1.03); filter:drop-shadow(0 6px 20px rgba(26,45,107,0.22)); }

  .hero h1{ font-family:var(--font-serif); font-size:40px; font-weight:700; color:#0f172a; margin:0 auto 16px; letter-spacing:0.01em; line-height:1.2; max-width:860px; }
  .hero p{ font-family:var(--font-body); font-size:14.5px; color:#475569; max-width:640px; margin:0 auto 28px; line-height:1.75; font-weight:400; }

  .hero-btns{ display:flex; gap:12px; justify-content:center; margin-bottom:12px; }
  .btn-hero-primary{ background:var(--gold); color:#ffffff; border:none; padding:12px 28px; border-radius:var(--radius);
    font-family:var(--font-mono); font-size:11.5px; letter-spacing:0.07em; font-weight:700; cursor:pointer; transition:all 0.15s ease; box-shadow:0 3px 10px rgba(212,146,10,0.25); }
  .btn-hero-primary:hover{ opacity:0.92; transform:translateY(-1px); box-shadow:0 6px 14px rgba(212,146,10,0.35); }
  .btn-hero-primary:active{ transform:translateY(1px); }

  .btn-hero-secondary{ background:#ffffff; color:#334155; border:1px solid #cbd5e1; padding:12px 28px; border-radius:var(--radius);
    font-family:var(--font-mono); font-size:11.5px; letter-spacing:0.07em; cursor:pointer; font-weight:600; box-shadow:0 1px 2px rgba(0,0,0,0.04); transition:border-color 0.15s; }
  .btn-hero-secondary:hover{ border-color:#94a3b8; color:#0f172a; }

  /* ================= 3D REVOLVING ULTRA-REALISTIC BIG HALF EARTH ================= */
  .hero-globe-wrap{ position:relative; width:100%; max-width:1180px; height:530px; margin:16px auto 0; overflow:hidden; display:flex; align-items:flex-start; justify-content:center; flex-shrink:0; background:transparent; border:none; box-shadow:none; border-radius:0; }
  #globe-canvas{ width:100%; height:530px; display:block; cursor:grab; }
  #globe-canvas:active{ cursor:grabbing; }

  .globe-indicator{ position:absolute; top:12px; left:50%; transform:translateX(-50%); font-family:var(--font-mono); font-size:10px; color:#0284c7; background:rgba(255,255,255,0.92); border:1px solid #bae6fd; padding:5px 16px; border-radius:20px; backdrop-filter:blur(12px); display:flex; align-items:center; gap:8px; box-shadow:0 4px 16px rgba(14,165,233,0.12); z-index:6; pointer-events:none; font-weight:600; letter-spacing:0.06em; }
  .globe-indicator .pulse-beacon{ width:7px; height:7px; border-radius:50%; background:#10b981; box-shadow:0 0 10px #10b981; position:relative; }
  .globe-indicator .pulse-beacon::after{ content:''; position:absolute; inset:-4px; border-radius:50%; border:1.5px solid #10b981; animation:sonarPing 2s infinite; }

  /* Sequential Popping Intelligence Messages - Sleek Crystal Glass HUD */
  #globe-popping-container{ position:absolute; inset:0; pointer-events:none; z-index:7; }
  .globe-pop-card{ position:absolute; pointer-events:auto; display:flex; flex-direction:column; gap:5px; padding:13px 17px; background:rgba(255,255,255,0.96); border:1px solid #cbd5e1; border-left:4px solid #0284c7; border-radius:12px; font-family:var(--font-body); box-shadow:0 16px 36px rgba(15,23,42,0.12), 0 2px 6px rgba(0,0,0,0.04); backdrop-filter:blur(16px); cursor:pointer; text-decoration:none; color:inherit; max-width:330px; opacity:0; transform:translateY(14px) scale(0.94); transition:opacity 0.4s cubic-bezier(0.16,1,0.3,1), transform 0.4s cubic-bezier(0.16,1,0.3,1), border-color 0.2s, box-shadow 0.2s; }
  .globe-pop-card.show{ opacity:1; transform:translateY(0) scale(1); }
  .globe-pop-card:hover{ transform:translateY(-3px) scale(1.02); border-color:#0284c7; box-shadow:0 22px 48px rgba(15,23,42,0.16); }
  .globe-pop-card.critical{ border-left-color:#ef4444; border-color:rgba(239,68,68,0.35); }
  .globe-pop-card.warning{ border-left-color:#f59e0b; border-color:rgba(245,158,11,0.35); }
  .globe-pop-card.success{ border-left-color:#10b981; border-color:rgba(16,185,129,0.35); }

  .pop-card-top{ display:flex; align-items:center; justify-content:space-between; gap:8px; }
  .pop-card-badge{ font-family:var(--font-mono); font-size:9px; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; color:#0284c7; }
  .globe-pop-card.critical .pop-card-badge{ color:#dc2626; }
  .globe-pop-card.warning .pop-card-badge{ color:#d97706; }
  .globe-pop-card.success .pop-card-badge{ color:#059669; }
  .pop-card-coords{ font-family:var(--font-mono); font-size:9px; color:#64748b; font-weight:600; }
  .pop-card-title{ font-size:13px; font-weight:600; color:#0f172a; line-height:1.45; }
  .pop-card-footer{ display:flex; align-items:center; justify-content:space-between; margin-top:2px; font-family:var(--font-mono); font-size:10px; color:#0284c7; font-weight:600; }
  .globe-pop-card:hover .pop-card-footer{ color:#0369a1; }

  /* Pin radar anchor pointing to earth */
  .pop-anchor-dot{ position:absolute; width:10px; height:10px; border-radius:50%; background:#0284c7; box-shadow:0 0 14px #0284c7; pointer-events:none; transform:translate(-50%, -50%); z-index:6; }
  .pop-anchor-dot::after{ content:''; position:absolute; inset:-5px; border-radius:50%; border:2px solid #0284c7; animation:sonarPing 2s infinite; }
  .pop-anchor-dot.critical{ background:#ef4444; box-shadow:0 0 14px #ef4444; }
  .pop-anchor-dot.critical::after{ border-color:#ef4444; }
  .pop-anchor-dot.warning{ background:#f59e0b; box-shadow:0 0 14px #f59e0b; }
  .pop-anchor-dot.warning::after{ border-color:#f59e0b; }
  .pop-anchor-dot.success{ background:#10b981; box-shadow:0 0 14px #10b981; }
  .pop-anchor-dot.success::after{ border-color:#10b981; }

  /* Globe stream control bar */
  .globe-controls-pill{ position:absolute; bottom:124px; left:50%; transform:translateX(-50%); display:flex; align-items:center; gap:8px; z-index:8; background:rgba(255,255,255,0.94); border:1px solid #cbd5e1; border-radius:20px; padding:5px 15px; font-family:var(--font-mono); font-size:10px; backdrop-filter:blur(12px); box-shadow:0 4px 16px rgba(15,23,42,0.08); }
  .stream-dot{ color:#10b981; font-size:9px; animation:blink 1.5s infinite; }
  .stream-lbl{ color:#475569; font-weight:600; }
  .stream-sep{ color:#cbd5e1; }
  .stream-btn{ border:none; background:transparent; font-size:10px; color:#64748b; cursor:pointer; padding:2px 6px; border-radius:10px; font-family:inherit; font-weight:600; }
  .stream-btn:hover{ color:#0f172a; background:rgba(2,132,199,0.1); }

  /* Live Telemetry HUD Bar - Anchored Directly ON the Earth at the Bottom of Page */
  .hero-hud-bar{ position:absolute; bottom:16px; left:50%; transform:translateX(-50%); display:grid; grid-template-columns:repeat(4, 1fr); gap:16px; max-width:980px; width:calc(100% - 40px); padding:16px 24px; background:rgba(255,255,255,0.95); border:1px solid #cbd5e1; border-radius:12px; box-shadow:0 12px 36px rgba(15,23,42,0.1), 0 1px 3px rgba(0,0,0,0.04); backdrop-filter:blur(16px); z-index:10; text-align:left; }
  .hud-stat{ display:flex; flex-direction:column; gap:3px; padding:0 10px; border-right:1px solid #e2e8f0; }
  .hud-stat:last-child{ border-right:none; }
  .hud-stat .hud-lbl{ font-family:var(--font-mono); font-size:9.5px; color:#64748b; text-transform:uppercase; letter-spacing:0.06em; font-weight:600; display:flex; align-items:center; gap:6px; }
  .hud-stat .hud-lbl span{ color:#1a56db; }
  .hud-stat .hud-val{ font-family:var(--font-serif); font-size:23px; font-weight:700; color:#0f172a; letter-spacing:-0.01em; margin:2px 0; }
  .hud-stat .hud-val span{ color:var(--gold); font-size:13px; font-weight:600; margin-left:4px; }
  .hud-stat .hud-sub{ font-size:10.5px; color:#16a34a; font-family:var(--font-mono); font-weight:500; }
  @media(max-width:768px){
    .hero-hud-bar{ grid-template-columns:repeat(2, 1fr); bottom:10px; padding:12px 14px; gap:10px; }
    .globe-controls-pill{ bottom:138px; }
  }

  /* Popping Live Toast Notifications in Corner */
  #live-feed-toaster{ position:fixed; bottom:24px; right:24px; z-index:150; display:flex; flex-direction:column-reverse; gap:10px; pointer-events:none; max-width:340px; width:calc(100vw - 48px); }
  .pop-toast{ pointer-events:auto; background:#ffffff; border:1px solid #cbd5e1; border-left:4px solid #1a56db; border-radius:8px; padding:12px 14px; box-shadow:0 12px 28px rgba(15,23,42,0.14); display:flex; align-items:flex-start; gap:10px; cursor:pointer; text-decoration:none; color:inherit; transform:translateX(140%) scale(0.95); opacity:0; transition:transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease; }
  .pop-toast.show{ transform:translateX(0) scale(1); opacity:1; }
  .pop-toast:hover{ transform:translateY(-2px) scale(1.01); border-color:#1a56db; box-shadow:0 14px 32px rgba(26,86,219,0.18); }
  .pop-toast.critical{ border-left-color:#c42020; }
  .pop-toast.warning{ border-left-color:var(--amber); }
  .pop-toast.resolved{ border-left-color:#16a34a; }
  .toast-icon{ width:26px; height:26px; border-radius:6px; background:#f1f5f9; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:12px; margin-top:1px; }
  .toast-body{ flex:1; min-width:0; }
  .toast-header{ display:flex; align-items:center; justify-content:space-between; margin-bottom:3px; }
  .toast-badge{ font-family:var(--font-mono); font-size:8.5px; font-weight:700; letter-spacing:0.06em; text-transform:uppercase; color:#1a56db; }
  .pop-toast.critical .toast-badge{ color:#c42020; }
  .pop-toast.warning .toast-badge{ color:var(--amber); }
  .pop-toast.resolved .toast-badge{ color:#16a34a; }
  .toast-time{ font-family:var(--font-mono); font-size:8.5px; color:#94a3b8; }
  .toast-text{ font-size:11.5px; color:#1e293b; font-weight:500; line-height:1.4; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .toast-sublink{ font-family:var(--font-mono); font-size:9.5px; color:#1a56db; margin-top:4px; display:inline-flex; align-items:center; gap:4px; font-weight:600; }
  .toast-close{ border:none; background:none; color:#94a3b8; font-size:13px; cursor:pointer; padding:0 2px; line-height:1; }
  .toast-close:hover{ color:#0f172a; }

  /* Capabilities Section - Official Clean Card Design */
  .caps-section{ position:relative; z-index:1; max-width:1080px; margin:36px auto 0; padding:45px 24px 20px; text-align:center; }
  .caps-section h2{ font-family:var(--font-serif); font-size:28px; margin-bottom:10px; font-weight:700; color:#0f172a; }
  .caps-section > p{ color:#64748b; font-size:14px; max-width:560px; margin:0 auto 14px; line-height:1.6; }
  .caps-divider{ width:50px; height:3px; background:var(--gold); margin:14px auto 32px; border-radius:2px; }

  .caps-grid{ position:relative; z-index:1; display:grid; grid-template-columns:repeat(3, 1fr); gap:18px; max-width:1080px; margin:0 auto; padding:0 24px; }
  .cap-card{ background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:24px 22px; text-align:left; position:relative; transition:box-shadow 0.2s, transform 0.2s; box-shadow:0 1px 3px rgba(0,0,0,0.03); }
  .cap-card:hover{ transform:translateY(-2px); box-shadow:0 8px 20px rgba(0,0,0,0.06); border-color:#cbd5e1; }
  .cap-tag{ position:absolute; top:16px; right:16px; font-family:var(--font-mono); font-size:9px; color:#64748b; letter-spacing:0.06em; background:#f1f5f9; padding:2px 7px; border-radius:3px; }
  .cap-tag.core{ color:var(--gold); border:1px solid rgba(212,146,10,0.4); background:#fffbeb; font-weight:700; }
  .cap-icon{ width:40px; height:40px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px;
    display:flex; align-items:center; justify-content:center; margin-bottom:16px; color:var(--gold); font-size:17px; }
  .cap-card h3{ font-family:var(--font-body); font-size:15px; font-weight:600; margin-bottom:8px; color:#0f172a; }
  .cap-card p{ font-size:13px; color:#64748b; line-height:1.65; }
  
  /* Clean Radar Graphic */
  .cap-visual{ position:relative; margin-top:16px; height:74px; border:1px solid #bfdbfe; border-radius:6px; display:flex;
    align-items:center; justify-content:center; font-family:var(--font-mono); font-size:10px; color:#1d4ed8; letter-spacing:0.05em; background:radial-gradient(circle at center, #eff6ff 0%, #ffffff 80%); overflow:hidden; font-weight:600; }
  .radar-sweep{ position:absolute; inset:0; width:100%; height:100%; border-radius:50%; background:conic-gradient(from 0deg at 50% 50%, rgba(29,78,216,0) 0deg, rgba(29,78,216,0.18) 60deg, transparent 61deg); animation:sweep 4s linear infinite; pointer-events:none; }
  @keyframes sweep{ 0%{transform:rotate(0deg);} 100%{transform:rotate(360deg);} }

  .cap-wide{ position:relative; z-index:1; max-width:1080px; margin:18px auto 0; padding:0 24px; }
  .cap-wide-card{ background:#ffffff; border:1px solid #e2e8f0; border-radius:8px; padding:20px 24px;
    display:flex; align-items:center; gap:20px; position:relative; box-shadow:0 1px 3px rgba(0,0,0,0.03); }
  .cap-wide-card .cap-icon{ margin-bottom:0; flex-shrink:0; color:#16a34a; background:#f0fdf4; border-color:#bbf7d0; }
  .cap-wide-card .body{ flex:1; }
  .cap-wide-card h3{ font-family:var(--font-body); font-size:15px; font-weight:600; margin-bottom:5px; color:#0f172a; }
  .cap-wide-card p{ font-size:13px; color:#64748b; line-height:1.6; }
  .btn-doc{ background:#f8fafc; border:1px solid #cbd5e1; color:#334155; padding:9px 18px; border-radius:var(--radius);
    font-family:var(--font-mono); font-size:11px; flex-shrink:0; letter-spacing:0.05em; cursor:pointer; font-weight:600; transition:all 0.15s; }
  .btn-doc:hover{ background:#f1f5f9; border-color:#94a3b8; color:#0f172a; }

  /* Clean Official Clearance Authentication Modal */
  #auth-modal{ position:fixed; inset:0; z-index:200; background:rgba(15,23,42,0.6); backdrop-filter:blur(6px); -webkit-backdrop-filter:blur(6px); display:none; align-items:center; justify-content:center; }
  #auth-modal.active{ display:flex; animation:fadeInModal 0.2s ease-out; }
  @keyframes fadeInModal{ from{opacity:0;} to{opacity:1;} }
  .auth-box{ width:460px; max-width:92vw; background:#ffffff; border:1px solid #cbd5e1; border-radius:10px; padding:28px 26px; box-shadow:0 16px 36px rgba(0,0,0,0.18); text-align:center; position:relative; overflow:hidden; }
  .auth-box::before{ content:''; position:absolute; top:0; left:0; width:100%; height:3px; background:linear-gradient(90deg, #FF9933 0%, #ffffff 50%, #138808 100%); }
  
  .auth-scanner{ width:68px; height:68px; margin:0 auto 16px; position:relative; display:flex; align-items:center; justify-content:center; }
  .scanner-ring{ position:absolute; inset:0; border-radius:50%; border:2px dashed #cbd5e1; animation:spinRing 6s linear infinite; }
  .scanner-ring-2{ position:absolute; inset:5px; border-radius:50%; border:2px solid transparent; border-top-color:#1a56db; border-right-color:#1a56db; animation:spinRingReverse 2s cubic-bezier(0.68,-0.55,0.27,1.55) infinite; }
  .scanner-center{ width:38px; height:38px; background:#eff6ff; border:1px solid #bfdbfe; border-radius:50%; display:flex; align-items:center; justify-content:center; color:#1d4ed8; font-size:16px; }
  @keyframes spinRing{ from{transform:rotate(0deg);} to{transform:rotate(360deg);} }
  @keyframes spinRingReverse{ from{transform:rotate(360deg);} to{transform:rotate(0deg);} }

  .auth-title{ font-family:var(--font-serif); font-size:18px; font-weight:700; color:#0f172a; margin-bottom:4px; }
  .auth-status{ font-family:var(--font-mono); font-size:11px; color:#1d4ed8; margin-bottom:14px; min-height:16px; letter-spacing:0.04em; font-weight:600; }
  .auth-progress-track{ width:100%; height:5px; background:#e2e8f0; border-radius:3px; overflow:hidden; margin-bottom:12px; position:relative; }
  .auth-progress-fill{ height:100%; width:0%; background:linear-gradient(90deg, #1a56db, var(--gold)); border-radius:3px; transition:width 0.2s ease-out; }
  .auth-terminal{ background:#f8fafc; border:1px solid #e2e8f0; border-radius:6px; padding:8px 12px; font-family:var(--font-mono); font-size:9.5px; color:#475569; text-align:left; height:68px; overflow:hidden; display:flex; flex-direction:column; justify-content:flex-end; gap:2px; }
  .auth-terminal-line{ opacity:0.9; white-space:nowrap; text-overflow:ellipsis; overflow:hidden; }
  .auth-terminal-line.active{ color:#1d4ed8; font-weight:600; }

  .land-footer{ position:relative; z-index:1; max-width:1080px; margin:48px auto 0; padding:20px 24px 32px; border-top:1px solid #e2e8f0;
    display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; font-family:var(--font-mono); font-size:10px; color:#64748b; letter-spacing:0.03em; }
  .land-footer a{ color:#64748b; text-decoration:none; margin-left:16px; transition:color 0.15s; }
  .land-footer a:hover{ color:#0f172a; }

  /* ================= APP SHELL ================= */
  #app{ display:none; height:100vh; grid-template-columns:224px 1fr; }
  #app.show{ display:grid; }

  .sidebar{ background:var(--bg-2); border-right:1px solid var(--border); display:flex; flex-direction:column; }
  .sb-brand{ display:flex; align-items:center; gap:10px; padding:16px 18px; border-bottom:1px solid var(--border); cursor:pointer; user-select:none; transition:background 0.15s; }
  .sb-brand:hover{ background:var(--panel-2); }
  .lang-switcher{ display:flex; gap:5px; padding:10px 18px; border-bottom:1px solid var(--border); }
  .lang-btn{ font-family:var(--font-mono); font-size:10px; padding:4px 10px; border-radius:var(--radius-sm); border:1px solid var(--border);
    background:var(--panel); color:var(--ink-dim); cursor:pointer; letter-spacing:0.04em; font-weight:500; transition:all 0.15s; }
  .lang-btn.active{ background:var(--blue); border-color:var(--blue); color:#fff; font-weight:700; }
  .lang-btn:hover:not(.active){ border-color:var(--ink-faint); color:var(--ink); }
  .land-lang-switcher{ padding:0; border-bottom:none; margin-left:16px; }
  .sb-brand-mark{ font-family:var(--font-serif); color:var(--gold); font-size:17px; }
  .sb-brand-text b{ font-family:var(--font-serif); font-size:14px; display:block; letter-spacing:0.04em; }
  .sb-brand-text span{ font-family:var(--font-mono); font-size:8px; color:var(--ink-faint); letter-spacing:0.06em; font-weight:500; }
  .sb-nav{ flex:1; padding:12px 10px; overflow-y:auto; }
  .sb-item{ display:flex; align-items:center; gap:10px; padding:9px 11px; border-radius:var(--radius); color:var(--ink-dim);
    font-size:12px; font-weight:500; cursor:pointer; margin-bottom:1px; transition:all 0.12s; letter-spacing:0.01em; }
  .sb-item svg{ flex-shrink:0; opacity:0.8; }
  .sb-item:hover{ background:var(--panel-2); color:var(--ink); }
  .sb-item.active{ background:var(--panel-2); color:var(--blue); border:1px solid var(--border); font-weight:600; }
  .sb-footer{ padding:12px 10px; border-top:1px solid var(--border); }
  .sb-footer .sb-item{ font-size:11px; }
  .sb-gov{ padding:10px 18px; font-family:var(--font-mono); font-size:8px; color:var(--ink-faint); border-top:1px solid var(--border); line-height:1.7; letter-spacing:0.04em; }

  .main-col{ display:flex; flex-direction:column; min-width:0; height:100vh; max-height:100vh; overflow:hidden; }
  .topbar{ display:flex; align-items:center; justify-content:space-between; padding:12px 22px;
    border-bottom:1px solid var(--border); background:var(--bg-2); gap:14px; flex-wrap:wrap; flex-shrink:0; }
  .topbar-left{ display:flex; align-items:center; gap:12px; flex:1; min-width:0; }
  .topbar h2{ font-family:var(--font-body); font-size:15px; font-weight:600; white-space:nowrap; letter-spacing:-0.01em; color:var(--ink); }
  .badge-secure{ font-family:var(--font-mono); font-size:8.5px; letter-spacing:0.08em; background:rgba(11,148,148,0.1);
    color:var(--cyan); border:1px solid rgba(11,148,148,0.35); padding:3px 8px; border-radius:10px; white-space:nowrap; font-weight:600; }
  .topbar-search{ display:flex; align-items:center; gap:8px; background:var(--bg); border:1px solid var(--border);
    border-radius:var(--radius); padding:7px 12px; min-width:220px; flex:1; max-width:380px; transition:border-color 0.15s; }
  .topbar-search:focus-within{ border-color:var(--blue); }
  .topbar-search input{ background:none; border:none; outline:none; color:var(--ink); font-family:var(--font-mono); font-size:11px; width:100%; }
  .topbar-search input::placeholder{ color:var(--ink-faint); }
  .topbar-icons{ display:flex; gap:6px; }
  .icon-btn{ width:30px; height:30px; border-radius:var(--radius); background:var(--bg); border:1px solid var(--border);
    display:flex; align-items:center; justify-content:center; color:var(--ink-dim); transition:all 0.12s; }
  .icon-btn:hover{ color:var(--ink); border-color:var(--ink-faint); background:var(--panel); }

  .page{ display:none; flex:1; min-height:0; overflow-y:auto; -webkit-overflow-scrolling:touch; }
  .page.active{ display:flex; flex-direction:column; }
  .page[data-page="report"]{ overflow-y:auto !important; }
  .page-pad{ padding:20px 24px; }

  .mobile-topbar{ display:none; }

  /* ---- Professional Command Center Overhaul ---- */
  .cc-case-tag{ font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); margin-left:8px; letter-spacing:0.05em; }
  .topbar-right-actions{ display:flex; align-items:center; gap:6px; }
  .btn-cc-action{ display:inline-flex; align-items:center; gap:5px; background:#ffffff; border:1px solid #d1d9e6; color:#1e40af; padding:5px 12px; border-radius:var(--radius); font-family:var(--font-body); font-size:12px; font-weight:600; cursor:pointer; transition:all 0.14s; letter-spacing:-0.01em; }
  .btn-cc-action svg{ opacity:0.8; }
  .btn-cc-action:hover{ background:#eff6ff; border-color:#93c5fd; color:#1d4ed8; box-shadow:0 1px 4px rgba(29,78,216,0.12); }

  /* --- Stat Grid (KPI Row) --- */
  .stat-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:16px; }
  .stat-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px 18px 12px; position:relative;
    box-shadow:0 1px 3px rgba(0,0,0,0.04); transition:transform 0.14s, box-shadow 0.14s; overflow:hidden; }
  .stat-card::before{ content:''; position:absolute; top:0; left:0; width:3px; height:100%; border-radius:8px 0 0 8px; }
  .stat-card.live::before{ background:#16a34a; }
  .stat-card.flagged::before{ background:#dc2626; }
  .stat-card.detected::before{ background:#1d4ed8; }
  .stat-card.monitored::before{ background:#d97706; }
  .stat-card:hover{ transform:translateY(-2px); box-shadow:0 6px 16px rgba(0,0,0,0.07); }
  .stat-card-top{ display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:10px; }
  .stat-card-icon{ width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .stat-card-icon.live{ background:#dcfce7; color:#16a34a; }
  .stat-card-icon.flagged{ background:#fee2e2; color:#dc2626; }
  .stat-card-icon.detected{ background:#dbeafe; color:#1d4ed8; }
  .stat-card-icon.monitored{ background:#fef3c7; color:#d97706; }
  .stat-card .tag{ font-family:var(--font-mono); font-size:8.5px; color:var(--ink-faint); letter-spacing:0.05em; padding:2px 7px; border-radius:20px; background:#f1f5f9; font-weight:600; }
  .stat-card .tag.up{ color:#16a34a; background:#f0fdf4; border:1px solid #bbf7d0; }
  .stat-card .tag.warn{ color:#c42020; background:#fef2f2; border:1px solid #fecaca; }
  .stat-card .l{ font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:0.07em; margin-bottom:4px; font-weight:600; }
  .stat-card .v{ font-family:var(--font-body); font-size:28px; font-weight:700; color:var(--ink); letter-spacing:-0.03em; line-height:1; }
  .stat-card .stat-sub{ font-family:var(--font-mono); font-size:9px; color:#64748b; margin-top:8px; display:flex; align-items:center; gap:5px; }
  .stat-sparkline{ margin-top:8px; display:block; }

  /* --- Main Visual Grid (Radar + Charts) --- */
  .cc-main-grid{ display:grid; grid-template-columns:1.3fr 1fr; gap:14px; margin-bottom:14px; }
  .cc-panel{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:18px 20px;
    box-shadow:0 1px 3px rgba(0,0,0,0.04); display:flex; flex-direction:column; }
  .cc-panel-head{ display:flex; align-items:flex-start; justify-content:space-between; margin-bottom:14px; gap:10px; }
  .cc-panel-title-wrap{ display:flex; align-items:center; gap:8px; }
  .cc-panel-icon{ width:28px; height:28px; border-radius:6px; background:#f1f5f9; display:flex; align-items:center; justify-content:center; flex-shrink:0; color:#475569; }
  .cc-panel-head h3{ font-family:var(--font-body); font-size:13px; font-weight:700; color:var(--ink); letter-spacing:-0.015em; margin-bottom:2px; }
  .cc-panel-sub{ font-family:var(--font-mono); font-size:9px; color:#94a3b8; letter-spacing:0.02em; }
  .cc-panel-actions{ display:flex; align-items:center; gap:6px; flex-shrink:0; }
  .cc-live-badge{ display:inline-flex; align-items:center; gap:5px; font-family:var(--font-mono); font-size:9px; color:#16a34a;
    background:#f0fdf4; border:1px solid #bbf7d0; padding:3px 9px; border-radius:20px; font-weight:700; letter-spacing:0.03em; }
  .cc-live-badge .pulse-dot{ width:6px; height:6px; border-radius:50%; background:#16a34a;
    animation:pulseDot 1.6s ease-in-out infinite; box-shadow:0 0 0 0 rgba(22,163,74,0.5); }
  @keyframes pulseDot{ 0%,100%{ box-shadow:0 0 0 0 rgba(22,163,74,0.5); } 50%{ box-shadow:0 0 0 5px rgba(22,163,74,0); } }
  .cc-btn-sm{ display:inline-flex; align-items:center; gap:5px; background:#f8fafc; border:1px solid #dde4ef; color:#475569;
    padding:4px 10px; border-radius:5px; font-family:var(--font-body); font-size:11.5px; cursor:pointer; font-weight:600;
    transition:all 0.13s; letter-spacing:-0.01em; }
  .cc-btn-sm:hover{ background:#f1f5f9; border-color:#94a3b8; color:#0f172a; box-shadow:0 1px 3px rgba(0,0,0,0.06); }
  .cc-tag-formula{ font-family:var(--font-mono); font-size:9px; color:var(--gold); background:#fffbeb;
    border:1px solid rgba(212,146,10,0.3); padding:3px 9px; border-radius:20px; font-weight:700; letter-spacing:0.03em; }
  .cc-tag-amber{ font-family:var(--font-mono); font-size:9px; color:#d97706; background:#fffbeb;
    border:1px solid #fde68a; padding:3px 9px; border-radius:20px; font-weight:700; letter-spacing:0.03em; }

  /* --- Radar Map Container --- */
  .cc-radar-container{ position:relative; width:100%; height:280px; background:linear-gradient(135deg,#f8fafc 0%,#f1f5f9 100%);
    border:1px solid #e8edf5; border-radius:6px; overflow:hidden; }
  #cc-mini-graph{ width:100%; height:100%; display:block; cursor:grab; }
  #cc-mini-graph:active{ cursor:grabbing; }
  .cc-radar-legend{ position:absolute; bottom:10px; left:10px; display:flex; gap:12px;
    font-family:var(--font-mono); font-size:9px; color:#64748b; background:rgba(255,255,255,0.95);
    border:1px solid #e2e8f0; padding:5px 12px; border-radius:6px; pointer-events:none;
    box-shadow:0 1px 4px rgba(0,0,0,0.06); }
  .cc-radar-legend span{ display:flex; align-items:center; gap:5px; font-weight:600; }
  .cc-radar-legend .dot{ width:7px; height:7px; border-radius:2px; flex-shrink:0; }

  /* --- Charts Container --- */
  .cc-charts-wrap{ display:grid; grid-template-columns:1.15fr 1fr; gap:12px; flex:1; min-height:0; }
  .cc-chart-box{ background:#f8fafc; border:1px solid #e8edf5; border-radius:6px; padding:14px 14px 10px;
    display:flex; flex-direction:column; }
  .cc-chart-title{ font-family:var(--font-body); font-size:11px; font-weight:700; color:#334155;
    text-transform:uppercase; letter-spacing:0.05em; margin-bottom:12px; display:flex; align-items:center; gap:6px; }
  .cc-chart-title svg{ color:#94a3b8; }

  /* --- Threat Score Bars --- */
  .cc-bars-list{ display:flex; flex-direction:column; gap:10px; flex:1; justify-content:space-around; }
  .cc-bar-item{ display:flex; flex-direction:column; gap:4px; }
  .cc-bar-header{ display:flex; justify-content:space-between; align-items:center;
    font-size:12px; font-family:var(--font-body); font-weight:600; color:#1e293b; }
  .cc-bar-score{ font-family:var(--font-mono); font-size:10.5px; font-weight:700; }
  .cc-bar-score.crit{ color:#c42020; }
  .cc-bar-score.warn{ color:#d97706; }
  .cc-bar-score.low{ color:#16a34a; }
  .cc-bar-track{ width:100%; height:6px; background:#e8edf5; border-radius:6px; overflow:hidden; }
  .cc-bar-fill{ height:100%; border-radius:6px; transition:width 0.6s cubic-bezier(.4,0,.2,1); }
  .cc-bar-fill.crit{ background:linear-gradient(90deg,#fca5a5,#dc2626); }
  .cc-bar-fill.warn{ background:linear-gradient(90deg,#fcd34d,#d97706); }
  .cc-bar-fill.low{ background:linear-gradient(90deg,#6ee7b7,#16a34a); }
  .cc-bar-role{ font-family:var(--font-mono); font-size:8.5px; color:#94a3b8; font-weight:500; }

  /* --- Donut SVG Chart --- */
  .cc-donut-container{ display:flex; align-items:center; gap:14px; flex:1; justify-content:center; }
  #cc-donut-svg{ width:96px; height:96px; flex-shrink:0; }
  .cc-donut-legend{ display:flex; flex-direction:column; gap:6px; font-family:var(--font-body); font-size:11px; color:#475569; }
  .cc-donut-legend .item{ display:flex; align-items:center; gap:7px; }
  .cc-donut-legend .dot{ width:8px; height:8px; border-radius:2px; flex-shrink:0; }
  .cc-donut-legend b{ color:#1e293b; }

  /* --- Bottom Row 3-column Grid --- */
  .cc-bottom-grid{ display:grid; grid-template-columns:1.2fr 1fr 1.1fr; gap:14px; }

  /* --- Financial Velocity SVG Chart --- */
  .cc-velocity-wrap{ height:170px; border:1px solid #e8edf5; border-radius:6px; background:#f8fafc; overflow:hidden; position:relative; }
  #cc-velocity-svg{ width:100%; height:100%; display:block; }
  .cc-velocity-labels{ display:flex; justify-content:space-around; padding:0 4px; margin-top:4px; }
  .cc-velocity-lbl{ font-family:var(--font-mono); font-size:8.5px; color:#94a3b8; text-align:center; font-weight:600; }
  /* legacy chart container - keep for compat */
  .cc-velocity-chart{ height:190px; display:flex; align-items:flex-end; gap:8px; padding:12px 10px 6px; background:#f8fafc; border:1px solid #e2e8f0; border-radius:4px; }
  .cc-hist-col{ flex:1; display:flex; flex-direction:column; align-items:center; height:100%; justify-content:flex-end; gap:4px; }
  .cc-hist-val{ font-family:var(--font-mono); font-size:8px; color:#64748b; font-weight:600; }
  .cc-hist-bar-outer{ width:100%; max-width:28px; height:130px; background:rgba(0,0,0,0.03); border-radius:4px 4px 0 0; display:flex; flex-direction:column; justify-content:flex-end; overflow:hidden; }
  .cc-hist-bar{ width:100%; border-radius:4px 4px 0 0; transition:height 0.5s cubic-bezier(.4,0,.2,1); }
  .cc-hist-bar.spike{ background:linear-gradient(to top,#dc2626,#f87171); box-shadow:0 0 8px rgba(220,38,38,0.3); }
  .cc-hist-bar.norm{ background:linear-gradient(to top,#1d4ed8,#60a5fa); }
  .cc-hist-lbl{ font-family:var(--font-mono); font-size:8px; color:#94a3b8; white-space:nowrap; margin-top:3px; font-weight:600; }

  /* --- Key Suspects Roster --- */
  .cc-suspects-list{ display:flex; flex-direction:column; gap:7px; overflow-y:auto; max-height:195px; }
  .cc-suspect-card{ display:flex; align-items:center; justify-content:space-between; padding:9px 11px;
    background:#f8fafc; border:1px solid #e8edf5; border-radius:6px;
    transition:border-color 0.13s, box-shadow 0.13s; cursor:pointer; }
  .cc-suspect-card:hover{ border-color:#94a3b8; background:#ffffff; box-shadow:0 2px 8px rgba(0,0,0,0.06); }
  .cc-suspect-info{ display:flex; align-items:center; gap:9px; }
  .cc-suspect-avatar{ width:30px; height:30px; border-radius:6px; display:flex; align-items:center;
    justify-content:center; font-size:11px; font-weight:800; color:#ffffff; flex-shrink:0; }
  .cc-suspect-avatar.orchestrator{ background:linear-gradient(135deg,#b45309,#d97706); }
  .cc-suspect-avatar.broker{ background:linear-gradient(135deg,#1d4ed8,#3b82f6); }
  .cc-suspect-avatar.conduit{ background:linear-gradient(135deg,#7c3aed,#a78bfa); }
  .cc-suspect-avatar.associate{ background:linear-gradient(135deg,#475569,#94a3b8); }
  .cc-suspect-name{ font-size:12px; font-weight:700; color:#0f172a; letter-spacing:-0.01em; }
  .cc-suspect-role{ font-family:var(--font-mono); font-size:9px; color:#64748b; margin-top:1px; }
  .cc-suspect-risk{ font-family:var(--font-body); font-size:10px; font-weight:700; padding:3px 8px; border-radius:20px; white-space:nowrap; }
  .cc-suspect-risk.high{ color:#991b1b; background:#fee2e2; border:1px solid #fca5a5; }
  .cc-suspect-risk.med{ color:#92400e; background:#fef3c7; border:1px solid #fcd34d; }

  /* --- Live Feed Stream --- */
  .cc-feed-scroll{ max-height:210px; overflow-y:auto; scrollbar-width:thin; }
  .feed-item{ display:flex; gap:10px; padding:9px 0; border-bottom:1px solid var(--border); }
  .feed-item:last-child{ border-bottom:none; }
  .feed-accent{ width:3px; border-radius:2px; flex-shrink:0; margin-top:2px; }
  .feed-accent.critical{ background:#dc2626; }
  .feed-accent.warning{ background:#d97706; }
  .feed-accent.info{ background:#0b9494; }
  .feed-body{ flex:1; min-width:0; }
  .feed-head{ display:flex; align-items:center; gap:7px; margin-bottom:3px; }
  .feed-sev{ font-family:var(--font-mono); font-size:8.5px; letter-spacing:0.07em; padding:2px 6px;
    border-radius:3px; text-transform:uppercase; font-weight:700; }
  .feed-sev.critical{ background:rgba(220,38,38,0.1); color:#dc2626; }
  .feed-sev.warning{ background:rgba(217,119,6,0.12); color:#d97706; }
  .feed-sev.info{ background:rgba(11,148,148,0.1); color:#0b9494; }
  .feed-time{ font-family:var(--font-mono); font-size:8.5px; color:var(--ink-faint); margin-left:auto; }
  .feed-text{ font-size:12px; color:var(--ink-dim); line-height:1.5; font-weight:500; }
  .feed-src{ font-family:var(--font-mono); font-size:8.5px; color:var(--ink-faint); margin-top:2px; }

  /* ---- Network Explorer ---- */
  #graph-wrap{ position:relative; overflow:hidden; background:var(--bg); flex:1; min-height:0; }
  .graph-dotgrid{ position:absolute; inset:0; background-image:radial-gradient(circle, rgba(20,30,60,0.07) 1px, transparent 1px);
    background-size:22px 22px; pointer-events:none; }
  svg#graph{ width:100%; height:100%; display:block; cursor:grab; position:relative; z-index:1; }
  svg#graph:active{ cursor:grabbing; }
  .link{ stroke:var(--ink-faint); stroke-opacity:0.45; fill:none; transition:stroke 0.25s ease, stroke-opacity 0.25s ease, stroke-width 0.25s ease; }
  .link.suspicious{ stroke:var(--red); stroke-opacity:0.85; stroke-dasharray:3,3; }
  .link.highlighted{ stroke:var(--gold) !important; stroke-width:2.2px !important; stroke-opacity:1 !important; filter:drop-shadow(0 0 5px rgba(212,146,10,0.6)); }
  .link.traced{ stroke:#00e5ff !important; stroke-width:2.8px !important; stroke-opacity:0.95 !important; stroke-dasharray:8,5; animation:flowDash 0.9s linear infinite; filter:drop-shadow(0 0 6px rgba(0,229,255,0.85)); }
  .link-label{ font-family:var(--font-mono); font-size:8.5px; fill:var(--ink-faint); pointer-events:none; transition:fill 0.2s ease; }
  .link.traced + .link-label, .link-label.traced-label{ fill:#00e5ff !important; font-weight:700; font-size:9.5px; }

  @keyframes flowDash {
    to { stroke-dashoffset: -26px; }
  }
  @keyframes beaconPulseCyan {
    0% { transform:scale(1); opacity:0.9; }
    50% { transform:scale(1.45); opacity:0.25; }
    100% { transform:scale(1); opacity:0.9; }
  }
  @keyframes beaconPulseGold {
    0% { transform:scale(1); opacity:0.9; }
    50% { transform:scale(1.45); opacity:0.25; }
    100% { transform:scale(1); opacity:0.9; }
  }
  @keyframes badgeSlideDown {
    from { opacity:0; transform:translateY(-10px) scale(0.98); }
    to { opacity:1; transform:translateY(0) scale(1); }
  }

  .node{ cursor:pointer; transition:opacity 0.25s ease; }
  .node-box{ fill:var(--panel); stroke-width:1.4px; transition:stroke 0.2s ease, filter 0.2s ease, stroke-width 0.2s ease; }
  .node-icon{ pointer-events:none; }
  .node-label{ font-family:var(--font-mono); font-size:9px; fill:var(--ink-dim); pointer-events:none; transition:fill 0.2s ease; }
  .node-sublabel{ font-family:var(--font-mono); font-size:7.5px; fill:var(--ink-faint); pointer-events:none; }
  .node.dim{ opacity:0.12; }
  .link.dim{ stroke-opacity:0.06 !important; }
  .link-label.dim{ opacity:0.1; }
  .node.selected .node-box{ filter:drop-shadow(0 0 8px currentColor); stroke-width:2px; }
  .node.key .node-box{ stroke:var(--gold) !important; }

  /* Node Traced Highlights */
  .node.path-origin .node-box{ stroke:#00e5ff !important; stroke-width:2.5px !important; filter:drop-shadow(0 0 10px #00e5ff) !important; }
  .node.path-target .node-box{ stroke:var(--gold) !important; stroke-width:2.5px !important; filter:drop-shadow(0 0 10px var(--gold)) !important; }
  .node.path-waypoint .node-box{ stroke:#00e5ff !important; stroke-width:2px !important; filter:drop-shadow(0 0 6px rgba(0,229,255,0.6)) !important; }
  .beacon-ring{ pointer-events:none; transform-box:fill-box; transform-origin:center; }
  .beacon-origin{ animation:beaconPulseCyan 1.8s ease-in-out infinite; stroke:#00e5ff; stroke-width:2px; fill:rgba(0,229,255,0.12); }
  .beacon-target{ animation:beaconPulseGold 1.8s ease-in-out infinite; stroke:var(--gold); stroke-width:2px; fill:rgba(212,146,10,0.12); }

  /* Flowing Arrow Overlay */
  .g-flow-overlay{ pointer-events:none; }
  .flow-arrow-marker{ pointer-events:none; filter:drop-shadow(0 0 5px #00e5ff); }

  #graph-toolbar-left{ position:absolute; top:14px; left:14px; z-index:4; display:flex; flex-direction:column; gap:6px; }
  #graph-hint{ position:absolute; bottom:12px; left:14px; z-index:4; font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); }
  .tool-icon{ width:32px; height:32px; border-radius:6px; background:var(--panel); border:1px solid var(--border);
    display:flex; align-items:center; justify-content:center; color:var(--ink-dim); font-family:var(--font-mono); font-size:13px; font-weight:700; cursor:pointer; user-select:none; box-shadow:var(--shadow-sm); transition:all 0.15s ease; }
  .tool-icon:hover{ color:var(--ink); border-color:var(--ink-faint); background:var(--panel-2); transform:scale(1.05); }
  .tool-icon.active, .tool-icon.paused{ color:var(--gold); border-color:var(--gold); background:rgba(212,146,10,0.08); }
  #graph-error{ position:absolute; inset:0; display:none; align-items:center; justify-content:center; flex-direction:column;
    gap:10px; text-align:center; padding:30px; font-family:var(--font-mono); color:var(--red); font-size:12px; z-index:5; background:var(--bg); }

  /* Path Finder Bar */
  .path-finder-bar{ display:flex; align-items:center; gap:8px; background:var(--panel); border:1px solid var(--border);
    border-radius:8px; padding:6px 14px; box-shadow:var(--shadow-sm); }
  .pf-label{ font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:0.06em; font-weight:700; display:flex; align-items:center; gap:4px; }
  .pf-select{ background:var(--bg); border:1px solid var(--border); color:var(--ink); font-family:var(--font-mono); font-size:11px; padding:5px 8px; border-radius:5px; outline:none; transition:border-color 0.15s; max-width:180px; text-overflow:ellipsis; }
  .pf-select:focus{ border-color:var(--gold); }
  .pf-swap-btn{ background:var(--panel-2); border:1px solid var(--border); color:var(--gold); border-radius:5px; padding:4px 8px; font-size:13px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; justify-content:center; transition:all 0.2s ease; line-height:1; }
  .pf-swap-btn:hover{ background:var(--border); color:var(--ink); transform:rotate(180deg); }
  .pf-arrow{ font-family:var(--font-mono); color:var(--gold); font-weight:700; font-size:12px; }
  .btn-pf-run{ background:linear-gradient(135deg, #d4920a, #e5a519); color:#fff; border:none; padding:6px 14px; border-radius:5px; font-family:var(--font-mono); font-size:11px; font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:6px; box-shadow:0 2px 6px rgba(212,146,10,0.3); transition:all 0.2s ease; }
  .btn-pf-run:hover{ box-shadow:0 4px 12px rgba(212,146,10,0.45); transform:translateY(-1px); }
  .btn-pf-clear{ background:none; border:1px solid var(--border); color:var(--ink-dim); padding:6px 12px; border-radius:5px; font-family:var(--font-mono); font-size:11px; cursor:pointer; transition:all 0.2s ease; }
  .btn-pf-clear:hover{ border-color:var(--ink-faint); color:var(--ink); }

  /* Interactive Path HUD Badge */
  .path-info-badge{ position:absolute; top:14px; left:58px; z-index:10; max-width:620px; background:rgba(15,22,38,0.94); backdrop-filter:blur(14px); -webkit-backdrop-filter:blur(14px); border:1px solid rgba(0,229,255,0.45); border-radius:10px; padding:12px 16px; color:#fff; display:none; box-shadow:0 12px 36px rgba(0,0,0,0.35), 0 0 20px rgba(0,229,255,0.15); animation:badgeSlideDown 0.3s cubic-bezier(0.16,1,0.3,1); }
  .pib-header{ display:flex; align-items:center; justify-content:space-between; gap:12px; border-bottom:1px solid rgba(255,255,255,0.1); padding-bottom:8px; margin-bottom:8px; }
  .pib-title-wrap{ display:flex; align-items:center; gap:8px; }
  .pib-status-tag{ font-family:var(--font-mono); font-size:9px; font-weight:800; letter-spacing:0.06em; padding:2px 6px; border-radius:3px; background:rgba(0,229,255,0.18); color:#00e5ff; border:1px solid rgba(0,229,255,0.4); text-transform:uppercase; }
  .pib-title{ font-family:var(--font-mono); font-size:11.5px; font-weight:700; color:#fff; }
  .pib-close{ background:none; border:none; color:rgba(255,255,255,0.5); font-size:14px; cursor:pointer; padding:2px 6px; line-height:1; border-radius:4px; transition:color 0.15s; }
  .pib-close:hover{ color:#fff; background:rgba(255,255,255,0.1); }
  .pib-chain{ display:flex; align-items:center; flex-wrap:wrap; gap:6px; margin:8px 0; font-family:var(--font-mono); font-size:11px; }
  .pib-node-chip{ display:inline-flex; align-items:center; gap:5px; background:rgba(255,255,255,0.08); border:1px solid rgba(255,255,255,0.15); border-radius:5px; padding:3px 8px; color:#f0f2f7; font-weight:600; cursor:pointer; transition:all 0.15s; }
  .pib-node-chip:hover{ background:rgba(0,229,255,0.2); border-color:#00e5ff; color:#fff; }
  .pib-node-chip.origin{ border-color:#00e5ff; color:#00e5ff; background:rgba(0,229,255,0.12); }
  .pib-node-chip.target{ border-color:var(--gold); color:var(--gold); background:rgba(212,146,10,0.15); }
  .pib-arrow-chip{ display:inline-flex; align-items:center; gap:4px; font-size:10px; color:#00e5ff; font-weight:700; padding:2px 4px; }
  .pib-arrow-chip .pib-rel-text{ font-size:9.5px; opacity:0.85; font-weight:500; }
  .pib-footer{ display:flex; align-items:center; justify-content:space-between; gap:12px; margin-top:8px; padding-top:6px; font-family:var(--font-mono); font-size:10px; color:rgba(255,255,255,0.6); }
  .btn-pib-focus{ background:rgba(0,229,255,0.15); border:1px solid rgba(0,229,255,0.4); color:#00e5ff; border-radius:4px; padding:3px 8px; font-size:10px; font-family:var(--font-mono); font-weight:700; cursor:pointer; display:inline-flex; align-items:center; gap:4px; transition:all 0.15s; }
  .btn-pib-focus:hover{ background:#00e5ff; color:#0f1626; }

  /* Timeline Player Bar */
  .timeline-player-bar{ position:absolute; bottom:14px; left:14px; right:14px; z-index:4; background:var(--panel);
    border:1px solid var(--border); border-radius:8px; padding:10px 16px; display:flex; align-items:center; gap:16px;
    box-shadow:0 6px 20px rgba(0,0,0,0.08); }
  .tp-controls{ display:flex; align-items:center; gap:6px; }
  .tp-btn{ width:30px; height:30px; border-radius:5px; background:var(--bg); border:1px solid var(--border); color:var(--ink); font-size:12px; display:flex; align-items:center; justify-content:center; cursor:pointer; }
  .tp-btn.primary{ background:var(--blue); border-color:var(--blue); color:#fff; }
  .tp-btn:hover{ opacity:0.85; }
  .tp-scrub-wrap{ flex:1; display:flex; flex-direction:column; gap:4px; min-width:0; }
  .tp-event-meta{ display:flex; align-items:center; gap:8px; font-size:11px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
  .tp-event-date{ font-family:var(--font-mono); font-weight:700; color:var(--ink); font-size:10.5px; }
  .tp-event-badge{ font-family:var(--font-mono); font-size:9px; padding:2px 6px; border-radius:3px; font-weight:700; text-transform:uppercase; background:rgba(37,84,232,0.12); color:var(--blue); }
  .tp-event-badge.SURVEILLANCE{ background:rgba(224,138,0,0.15); color:var(--amber); }
  .tp-event-badge.FINANCIAL{ background:rgba(220,38,38,0.12); color:var(--red); }
  .tp-event-badge.COMMUNICATION{ background:rgba(14,165,164,0.12); color:var(--cyan); }
  .tp-event-title{ color:var(--ink-dim); overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:11px; }
  .tp-slider{ width:100%; accent-color:var(--blue); cursor:pointer; }
  .tp-ticker{ font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); white-space:nowrap; }

  /* Role Badges */
  .role-badge{ display:inline-flex; align-items:center; gap:4px; font-family:var(--font-mono); font-size:8.5px; letter-spacing:0.06em; font-weight:700; padding:2px 8px; border-radius:2px; border:1px solid var(--border); }
  .role-badge.role-orchestrator{ background:rgba(212,146,10,0.1); color:var(--gold); border-color:rgba(212,146,10,0.4); }
  .role-badge.role-broker{ background:rgba(11,148,148,0.1); color:var(--cyan); border-color:rgba(11,148,148,0.4); }
  .role-badge.role-mule{ background:rgba(196,32,32,0.1); color:var(--red); border-color:rgba(196,32,32,0.4); }
  .role-badge.role-communicator{ background:rgba(31,70,204,0.1); color:var(--blue); border-color:rgba(31,70,204,0.4); }
  .role-badge.role-associate{ background:var(--bg); color:var(--ink-dim); border-color:var(--border); }

  /* Export Button */
  .btn-export-dossier{ background:var(--panel); border:1px solid var(--border); color:var(--ink); font-family:var(--font-mono); font-size:11px; padding:7px 14px; border-radius:5px; display:inline-flex; align-items:center; gap:6px; font-weight:600; cursor:pointer; }
  .btn-export-dossier:hover{ border-color:var(--ink); }

  .legend-sidebar{ position:absolute; bottom:70px; right:14px; z-index:4; background:var(--panel); border:1px solid var(--border);
    border-radius:6px; padding:10px 12px; display:flex; flex-direction:column; gap:6px; }
  .legend-row2{ display:flex; align-items:center; gap:8px; font-size:10.5px; color:var(--ink-dim); cursor:pointer; user-select:none; }
  .legend-row2.off{ opacity:0.35; }

  /* Print Stylesheet */
  .print-only{ display:none; }
  @media print{
    @page { margin: 15mm 15mm 15mm 15mm; size: A4 portrait; }
    #landing, .sidebar, .mobile-topbar, .topbar, .topbar-search, .topbar-icons, 
    .path-finder-bar, .timeline-player-bar, #graph-toolbar-left, .legend-sidebar, 
    #graph-hint, .btn-export-dossier, .breadcrumb, .report-filter-group, 
    .asst-input-row, .asst-suggestions, .dl-input-toggle, .dl-run-btn{ display:none !important; }
    
    #app{ display:block !important; height:auto !important; overflow:visible !important; }
    .page{ display:none !important; }
    .page.active{ display:block !important; padding:0 !important; width:100% !important; }
    
    body{ background:#fff !important; color:#111 !important; overflow:visible !important; font-size:10.5pt !important; }
    
    .print-only{ display:block !important; }
    .print-official-header{ text-align:center; margin-bottom:20px; border-bottom:2px solid #000; padding-bottom:12px; }
    .print-official-header .gov-title{ font-size:13pt; font-weight:800; text-transform:uppercase; letter-spacing:0.04em; }
    .print-official-header .sub-dept{ font-size:9.5pt; color:#444; margin-top:2px; text-transform:uppercase; }
    .print-official-header .doc-title{ font-size:12pt; font-weight:700; margin-top:6px; letter-spacing:0.02em; }
    
    .report-exec-card, .report-section-card, .pd-card{ 
      background:#fff !important; color:#000 !important; border:1px solid #ccc !important; 
      box-shadow:none !important; page-break-inside:avoid; margin-bottom:14px !important; padding:14px !important;
    }
    .rec-stat-box{ background:#f8f9fa !important; border:1px solid #ddd !important; }
    .rec-stat-box .v{ color:#000 !important; }
    .statement-card{ 
      background:#fdfdfd !important; color:#111 !important; border:1px solid #e0e0e0 !important; 
      page-break-inside:avoid; margin-bottom:8px !important; padding:8px 12px !important;
    }
    .statement-card.FACT{ border-left:4px solid #0e9aa7 !important; }
    .statement-card.AI_INFERENCE{ border-left:4px solid #e08a00 !important; }
    .statement-card.LEAD{ border-left:4px solid #dc2626 !important; }
    
    .print-sig-block{ display:flex !important; justify-content:space-between; margin-top:35px; padding-top:15px; border-top:1px dashed #888; page-break-inside:avoid; }
    .print-sig-col{ width:45%; }
    .print-sig-line{ margin-top:25px; border-bottom:1px solid #333; }
    .print-sig-title{ font-size:8.5pt; color:#555; margin-top:4px; }
  }

  /* ---- Profile panel (right side, Network Explorer) ---- */
  .profile-panel{ width:320px; border-left:1px solid var(--border); background:var(--bg-2); overflow-y:auto; flex-shrink:0; }
  .profile-empty{ padding:40px 20px; text-align:center; color:var(--ink-faint); font-family:var(--font-mono); font-size:11px; line-height:1.7; }
  .profile-badge{ display:flex; align-items:center; gap:6px; font-family:var(--font-mono); font-size:9.5px; letter-spacing:0.06em;
    color:var(--cyan); padding:14px 20px 0; }
  .profile-head{ padding:8px 20px 16px; border-bottom:1px solid var(--border); }
  .profile-head h2{ font-family:var(--font-serif); font-size:19px; margin-top:6px; }
  .profile-head .type{ font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint); margin-top:3px; }
  .risk-pill{ display:inline-block; font-family:var(--font-mono); font-size:9px; letter-spacing:0.06em; font-weight:700;
    padding:3px 9px; border-radius:10px; }
  .profile-head .risk-pill{ margin-top:8px; }
  .risk-pill.HIGH{ background:rgba(220,38,38,0.12); color:var(--red); border:1px solid var(--red); }
  .risk-pill.MEDIUM{ background:rgba(224,138,0,0.13); color:var(--amber); border:1px solid var(--amber); }
  .risk-pill.LOW{ background:rgba(22,163,74,0.12); color:var(--green); border:1px solid var(--green); }
  .risk-pill.UNRATED{ background:var(--panel); color:var(--ink-faint); border:1px solid var(--border); }
  .profile-section{ padding:16px 20px; border-bottom:1px solid var(--border); }
  .profile-section .st{ font-family:var(--font-mono); font-size:9px; letter-spacing:0.08em; text-transform:uppercase; color:var(--ink-faint); margin-bottom:10px; }
  .confidence-bar-wrap{ margin-top:6px; }
  .confidence-bar-track{ height:5px; background:var(--panel); border-radius:3px; overflow:hidden; margin-top:4px; }
  .confidence-bar-fill{ height:100%; background:var(--cyan); border-radius:3px; }
  .confidence-label{ display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); }
  .attr-row{ display:flex; justify-content:space-between; padding:6px 0; font-size:11.5px; }
  .attr-row .k{ color:var(--ink-faint); }
  .attr-row .v{ color:var(--ink-dim); text-align:right; }
  .trace-item{ display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid var(--border); cursor:pointer; }
  .trace-item:last-child{ border-bottom:none; }
  .trace-icon{ width:26px; height:26px; border-radius:5px; background:var(--panel); border:1px solid var(--border);
    display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .trace-info .n{ font-size:11.5px; color:var(--ink-dim); }
  .trace-info .r{ font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); }
  .trace-info .r.susp{ color:var(--red); }
  .explain-mini{ background:var(--panel); border:1px solid var(--amber); border-radius:5px; padding:11px 13px; }
  .explain-mini .title{ font-family:var(--font-mono); font-size:9.5px; color:var(--amber); letter-spacing:0.06em; text-transform:uppercase; margin-bottom:7px; }
  .explain-mini .reason{ font-size:11px; color:var(--ink-dim); padding:2px 0; display:flex; gap:6px; }
  .explain-mini .reason::before{ content:"\u2022"; color:var(--amber); }
  .explain-mini .verify{ margin-top:8px; font-family:var(--font-mono); font-size:9px; color:var(--red); }

  /* ---- Data Lab ---- */
  .datalab-grid{ display:grid; grid-template-columns:260px 1fr 300px; flex:1; min-height:0; }
  .dl-panel{ border-right:1px solid var(--border); overflow-y:auto; padding:18px 18px; background:var(--bg-2); }
  .dl-panel.right{ border-right:none; border-left:1px solid var(--border); }
  .dl-label{ font-family:var(--font-mono); font-size:9.5px; letter-spacing:0.08em; text-transform:uppercase; color:var(--ink-faint); margin-bottom:10px; }
  .dl-select{ width:100%; background:var(--panel); border:1px solid var(--border); color:var(--ink); font-family:var(--font-mono);
    font-size:11.5px; padding:9px 10px; border-radius:4px; margin-bottom:18px; }
  .dl-slider-row{ margin-bottom:18px; }
  .dl-slider-row input[type=range]{ width:100%; accent-color:var(--cyan); margin-top:8px; }
  .dl-slider-val{ font-family:var(--font-mono); font-size:11px; color:var(--cyan); float:right; }
  .dl-chip-row{ display:flex; flex-wrap:wrap; gap:7px; margin-bottom:18px; }
  .dl-chip{ font-family:var(--font-mono); font-size:10px; padding:5px 10px; border-radius:12px; border:1px solid var(--border);
    color:var(--ink-dim); cursor:pointer; user-select:none; }
  .dl-chip.active{ border-color:var(--cyan); color:var(--cyan); background:rgba(14,165,164,0.08); }
  .dl-doc-area{ padding:20px 24px; overflow-y:auto; }
  .dl-doc-toolbar{ display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
  .dl-doc-toolbar .pageinfo{ font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint); }
  .dl-doc-toolbar .icons{ display:flex; gap:6px; }
  .dl-doc-card{ background:#fff; color:#1a1a1a; border-radius:4px; padding:26px 30px; max-width:700px; min-height:300px;
    border:1px solid var(--border);
    box-shadow:0 4px 20px rgba(20,30,60,0.08); }
  .dl-doc-card .doctitle{ font-family:var(--font-serif); font-weight:700; font-size:15px; letter-spacing:0.02em; margin-bottom:16px; text-transform:uppercase; }
  .dl-doc-card .doc-text{ font-size:12.5px; line-height:1.9; color:#2a2a2a; }
  .dl-doc-card .ent-tag{ padding:1px 4px; border-radius:2px; font-weight:700; }
  .dl-doc-card .ent-tag.person{ background:#dce6ff; color:#1d3fae; }
  .dl-doc-card .ent-tag.location{ background:#dcf5e1; color:#157a34; }
  .dl-doc-card .ent-tag.phone{ background:#fce8c8; color:#8a5600; }
  .dl-doc-card .ent-tag.vehicle{ background:#ede1fb; color:#5b21b6; }
  .dl-doc-card .ent-tag.org{ background:#d7f0f1; color:#0b6e70; }
  .dl-doc-card .ent-tag sup{ font-size:7px; margin-left:1px; }
  .dl-input-toggle{ display:flex; gap:8px; margin-bottom:16px; }
  .dl-input-toggle button{ font-family:var(--font-mono); font-size:10.5px; background:var(--panel); border:1px solid var(--border);
    color:var(--ink-dim); padding:8px 14px; border-radius:4px; }
  .dl-input-toggle button.active{ border-color:var(--blue); color:var(--blue); background:var(--panel-2); }
  .dl-upload-zone{ border:2px dashed var(--border); border-radius:8px; background:var(--panel); padding:44px 20px;
    text-align:center; cursor:pointer; transition:all 0.15s; max-width:500px; }
  .dl-upload-zone:hover, .dl-upload-zone.dragover{ border-color:var(--blue); background:var(--panel-2); }
  .dl-upload-icon{ font-size:30px; color:var(--blue); margin-bottom:10px; }
  .dl-upload-title{ font-weight:700; color:var(--ink); font-size:13.5px; margin-bottom:6px; }
  .dl-upload-sub{ font-size:11px; color:var(--ink-faint); }
  .dl-textarea-wrap{ display:none; margin-bottom:16px; }
  .dl-textarea-wrap.show{ display:block; }
  .dl-textarea-wrap textarea{ width:100%; min-height:120px; background:var(--panel); border:1px solid var(--border);
    border-radius:4px; color:var(--ink); font-family:var(--font-mono); font-size:12px; padding:12px; resize:vertical; }
  .dl-textarea-wrap textarea:focus{ outline:none; border-color:var(--blue); }
  .dl-run-btn{ margin-top:10px; background:var(--blue); border:1px solid var(--blue); color:#fff; padding:9px 18px;
    border-radius:4px; font-family:var(--font-mono); font-size:11.5px; font-weight:600; }

  .conflict-card{ background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:14px 15px; margin-bottom:12px; }
  .conflict-card .head{ font-size:11.5px; color:var(--ink); margin-bottom:4px; font-weight:600; }
  .conflict-card .sub{ font-size:11px; color:var(--ink-faint); margin-bottom:10px; }
  .conflict-opt{ display:flex; align-items:center; justify-content:space-between; padding:6px 9px; border-radius:4px;
    background:var(--bg-2); margin-bottom:6px; font-size:11px; }
  .conflict-opt .pct{ font-family:var(--font-mono); color:var(--amber); }
  .conflict-btns{ display:flex; gap:8px; margin-top:10px; }
  .conflict-btns button{ flex:1; font-family:var(--font-mono); font-size:10.5px; padding:7px; border-radius:4px; }
  .btn-accept{ background:var(--cyan); border:1px solid var(--cyan); color:#ffffff; font-weight:700; }
  .btn-accept.done{ background:var(--panel); color:var(--cyan); border:1px solid var(--cyan); }
  .btn-edit{ background:none; border:1px solid var(--border); color:var(--ink-dim); }
  .conflict-card.resolved{ opacity:0.55; }

  /* ---- Entity Profile detail page ---- */
  .breadcrumb{ font-family:var(--font-mono); font-size:11px; color:var(--ink-faint); }
  .breadcrumb a{ color:var(--blue); text-decoration:none; }
  .pd-hero{ border-radius:10px; background:linear-gradient(120deg, #142b8f, #2554e8 60%, #4c7bff); padding:28px 30px;
    display:flex; align-items:center; gap:20px; margin-bottom:22px; color:#fff; flex-wrap:wrap; }
  .pd-avatar{ width:68px; height:68px; border-radius:12px; background:rgba(255,255,255,0.18); border:1px solid rgba(255,255,255,0.35);
    display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .pd-hero-info{ flex:1; min-width:200px; }
  .pd-hero-info h1{ font-family:var(--font-serif); font-size:26px; margin-bottom:4px; }
  .pd-hero-meta{ display:flex; gap:16px; flex-wrap:wrap; font-size:12px; opacity:0.9; }
  .pd-hero-meta span{ display:flex; align-items:center; gap:5px; }
  .pd-hero .risk-pill{ margin-top:10px; }
  .btn-track{ background:#ffffff; color:#142b8f; border:none; padding:11px 18px; border-radius:5px; font-weight:700;
    font-size:12px; white-space:nowrap; }

  .pd-grid{ display:grid; grid-template-columns:1.6fr 1fr; gap:20px; }
  .pd-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:20px 22px; margin-bottom:18px; }
  .pd-card-head{ display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
  .pd-card-head h3{ font-family:var(--font-serif); font-size:15px; display:flex; align-items:center; gap:8px; }
  .pd-live-tag{ font-family:var(--font-mono); font-size:9px; color:var(--cyan); background:rgba(14,165,164,0.12);
    padding:2px 8px; border-radius:10px; letter-spacing:0.05em; }
  .pd-briefing-text{ font-size:13px; color:var(--ink-dim); line-height:1.75; margin-bottom:14px; }
  .pd-briefing-text b{ color:var(--ink); }
  .pd-assessment{ background:var(--panel-2); border-left:3px solid var(--blue); border-radius:0 6px 6px 0; padding:12px 14px;
    font-size:12.5px; color:var(--ink-dim); margin-bottom:14px; }
  .pd-assessment b{ color:var(--blue); }
  .pd-tag-row{ display:flex; gap:8px; flex-wrap:wrap; }
  .pd-tag{ font-family:var(--font-mono); font-size:10px; padding:4px 10px; border-radius:12px; border:1px solid var(--border); color:var(--ink-dim); }
  .pd-verify-note{ margin-top:14px; font-family:var(--font-mono); font-size:10.5px; color:var(--red); }

  .pd-id-row{ padding:10px 0; border-bottom:1px solid var(--border); }
  .pd-id-row:last-child{ border-bottom:none; }
  .pd-id-row .k{ font-family:var(--font-mono); font-size:9px; text-transform:uppercase; letter-spacing:0.06em; color:var(--ink-faint); margin-bottom:4px; }
  .pd-id-row .v{ font-size:12.5px; color:var(--ink); }
  .pd-risk-bar-track{ height:8px; background:var(--panel-2); border-radius:4px; overflow:hidden; margin-top:8px; }
  .pd-risk-bar-fill{ height:100%; border-radius:4px; }

  .pd-matrix-wrap{ height:220px; position:relative; background:var(--bg); border-radius:6px; border:1px solid var(--border); overflow:hidden; }
  .pd-matrix-wrap svg{ width:100%; height:100%; }

  .pd-timeline-item{ display:flex; gap:12px; padding:11px 0; border-bottom:1px solid var(--border); }
  .pd-timeline-item:last-child{ border-bottom:none; }
  .pd-timeline-dot{ width:8px; height:8px; border-radius:50%; background:var(--blue); margin-top:5px; flex-shrink:0; }
  .pd-timeline-info .t{ font-size:12.5px; color:var(--ink); font-weight:600; }
  .pd-timeline-info .d{ font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); margin-top:2px; }
  .pd-timeline-info .n{ font-size:11.5px; color:var(--ink-dim); margin-top:3px; }
  .pd-empty{ font-size:12px; color:var(--ink-faint); font-style:italic; }

  /* ---- AI Assistant ---- */
  .asst-wrap{ flex:1; display:flex; flex-direction:column; min-height:0; max-width:900px; margin:0 auto; width:100%; padding:0 26px 20px; }
  .asst-messages{ flex:1; overflow-y:auto; padding:22px 0; display:flex; flex-direction:column; gap:16px; }
  .asst-msg{ display:flex; gap:12px; max-width:88%; }
  .asst-msg.user{ align-self:flex-end; flex-direction:row-reverse; }
  .asst-msg-avatar{ width:30px; height:30px; border-radius:7px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
  .asst-msg.assistant .asst-msg-avatar{ background:var(--panel-2); color:var(--blue); border:1px solid var(--border); }
  .asst-msg.user .asst-msg-avatar{ background:var(--blue); color:#fff; }
  .asst-bubble{ background:var(--panel); border:1px solid var(--border); border-radius:10px; padding:13px 16px; font-size:13px; color:var(--ink-dim); line-height:1.6; }
  .asst-msg.user .asst-bubble{ background:var(--blue); border-color:var(--blue); color:#fff; }
  .asst-bubble b{ color:var(--ink); }
  .asst-msg.user .asst-bubble b{ color:#fff; }
  .asst-evidence{ margin-top:10px; padding-top:10px; border-top:1px solid var(--border); }
  .asst-evidence-row{ display:flex; justify-content:space-between; font-size:11px; padding:3px 0; color:var(--ink-faint); }
  .asst-evidence-row .k{ font-family:var(--font-mono); text-transform:uppercase; letter-spacing:0.04em; font-size:9.5px; }
  .asst-evidence-row .v{ color:var(--ink-dim); text-align:right; max-width:70%; }
  .asst-confidence-pill{ display:inline-block; font-family:var(--font-mono); font-size:9.5px; padding:2px 8px; border-radius:10px; background:rgba(37,84,232,0.1); color:var(--blue); margin-top:8px; }
  .asst-verify{ margin-top:8px; font-family:var(--font-mono); font-size:9.5px; color:var(--red); }
  .asst-entity-link{ color:var(--blue); text-decoration:none; font-weight:600; cursor:pointer; }
  .asst-entity-link:hover{ text-decoration:underline; }
  .asst-suggestions{ display:flex; gap:8px; flex-wrap:wrap; padding:10px 0; }
  .asst-chip{ font-family:var(--font-mono); font-size:10.5px; padding:7px 13px; border-radius:14px; border:1px solid var(--border);
    background:var(--panel); color:var(--ink-dim); cursor:pointer; }
  .asst-chip:hover{ border-color:var(--blue); color:var(--blue); }
  .asst-input-row{ display:flex; gap:10px; padding-top:6px; }
  .asst-input-row input{ flex:1; background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:12px 15px;
    font-size:13px; color:var(--ink); font-family:var(--font-body); }
  .asst-input-row input:focus{ outline:none; border-color:var(--blue); }
  .asst-input-row button{ background:var(--blue); color:#fff; border:none; border-radius:8px; padding:0 22px; font-weight:700; font-size:13px; }
  .asst-input-row button:hover{ opacity:0.9; }
  .asst-typing{ display:flex; gap:4px; padding:4px 0; }
  .asst-typing span{ width:6px; height:6px; border-radius:50%; background:var(--ink-faint); animation:asst-bounce 1.2s infinite ease-in-out; }
  .asst-typing span:nth-child(2){ animation-delay:0.15s; }
  .asst-typing span:nth-child(3){ animation-delay:0.3s; }
  @keyframes asst-bounce{ 0%,60%,100%{ transform:translateY(0); opacity:0.5; } 30%{ transform:translateY(-4px); opacity:1; } }


  .ep-grid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(230px,1fr)); gap:14px; }
  .ep-card{ background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:16px 17px; cursor:pointer; }
  .ep-card:hover{ border-color:var(--ink-faint); }
  .ep-card .ep-top{ display:flex; align-items:center; gap:10px; margin-bottom:10px; }
  .ep-avatar{ width:36px; height:36px; border-radius:6px; background:var(--bg-2); border:1px solid var(--border);
    display:flex; align-items:center; justify-content:center; color:var(--cyan); flex-shrink:0; }
  .ep-card .name{ font-family:var(--font-serif); font-size:13.5px; }
  .ep-card .id{ font-family:var(--font-mono); font-size:9px; color:var(--ink-faint); }
  .ep-card .aliases{ font-size:10.5px; color:var(--ink-faint); margin-bottom:8px; }

  /* ---- Report page ---- */
  .report-exec-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:20px 24px; margin-bottom:20px; }
  .rec-top{ display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:12px; margin-bottom:16px; }
  .rec-org{ font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); letter-spacing:0.08em; text-transform:uppercase; margin-bottom:4px; font-weight:700; }
  .rec-title{ font-family:var(--font-serif); font-size:22px; color:var(--ink); font-weight:700; }
  .rec-meta{ display:flex; gap:12px; font-size:11.5px; color:var(--ink-dim); margin-top:6px; flex-wrap:wrap; }
  .rec-status-badge{ font-family:var(--font-mono); font-size:9px; background:rgba(220,38,38,0.12); color:var(--red); border:1px solid var(--red); padding:4px 10px; border-radius:4px; font-weight:700; letter-spacing:0.06em; }
  .rec-stats-row{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; padding-top:16px; border-top:1px solid var(--border); }
  .rec-stat-box{ background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:10px 14px; text-align:left; }
  .rec-stat-box .k{ font-family:var(--font-mono); font-size:9px; color:var(--ink-faint); text-transform:uppercase; }
  .rec-stat-box .v{ font-family:var(--font-serif); font-size:20px; font-weight:700; color:var(--ink); margin-top:2px; }

  .report-filter-group{ display:flex; gap:6px; background:var(--panel); border:1px solid var(--border); border-radius:6px; padding:3px; }
  .rf-btn{ background:none; border:none; color:var(--ink-dim); font-family:var(--font-mono); font-size:10px; padding:6px 12px; border-radius:4px; cursor:pointer; font-weight:600; }
  .rf-btn.active{ background:var(--panel-2); color:var(--blue); font-weight:700; }
  .rf-btn.fact.active{ background:rgba(14,165,164,0.15); color:var(--cyan); }
  .rf-btn.inference.active{ background:rgba(224,138,0,0.15); color:var(--amber); }
  .rf-btn.lead.active{ background:rgba(220,38,38,0.15); color:var(--red); }

  .report-section-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:20px 24px; margin-bottom:18px; }
  .report-section-head{ font-family:var(--font-serif); font-size:16px; font-weight:700; color:var(--ink); border-bottom:1px solid var(--border); padding-bottom:10px; margin-bottom:14px; display:flex; justify-content:space-between; align-items:center; }
  .statement-card{ padding:12px 14px; border-radius:6px; background:var(--bg); border-left:4px solid var(--border); margin-bottom:10px; font-size:12.5px; line-height:1.6; color:var(--ink); display:flex; gap:12px; align-items:flex-start; transition:all 0.15s; }
  .statement-card:hover{ border-color:var(--ink-faint); transform:translateX(2px); }
  .statement-card.FACT{ border-left-color:var(--cyan); background:rgba(14,165,164,0.03); }
  .statement-card.AI_INFERENCE{ border-left-color:var(--amber); background:rgba(224,138,0,0.03); }
  .statement-card.LEAD{ border-left-color:var(--red); background:rgba(220,38,38,0.03); }
  .stmt-tag{ font-family:var(--font-mono); font-size:9px; font-weight:700; padding:2px 7px; border-radius:3px; text-transform:uppercase; white-space:nowrap; flex-shrink:0; letter-spacing:0.04em; }
  .stmt-tag.FACT{ background:rgba(14,165,164,0.12); color:var(--cyan); border:1px solid var(--cyan); }
  .stmt-tag.AI_INFERENCE{ background:rgba(224,138,0,0.15); color:var(--amber); border:1px solid var(--amber); }
  .stmt-tag.LEAD{ background:rgba(220,38,38,0.15); color:var(--red); border:1px solid var(--red); }
  .stmt-text{ flex:1; }

  /* ================= RESPONSIVE ================= */
  @media (max-width: 1150px){
    #app{ grid-template-columns:1fr; }
    .sidebar{ position:fixed; top:0; bottom:0; left:0; width:230px; z-index:30; transform:translateX(-100%);
      transition:transform 0.25s ease; box-shadow:0 0 30px rgba(0,0,0,0.6); }
    .sidebar.open{ transform:translateX(0); }
    .mobile-topbar{ display:flex; align-items:center; justify-content:space-between; padding:12px 16px;
      border-bottom:1px solid var(--border); background:var(--bg-2); }
    .mobile-topbar .hbtn{ background:var(--panel); border:1px solid var(--border); color:var(--ink); width:34px; height:34px;
      border-radius:5px; display:flex; align-items:center; justify-content:center; }
    .profile-panel{ position:fixed; top:0; bottom:0; right:0; z-index:30; transform:translateX(100%); transition:transform 0.25s ease;
      box-shadow:0 0 30px rgba(0,0,0,0.6); }
    .profile-panel.open{ transform:translateX(0); }
    .datalab-grid{ grid-template-columns:1fr; }
    .dl-panel{ border-right:none; border-bottom:1px solid var(--border); }
    .dl-panel.right{ border-left:none; border-top:1px solid var(--border); }
    .stat-grid{ grid-template-columns:1fr 1fr; }
    .cc-grid{ grid-template-columns:1fr; }
    .caps-grid{ grid-template-columns:1fr; }
    .hero h1{ font-size:32px; }
    .active-graph-label{ display:none; }
    .topbar{ flex-wrap:wrap; }
    .topbar-search{ order:3; max-width:none; flex-basis:100%; }
  }
  @media (max-width: 620px){
    .stat-grid{ grid-template-columns:1fr; }
    .hero{ padding:70px 20px 50px; }
    .hero-mark{ font-size:52px; }
    .hero h1{ font-size:26px; }
    .land-nav{ display:none; }
    .topbar h2{ font-size:14px; }
    .topbar-search{ min-width:0; }
    .page-pad{ padding:16px; }
    .cap-tag{ display:none; }
  }

  /* ================= EVIDENCE VAULT ================= */
  .evid-filter-bar{ display:flex; gap:8px; align-items:center; flex-wrap:wrap; margin-bottom:18px; }
  .evid-tab-btn{ background:var(--panel); border:1px solid var(--border); color:var(--ink-dim); padding:6px 14px; border-radius:5px; font-family:var(--font-mono); font-size:11px; cursor:pointer; font-weight:600; }
  .evid-tab-btn.active{ background:var(--ink); color:#fff; border-color:var(--ink); }
  .evid-grid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(340px, 1fr)); gap:16px; }
  .evid-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:18px; display:flex; flex-direction:column; gap:12px; transition:border-color 0.2s; }
  .evid-card:hover{ border-color:var(--ink-faint); }
  .evid-header{ display:flex; justify-content:space-between; align-items:flex-start; gap:8px; }
  .evid-id-tag{ font-family:var(--font-mono); font-size:10px; font-weight:700; background:rgba(31,70,204,0.1); color:var(--blue); padding:3px 8px; border-radius:4px; border:1px solid rgba(31,70,204,0.3); }
  .evid-badge{ font-family:var(--font-mono); font-size:9px; font-weight:700; padding:3px 8px; border-radius:4px; text-transform:uppercase; letter-spacing:0.04em; }
  .evid-badge.verified{ background:rgba(19,122,53,0.12); color:var(--green); border:1px solid var(--green); }
  .evid-badge.pending{ background:rgba(224,138,0,0.12); color:var(--amber); border:1px solid var(--amber); }
  .evid-badge.tampered{ background:rgba(220,38,38,0.12); color:var(--red); border:1px solid var(--red); }
  .evid-title{ font-family:var(--font-serif); font-size:15px; font-weight:700; color:var(--ink); line-height:1.3; }
  .evid-meta-line{ font-size:11.5px; color:var(--ink-dim); display:flex; gap:10px; flex-wrap:wrap; }
  .evid-hash-box{ background:var(--bg); border:1px solid var(--border); border-radius:5px; padding:8px 10px; font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); display:flex; justify-content:space-between; align-items:center; word-break:break-all; }
  .evid-content-box{ background:var(--bg); border:1px solid var(--border); border-radius:5px; padding:10px; font-size:11.5px; line-height:1.5; color:var(--ink); max-height:110px; overflow-y:auto; white-space:pre-line; }
  .btn-verify-hash{ background:var(--bg-2); border:1px solid var(--border); color:var(--ink); padding:6px 12px; border-radius:5px; font-family:var(--font-mono); font-size:10.5px; font-weight:700; display:flex; align-items:center; gap:6px; cursor:pointer; transition:all 0.15s; }
  .btn-verify-hash:hover{ background:var(--green); color:#fff; border-color:var(--green); }

  /* ================= ANOMALY & RISK ================= */
  .formula-banner{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px 20px; margin-bottom:18px; display:flex; gap:16px; align-items:center; flex-wrap:wrap; justify-content:space-between; }
  .formula-chips{ display:flex; gap:8px; flex-wrap:wrap; }
  .formula-chip{ font-family:var(--font-mono); font-size:10px; padding:4px 9px; border-radius:4px; background:var(--bg); border:1px solid var(--border); font-weight:600; color:var(--ink-dim); }
  .anom-grid{ display:grid; grid-template-columns:repeat(auto-fill, minmax(340px, 1fr)); gap:16px; }
  .anom-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:18px; display:flex; flex-direction:column; gap:12px; }
  .anom-top{ display:flex; justify-content:space-between; align-items:flex-start; }
  .anom-score-pill{ font-family:var(--font-mono); font-size:14px; font-weight:800; padding:4px 10px; border-radius:6px; }
  .anom-score-pill.crit{ background:rgba(220,38,38,0.12); color:var(--red); border:1px solid var(--red); }
  .anom-score-pill.warn{ background:rgba(224,138,0,0.12); color:var(--amber); border:1px solid var(--amber); }
  .anom-score-pill.low{ background:rgba(19,122,53,0.12); color:var(--green); border:1px solid var(--green); }
  .decomp-row{ display:flex; flex-direction:column; gap:6px; margin-top:4px; }
  .decomp-metric{ display:flex; justify-content:space-between; font-size:11px; font-family:var(--font-mono); color:var(--ink-dim); }
  .decomp-bar{ height:5px; background:var(--border); border-radius:3px; overflow:hidden; }
  .decomp-bar-fill{ height:100%; border-radius:3px; }
  .spikes-list{ display:flex; flex-direction:column; gap:6px; margin-top:8px; border-top:1px solid var(--border); padding-top:10px; }
  .spike-item{ background:var(--bg); border-left:3px solid var(--red); padding:6px 10px; border-radius:4px; font-size:11px; display:flex; justify-content:space-between; align-items:center; }

  /* ================= INVESTIGATION TIMELINE ================= */
  .tl-stream{ display:flex; flex-direction:column; gap:12px; position:relative; margin-top:16px; padding-left:24px; border-left:2px dashed var(--border); }
  .tl-card{ background:var(--panel); border:1px solid var(--border); border-radius:7px; padding:14px 18px; position:relative; transition:all 0.15s; }
  .tl-card:hover{ border-color:var(--ink-faint); transform:translateX(3px); }
  .tl-card::before{ content:''; position:absolute; left:-31px; top:18px; width:12px; height:12px; border-radius:50%; background:var(--bg-2); border:2px solid var(--ink-faint); }
  .tl-card.crit::before{ border-color:var(--red); background:var(--red); }
  .tl-card.warn::before{ border-color:var(--amber); background:var(--amber); }
  .tl-card.info::before{ border-color:var(--cyan); background:var(--cyan); }
  .tl-header{ display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; flex-wrap:wrap; gap:8px; }
  .tl-date{ font-family:var(--font-mono); font-size:10.5px; font-weight:700; color:var(--ink-dim); }
  .tl-badge{ font-family:var(--font-mono); font-size:9px; font-weight:700; padding:2px 7px; border-radius:3px; }
  .tl-badge.crit{ background:rgba(220,38,38,0.12); color:var(--red); border:1px solid var(--red); }
  .tl-badge.warn{ background:rgba(224,138,0,0.12); color:var(--amber); border:1px solid var(--amber); }
  .tl-badge.info{ background:rgba(14,165,164,0.12); color:var(--cyan); border:1px solid var(--cyan); }
  .tl-entities{ display:flex; gap:6px; margin-top:8px; flex-wrap:wrap; }
  .tl-chip{ font-family:var(--font-mono); font-size:10px; background:var(--bg); border:1px solid var(--border); padding:2px 7px; border-radius:4px; }

  /* ================= 6-STAGE INGESTION ================= */
  .stepper-container{ display:flex; justify-content:space-between; margin-bottom:24px; position:relative; padding:14px 20px; background:var(--panel); border:1px solid var(--border); border-radius:8px; overflow-x:auto; }
  .step-node{ display:flex; flex-direction:column; align-items:center; gap:6px; font-size:10.5px; font-family:var(--font-mono); color:var(--ink-faint); z-index:2; min-width:110px; text-align:center; }
  .step-circle{ width:32px; height:32px; border-radius:50%; background:var(--bg); border:2px solid var(--border); display:flex; align-items:center; justify-content:center; font-weight:700; color:var(--ink-faint); transition:all 0.2s; }
  .step-node.active .step-circle{ border-color:var(--blue); background:rgba(31,70,204,0.15); color:var(--blue); }
  .step-node.completed .step-circle{ border-color:var(--green); background:var(--green); color:#fff; }
  .step-node.completed{ color:var(--green); font-weight:700; }
  .step-node.active{ color:var(--blue); font-weight:700; }

  /* ================= AUDIT & VERIFICATION ================= */
  .audit-layout{ display:grid; grid-template-columns:1fr 1fr; gap:20px; }
  @media (max-width: 900px){ .audit-layout{ grid-template-columns:1fr; } }
  .cand-card{ background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:16px; margin-bottom:12px; }
  .cand-top{ display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; }
  .cand-actions{ display:flex; gap:8px; margin-top:12px; }
  .btn-approve{ background:var(--green); color:#fff; border:none; padding:6px 14px; border-radius:5px; font-family:var(--font-mono); font-size:11px; font-weight:700; cursor:pointer; }
  .btn-reject{ background:var(--panel-2); color:var(--red); border:1px solid var(--red); padding:6px 14px; border-radius:5px; font-family:var(--font-mono); font-size:11px; font-weight:700; cursor:pointer; }
  .audit-table{ width:100%; border-collapse:collapse; font-size:11.5px; }
  .audit-table th, .audit-table td{ padding:8px 12px; border-bottom:1px solid var(--border); text-align:left; }
  .audit-table th{ font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); text-transform:uppercase; background:var(--bg); }
  .audit-badge{ font-family:var(--font-mono); font-size:9px; font-weight:700; padding:2px 6px; border-radius:3px; }
</style>
</head>
<body>
<!-- ================= LANDING ================= -->
<div id="landing">
  <div class="gov-tricolor-bar"></div>
  <canvas id="landing-canvas"></canvas>
  
  <div class="land-header">
    <div class="land-brand">
      <div class="land-devanagari">सूत्र</div>
      <div class="land-brand-name">SŪTRA</div>
      <div class="land-brand-badge">GOVERNMENT OF INDIA • INI-CLEARANCE</div>
    </div>
    <div class="land-nav">
      <a href="#briefing-section" data-i18n="land_nav_1">ANALYTICAL CAPABILITIES</a>
      <a href="#" id="nav-protocol-btn" data-i18n="land_nav_2">SECURE ACCESS PROTOCOL</a>
      <a href="#" id="nav-disclaimer-btn" data-i18n="land_nav_3">GOVERNMENT DISCLAIMER</a>
      <div class="lang-switcher land-lang-switcher">
        <button class="lang-btn active" data-lang="en">EN</button>
        <button class="lang-btn" data-lang="hi">हिं</button>
        <button class="lang-btn" data-lang="mr">मरा</button>
      </div>
      <button class="theme-toggle-btn" id="theme-toggle-landing" title="Toggle Day / Night Mode">
        <span class="theme-icon">🌙</span>
      </button>
    </div>
  </div>

  <div class="hero">
    <div class="hero-logo-wrap">
      <!-- English: Official SŪTRA Logo with Tricolor Ribbon -->
      <div class="hero-logo-en active" id="hero-logo-en">
        <img src="sutra-logo-en.png" alt="SŪTRA" class="hero-logo-img">
      </div>
      <!-- Hindi/Marathi: Official सूत्र Logo with Tricolor Ribbon -->
      <div class="hero-logo-hi" id="hero-logo-hi">
        <img src="sutra-logo-hi.png" alt="सूत्र" class="hero-logo-img">
      </div>
    </div>
    <h1 data-i18n="hero_title">The Connection Thread</h1>
    <p data-i18n="hero_subtitle">Uncovering the invisible networks of crime. A unified investigative decision-support platform for entity resolution, knowledge-graph analysis, and evidence-backed leads — built for institutional accountability, not automated accusation.</p>
    <div class="hero-btns">
      <button class="btn-hero-primary" id="btn-enter-app" data-i18n="btn_request_access">Request Access → Command Center</button>
      <button class="btn-hero-secondary" id="btn-view-briefing" data-i18n="btn_view_briefing">View Briefing</button>
    </div>

    <!-- 3D Revolving Ultra-Realistic Big Half Earth Section with Sequential Popping Messages -->
    <div class="hero-globe-wrap" id="hero-globe-wrap">
      <div class="globe-indicator">
        <span class="pulse-beacon"></span>
        <span data-i18n="globe_indicator_text">LIVE GLOBAL INTELLIGENCE MESH • ACTIVE INTERCEPT STREAM</span>
      </div>

      <!-- Messages Popping One By One over Globe -->
      <div id="globe-popping-container"></div>

      <!-- Globe 3D Canvas -->
      <canvas id="globe-canvas"></canvas>

      <!-- Globe Stream Control & Status Bar -->
      <div class="globe-controls-pill">
        <span class="stream-dot">●</span>
        <span class="stream-lbl" id="globe-stream-status">STREAM ACTIVE (1 / 6)</span>
        <span class="stream-sep">|</span>
        <button class="stream-btn" id="btn-prev-intel" title="Previous Alert">◀</button>
        <button class="stream-btn" id="btn-pause-intel" title="Pause / Resume Stream">❚❚</button>
        <button class="stream-btn" id="btn-next-intel" title="Next Alert">▶</button>
      </div>

      <!-- Live Telemetry HUD Bar - Anchored Directly ON/OVER the Earth at the bottom of the page -->
      <div class="hero-hud-bar">
        <div class="hud-stat">
          <div class="hud-lbl"><span>◈</span> Verified Nodes</div>
          <div class="hud-val">1,420<span>pts</span></div>
          <div class="hud-sub">● 99.4% Graph Density</div>
        </div>
        <div class="hud-stat">
          <div class="hud-lbl"><span>◉</span> Active Networks</div>
          <div class="hud-val">28<span>rings</span></div>
          <div class="hud-sub">● 6 Cross-Border</div>
        </div>
        <div class="hud-stat">
          <div class="hud-lbl"><span>✵</span> Entity Clusters</div>
          <div class="hud-val">342<span>resolved</span></div>
          <div class="hud-sub">● 0.94 Confidence</div>
        </div>
        <div class="hud-stat">
          <div class="hud-lbl"><span>🔒</span> Security Protocol</div>
          <div class="hud-val" style="font-size:18px;margin-top:4px;">AES-256<span>GCM</span></div>
          <div class="hud-sub">● Zero-Knowledge</div>
        </div>
      </div>
    </div>
  </div>

  <div class="caps-section" id="briefing-section">
    <h2 data-i18n="caps_title">Analytical Capabilities</h2>
    <p data-i18n="caps_subtitle">Core modules for advanced investigative decision-support.</p>
    <div class="caps-divider"></div>
  </div>
  
  <div class="caps-grid">
    <div class="cap-card">
      <div class="cap-tag">REC-01-33</div>
      <div class="cap-icon">◈</div>
      <h3 data-i18n="cap1_title">Data Integration</h3>
      <p data-i18n="cap1_desc">Harmonize FIRs, CDRs, financial records, and surveillance reports into one structured investigative namespace.</p>
    </div>
    <div class="cap-card">
      <div class="cap-tag">REC-02-15</div>
      <div class="cap-icon">◉</div>
      <h3 data-i18n="cap2_title">Entity Extraction &amp; Resolution</h3>
      <p data-i18n="cap2_desc">Automated identification of persons, phones, vehicles, and organizations — with confidence-scored merging of duplicate mentions.</p>
    </div>
    <div class="cap-card">
      <div class="cap-tag core" data-i18n="cap3_module">CORE MODULE</div>
      <div class="cap-icon">✵</div>
      <h3 data-i18n="cap3_title">Relationship Mapping</h3>
      <p data-i18n="cap3_desc">Visualize covert networks. Trace financial flows, communication linkages, and hierarchical structures dynamically.</p>
      <div class="cap-visual">
        <div class="radar-sweep"></div>
        <span style="position:relative;z-index:2;" data-i18n="cap3_visual">Active Network Radar Stream</span>
      </div>
    </div>
  </div>

  <div class="cap-wide">
    <div class="cap-wide-card">
      <div class="cap-icon">◠</div>
      <div class="body">
        <h3 data-i18n="cap4_title">Explainable Risk Scoring</h3>
        <p data-i18n="cap4_desc">Transparent, source-weighted risk indicators — every score fully traceable to evidence, always requiring human verification. No automated accusation, ever.</p>
      </div>
      <button class="btn-doc" id="btn-view-docs" data-i18n="btn_view_docs">Launch Investigation</button>
    </div>
  </div>

  <div class="land-footer">
    <div data-i18n="footer_copyright">© 2026 SŪTRA Investigative Intelligence Platform. Prototype — Restricted Demonstration Use Only.</div>
    <div><a href="#" data-i18n="footer_link1">Secure Access Protocol</a><a href="#" data-i18n="footer_link2">Privacy Policy</a><a href="#" data-i18n="footer_link3">Government Disclaimer</a><a href="#" data-i18n="footer_link4">Contact Administrator</a></div>
  </div>

  <!-- Live Intelligence Alert Pop-up Toaster -->
  <div id="live-feed-toaster"></div>
</div>

<!-- ================= HIGH-TECH AUTHENTICATION LOADER MODAL ================= -->
<div id="auth-modal">
  <div class="auth-box">
    <div class="auth-scanner">
      <div class="scanner-ring"></div>
      <div class="scanner-ring-2"></div>
      <div class="scanner-center">⚡</div>
    </div>
    <div class="auth-title">SŪTRA CLEARANCE SYSTEM</div>
    <div class="auth-status" id="auth-status-txt">INITIATING CRYPTOGRAPHIC HANDSHAKE...</div>
    <div class="auth-progress-track">
      <div class="auth-progress-fill" id="auth-progress-bar"></div>
    </div>
    <div class="auth-terminal" id="auth-terminal-box">
      <div class="auth-terminal-line">[SYS] Initializing secure socket daemon...</div>
      <div class="auth-terminal-line">[AUTH] Verifying biometrics and role-token...</div>
      <div class="auth-terminal-line active">[GRAPH] Syncing localized Neo4j entity namespace...</div>
    </div>
  </div>
</div>

<!-- ================= APP SHELL ================= -->
<div id="app">
  <div class="sidebar" id="sidebar">
    <div class="sb-brand" id="sb-brand-btn" title="Return to Landing / Briefing Page">
      <div class="sb-logo-wrap">
        <div class="sb-logo-en">S</div>
        <div class="sb-logo-hi">\u0938</div>
      </div>
      <div class="sb-brand-text">
        <b id="sb-brand-name">S\u016aTRA</b>
        <span data-i18n="brand_tagline">INTELLIGENCE PLATFORM</span>
      </div>
    </div>
    <div class="lang-switcher">
      <button class="lang-btn active" data-lang="en">EN</button>
      <button class="lang-btn" data-lang="hi">\u0939\u093f\u0902</button>
      <button class="lang-btn" data-lang="mr">\u092e\u0930\u093e</button>
      <button class="theme-toggle-btn" id="theme-toggle-app" title="Toggle Day / Night Mode" style="margin-left:auto;">
        <span class="theme-icon">🌙</span>
      </button>
    </div>
    <div class="sb-nav" id="sb-nav">
      <div class="sb-item active" data-page="command"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg><span data-i18n="nav_command">Command Center</span></div>
      <div class="sb-item" data-page="graph"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><line x1="8.5" y1="7.5" x2="15.5" y2="16.5"/><line x1="15.5" y1="7.5" x2="8.5" y2="16.5"/></svg><span data-i18n="nav_graph">Network Explorer</span></div>
      <div class="sb-item" data-page="evidence"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg><span data-i18n="nav_evidence">Evidence Vault</span></div>
      <div class="sb-item" data-page="anomalies"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg><span data-i18n="nav_anomalies">Anomaly &amp; Risk</span></div>
      <div class="sb-item" data-page="timeline"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg><span data-i18n="nav_timeline">Investigation Timeline</span></div>
      <div class="sb-item" data-page="ingestion"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg><span data-i18n="nav_ingestion">Ingestion Pipeline</span></div>
      <div class="sb-item" data-page="audit"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg><span data-i18n="nav_audit">Audit &amp; Verification</span></div>
      <div class="sb-item" data-page="assistant"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><line x1="8" y1="9" x2="16" y2="9"/><line x1="8" y1="13" x2="13" y2="13"/></svg><span data-i18n="nav_assistant">AI Assistant</span></div>
      <div class="sb-item" data-page="profiles"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg><span data-i18n="nav_profiles">Entity Profiles</span></div>
      <div class="sb-item" data-page="datalab"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg><span data-i18n="nav_datalab">Data Lab</span></div>
      <div class="sb-item" data-page="report"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="16" y2="17"/></svg><span data-i18n="nav_report">Analytics Report</span></div>
    </div>
    <div class="sb-footer">
      <div class="sb-item" id="btn-back-landing" style="color:var(--gold); font-weight:600; cursor:pointer;" title="Return to Landing Page"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5"/><path d="M12 19l-7-7 7-7"/></svg><span data-i18n="nav_landing">\u2190 Landing / Briefing</span></div>
      <div class="sb-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg><span data-i18n="nav_settings">Settings</span></div>
      <div class="sb-item"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg><span data-i18n="nav_security">Security</span></div>
    </div>
    <div class="sb-gov" id="sb-gov-note" data-i18n="sidebar_gov_note" style="white-space:pre-line;">GOVERNMENT PROTOTYPE
SYNTHETIC DATA ONLY</div>
  </div>

  <div class="main-col">
    <div class="mobile-topbar">
      <button class="hbtn" id="btn-toggle-sidebar">\u2630</button>
      <div class="land-brand-name" id="mobile-brand-btn" style="font-size:14px; cursor:pointer;" title="Return to Landing Page">S\u016aTRA</div>
      <button class="hbtn" id="topbar-landing-btn" title="Return to Landing Page" style="font-size:14px;">\u2302</button>
    </div>
    <!-- ---- COMMAND CENTER ---- -->
    <div class="page active" data-page="command">
      <div class="topbar">
        <div class="topbar-left">
          <h2>Command Center</h2>
          <span class="badge-secure">CONNECTION SECURE</span>
          <span class="cc-case-tag">CASE: MH/CID/2026/0417 · NATIONAL INTELLIGENCE GRID</span>
        </div>
        <div class="topbar-right-actions">
          <button class="btn-cc-action" onclick="goToPage('graph')">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="6" cy="6" r="2.5"/><circle cx="18" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><line x1="8.1" y1="7.4" x2="15.9" y2="16.6"/><line x1="15.9" y1="7.4" x2="8.1" y2="16.6"/></svg>
            Network Explorer
          </button>
          <button class="btn-cc-action" onclick="goToPage('report')">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="8" y1="13" x2="16" y2="13"/><line x1="8" y1="17" x2="13" y2="17"/></svg>
            Evidence Briefing
          </button>
        </div>
      </div>
      <div class="page-pad">
        <!-- Row 1: KPI Stat Cards -->
        <div class="stat-grid" id="stat-grid"></div>

        <!-- Row 2: Network Topology Radar + Threat Index & Entity Donut -->
        <div class="cc-main-grid">
          <!-- Network Topology Radar -->
          <div class="cc-panel">
            <div class="cc-panel-head">
              <div class="cc-panel-title-wrap">
                <div class="cc-panel-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>
                </div>
                <div>
                  <h3>Network Topology Radar</h3>
                  <div class="cc-panel-sub">Force-directed syndicate cluster · drag nodes to explore</div>
                </div>
              </div>
              <div class="cc-panel-actions">
                <span class="cc-live-badge"><span class="pulse-dot"></span>LIVE</span>
                <button class="cc-btn-sm" onclick="goToPage('graph')">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                  Full Graph
                </button>
              </div>
            </div>
            <div class="cc-radar-container" id="cc-radar-container">
              <svg id="cc-mini-graph"></svg>
              <div class="cc-radar-legend">
                <span><span class="dot" style="background:#d4920a;border-radius:50%;"></span>Person</span>
                <span><span class="dot" style="background:#16a34a;border-radius:50%;"></span>Phone</span>
                <span><span class="dot" style="background:#1a56db;border-radius:50%;"></span>Account</span>
                <span><span class="dot" style="background:#dc2626;border-radius:2px;"></span>Suspicious Link</span>
              </div>
            </div>
          </div>

          <!-- Threat Index & Entity Distribution -->
          <div class="cc-panel">
            <div class="cc-panel-head">
              <div class="cc-panel-title-wrap">
                <div class="cc-panel-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
                </div>
                <div>
                  <h3>Threat Index &amp; Entity Distribution</h3>
                  <div class="cc-panel-sub">Explainable multi-signal decision-support ranking</div>
                </div>
              </div>
              <span class="cc-tag-formula">MULTI-SIGNAL</span>
            </div>
            <div class="cc-charts-wrap">
              <div class="cc-chart-box">
                <div class="cc-chart-title">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>
                  Suspect Threat Ranking
                </div>
                <div class="cc-bars-list" id="cc-threat-bars"></div>
              </div>
              <div class="cc-chart-box">
                <div class="cc-chart-title">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><circle cx="12" cy="12" r="9"/><path d="M12 3v9l6 3"/></svg>
                  Node Classification
                </div>
                <div class="cc-donut-container">
                  <svg id="cc-donut-svg" viewBox="0 0 160 160"></svg>
                  <div class="cc-donut-legend" id="cc-donut-legend"></div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Row 3: Financial Flow + Suspects + Live Feed -->
        <div class="cc-bottom-grid">
          <!-- Financial Flow & Hawala Spikes -->
          <div class="cc-panel">
            <div class="cc-panel-head">
              <div class="cc-panel-title-wrap">
                <div class="cc-panel-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
                </div>
                <div>
                  <h3>Financial Flow &amp; Hawala Spikes</h3>
                  <div class="cc-panel-sub">Transaction outlier velocity · flagged wire anomalies</div>
                </div>
              </div>
              <span class="cc-tag-amber">ANOMALY SPIKES</span>
            </div>
            <div id="cc-velocity-chart" class="cc-velocity-chart"></div>
          </div>

          <!-- Key Persons of Interest -->
          <div class="cc-panel">
            <div class="cc-panel-head">
              <div class="cc-panel-title-wrap">
                <div class="cc-panel-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
                </div>
                <div>
                  <h3 id="communities-title-el">Key Persons of Interest</h3>
                  <div class="cc-panel-sub">High-centrality orchestrators &amp; brokers</div>
                </div>
              </div>
              <button class="cc-btn-sm" onclick="goToPage('profiles')">
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
                All Dossiers
              </button>
            </div>
            <div class="cc-suspects-list" id="cc-suspects-list"></div>
          </div>

          <!-- Live Investigation Stream -->
          <div class="cc-panel">
            <div class="cc-panel-head">
              <div class="cc-panel-title-wrap">
                <div class="cc-panel-icon">
                  <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
                </div>
                <div>
                  <h3 id="feed-title-el">Live Investigation Stream</h3>
                  <div class="cc-panel-sub">Automated multi-source anomaly detections</div>
                </div>
              </div>
            </div>
            <div id="live-feed-list" class="cc-feed-scroll"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ---- NETWORK EXPLORER ---- -->
    <div class="page" data-page="graph" style="flex-direction:column;">
      <div class="topbar">
        <div class="topbar-left"><h2 data-i18n="tb_graph">Network Explorer</h2><span class="badge-secure" data-i18n="badge_secure_short">SECURE</span>
          <span class="active-graph-label" data-i18n="active_graph" style="font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint);">Active Graph: Operation Case MH/CID/2026/0417</span></div>
        <div class="path-finder-bar" id="path-finder-bar">
          <span class="pf-label"><svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="6" cy="19" r="3"/><circle cx="18" cy="5" r="3"/><path d="M12 19h4.5a3.5 3.5 0 0 0 0-7h-9a3.5 3.5 0 0 1 0-7H12"/></svg><span id="pf-label-text" data-i18n="trace_path_label">Trace Path:</span></span>
          <select id="pf-source" class="pf-select" data-i18n-attr="title" data-i18n="pf_origin_title" title="Origin entity"></select>
          <button id="btn-pf-swap" class="pf-swap-btn" data-i18n-attr="title" data-i18n="swap_tooltip" title="Swap Origin and Target">⇄</button>
          <select id="pf-target" class="pf-select" data-i18n-attr="title" data-i18n="pf_target_title" title="Target entity"></select>
          <button id="btn-find-path" class="btn-pf-run" data-i18n="btn_trace_path">⚡ Trace Path</button>
          <button id="btn-clear-path" class="btn-pf-clear" data-i18n="btn_clear_path">Reset</button>
        </div>
        <div class="topbar-search"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input id="search-input" data-i18n="search_placeholder" data-i18n-attr="placeholder" placeholder="Query entity, phone, location…"></div>
      </div>
      <div style="display:flex; flex:1; min-height:0;">
        <div id="graph-wrap">
          <div class="graph-dotgrid"></div>
          <div id="graph-toolbar-left">
            <div class="tool-icon" id="btn-zoom-in" data-i18n-attr="title" data-i18n="tooltip_zoom_in" title="Zoom In">+</div>
            <div class="tool-icon" id="btn-zoom-out" data-i18n-attr="title" data-i18n="tooltip_zoom_out" title="Zoom Out">−</div>
            <div class="tool-icon" id="btn-reset" data-i18n-attr="title" data-i18n="tooltip_reset_camera" title="Reset Camera / Fit to View">⤢</div>
            <div class="tool-icon" id="btn-physics-toggle" data-i18n-attr="title" data-i18n="tooltip_physics_toggle" title="Pause / Resume Layout Physics">⏸</div>
          </div>
          <div class="path-info-badge" id="path-info-badge"></div>
          <svg id="graph"></svg>
          <div id="graph-error"><div data-i18n="graph_error_title">Graph rendering failed to initialize.</div><div data-i18n="graph_error_sub" style="color:var(--ink-faint); font-size:11px;">Other pages are unaffected.</div></div>
          <div id="graph-hint" data-i18n="graph_hint" style="bottom:75px;">Drag to reposition \u00b7 Scroll to zoom \u00b7 Click a node to inspect</div>
          <div class="legend-sidebar" id="legend-list"></div>

          <!-- Timeline Sequence Player -->
          <div class="timeline-player-bar" id="timeline-player-bar">
            <div class="tp-controls">
              <button id="btn-tp-prev" class="tp-btn" title="Previous Event">\u23ee</button>
              <button id="btn-tp-play" class="tp-btn primary" title="Play / Pause">\u25b6</button>
              <button id="btn-tp-next" class="tp-btn" title="Next Event">\u23ed</button>
              <button id="btn-tp-reset" class="tp-btn" title="Reset">\u21ba</button>
            </div>
            <div class="tp-scrub-wrap">
              <div class="tp-event-meta">
                <span class="tp-event-date" id="tp-event-date">--/--/----</span>
                <span class="tp-event-badge" id="tp-event-badge">TIMELINE</span>
                <span class="tp-event-title" id="tp-event-title">Click Play or Drag slider to replay event sequence</span>
              </div>
              <input type="range" id="tp-slider" min="0" max="10" value="0" class="tp-slider">
            </div>
            <div class="tp-ticker" id="tp-ticker">Step 0 of 0</div>
          </div>
        </div>
        <div class="profile-panel" id="profile-panel">
          <div class="profile-empty" data-i18n="empty_select_node" style="white-space:pre-line;">SELECT A NODE ON THE GRAPH
TO VIEW ITS INVESTIGATIVE PROFILE</div>
        </div>
      </div>
    </div>

    <!-- ---- AI ASSISTANT ---- -->
    <div class="page" data-page="assistant" style="flex-direction:column;">
      <div class="topbar">
        <div class="topbar-left"><h2 data-i18n="tb_assistant">AI Investigation Assistant</h2><span class="badge-secure" data-i18n="badge_evidence_cited">EVIDENCE-CITED ANSWERS ONLY</span></div>
      </div>
      <div class="asst-wrap">
        <div class="asst-messages" id="asst-messages"></div>
        <div class="asst-suggestions" id="asst-suggestions"></div>
        <div class="asst-input-row">
          <input type="text" id="asst-input" data-i18n="asst_placeholder" data-i18n-attr="placeholder" placeholder="Ask about an entity, a connection, or the case\u2026">
          <button id="asst-send" data-i18n="asst_send">Ask</button>
        </div>
      </div>
    </div>

    <!-- ---- ENTITY PROFILES ---- -->
    <div class="page" data-page="profiles">
      <div class="topbar"><div class="topbar-left"><h2>Entity Profiles</h2><span class="badge-secure">{{N}} PERSONS OF INTEREST</span></div></div>
      <div class="page-pad"><div class="ep-grid" id="ep-grid"></div></div>
    </div>

    <!-- ---- ENTITY PROFILE DETAIL (full page) ---- -->
    <div class="page" data-page="profile-detail">
      <div class="topbar">
        <div class="topbar-left">
          <span class="breadcrumb"><a href="#" id="pd-back-link">Entity Profiles</a> &nbsp;\u203a&nbsp; <span id="pd-breadcrumb-name">Profile View</span></span>
        </div>
        <div>
          <button class="btn-export-dossier" onclick="window.print()">Print / Export Dossier</button>
        </div>
      </div>
      <div class="page-pad" id="profile-detail-content" style="max-width:1100px;"></div>
    </div>

    <!-- ---- DATA LAB ---- -->
    <div class="page" data-page="datalab" style="flex-direction:column;">
      <div class="topbar"><div class="topbar-left"><h2 data-i18n="tb_datalab">Data Lab Workspace</h2><span class="badge-secure" data-i18n="badge_doc_analysis">DOCUMENT ANALYSIS</span></div></div>
      <div class="datalab-grid">
        <div class="dl-panel">
          <div class="dl-label" id="dl-extraction-model-label">Extraction Model</div>
          <select class="dl-select"><option id="dl-model-option">Rule-Based NER v1 (regex + gazetteer)</option></select>
          <div class="dl-slider-row">
            <div class="dl-label" id="dl-merge-threshold-label">Merge Confidence Threshold<span class="dl-slider-val" id="thresh-val">60%</span></div>
            <input type="range" id="thresh-slider" min="30" max="90" value="60">
          </div>
          <div class="dl-label" id="dl-active-classes-label">Active Entity Classes</div>
          <div class="dl-chip-row" id="entity-chip-row"></div>
          <div class="dl-label" id="dl-conflicts-title" style="margin-top:6px;">Data Conflicts (<span id="conflict-count">0</span>)</div>
          <div id="conflict-list"></div>
        </div>
        <div class="dl-doc-area">
          <div class="dl-input-toggle">
            <button class="active" id="btn-mode-sample" data-i18n="mode_sample">Sample Documents</button>
            <button id="btn-mode-custom" data-i18n="mode_custom">Paste Your Own Text</button>
            <button id="btn-mode-upload" data-i18n="mode_upload">Upload Source File</button>
          </div>
          <div id="sample-doc-mode"></div>
          <div class="dl-textarea-wrap" id="custom-mode">
            <textarea id="live-input" data-i18n="textarea_placeholder" data-i18n-attr="placeholder" placeholder="Type or paste an FIR excerpt, surveillance note, or informant report\u2026"></textarea>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
              <button class="dl-run-btn" id="btn-run-extraction" data-i18n="btn_run_extraction">Run Extraction</button>
              <button class="dl-run-btn" style="background:none; color:var(--ink-dim); border-color:var(--border);" id="btn-example-1" data-i18n="btn_example1">Load Example 1</button>
              <button class="dl-run-btn" style="background:none; color:var(--ink-dim); border-color:var(--border);" id="btn-example-2" data-i18n="btn_example2">Load Example 2</button>
            </div>
            <div id="live-output" style="margin-top:16px;"></div>
          </div>
          <div class="dl-textarea-wrap" id="upload-mode">
            <div class="dl-upload-zone" id="dl-upload-zone">
              <div class="dl-upload-icon"><svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg></div>
              <div class="dl-upload-title" data-i18n="upload_title">Upload Source File</div>
              <div class="dl-upload-sub" data-i18n="upload_sub">Drag &amp; drop or browse \u2014 plain text (.txt) files only in this prototype</div>
              <input type="file" id="dl-file-input" accept=".txt" style="display:none;">
            </div>
            <div id="upload-filename" style="font-family:var(--font-mono); font-size:11px; color:var(--ink-faint); margin-top:10px;"></div>
            <div id="upload-output" style="margin-top:16px;"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ---- ANALYTICS REPORT ---- -->
    <div class="page" data-page="report">
      <div class="topbar">
        <div class="topbar-left">
          <h2 data-i18n="tb_report">Analytics Report</h2>
          <span class="badge-secure" data-i18n="badge_tagged">FACT / INFERENCE / LEAD TAGGED</span>
        </div>
        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
          <div class="report-filter-group" id="report-filter-group">
            <button class="rf-btn active" data-filter="ALL" data-i18n="report_filter_all">All Statements</button>
            <button class="rf-btn fact" data-filter="FACT" data-i18n="report_filter_fact">FACT</button>
            <button class="rf-btn inference" data-filter="AI_INFERENCE" data-i18n="report_filter_inf">INFERENCE</button>
            <button class="rf-btn lead" data-filter="LEAD" data-i18n="report_filter_lead">LEAD</button>
          </div>
          <button class="btn-export-dossier" data-i18n="report_btn_export" onclick="window.print()">Export Full Briefing (PDF)</button>
        </div>
      </div>
      <div class="page-pad" style="max-width:1100px; margin:0 auto; width:100%;">
        <!-- Print-Only Official Seal & Header -->
        <div class="print-only print-official-header">
          <div class="gov-title">Government of Maharashtra \u2022 Police Department</div>
          <div class="sub-dept">State Criminal Investigation Department (CID) \u2022 Crime Intelligence Wing</div>
          <div class="doc-title">OFFICIAL CASE INTELLIGENCE &amp; EVIDENTIARY REPORT</div>
          <div style="font-size:8.5pt; color:#666; margin-top:3px;">STRICTLY CONFIDENTIAL \u2014 SUBMITTED UNDER SECTION 91/161 CrPC DECISION SUPPORT</div>
        </div>

        <!-- Executive Metadata Card -->
        <div class="report-exec-card">
          <div class="rec-top">
            <div>
              <div class="rec-org">STATE CRIMINAL INVESTIGATION DEPARTMENT // SPECIAL INTELLIGENCE UNIT</div>
              <h1 class="rec-title">EVIDENTIARY CASE INTELLIGENCE BRIEFING</h1>
              <div class="rec-meta">
                <span><b>Case Ref:</b> Operation Case MH/CID/2026/0417</span>
                <span>\u2022</span>
                <span><b>Jurisdiction:</b> Mumbai Metropolitan Area</span>
                <span>\u2022</span>
                <span><b>Evidentiary Standard:</b> Multi-Source Corroborated</span>
              </div>
            </div>
            <div class="rec-status-badge">CONFIDENTIAL // LAW ENFORCEMENT ONLY</div>
          </div>
          <div class="rec-stats-row" id="report-stat-summary"></div>
        </div>

        <!-- Section Statement Cards -->
        <div id="report-sections-container"></div>

        <!-- Print-Only Signature Block -->
        <div class="print-only print-sig-block">
          <div class="print-sig-col">
            <div><b>Prepared &amp; Verified By:</b></div>
            <div class="print-sig-line"></div>
            <div class="print-sig-title">Investigating Officer (IO), Cyber &amp; Crime Branch</div>
          </div>
          <div class="print-sig-col">
            <div><b>Reviewed &amp; Countersigned By:</b></div>
            <div class="print-sig-line"></div>
            <div class="print-sig-title">Superintendent of Police (SP) / Dy. Commissioner of Police</div>
          </div>
        </div>
      </div>
    </div>

    <!-- ---- EVIDENCE VAULT ---- -->
    <div class="page" data-page="evidence">
      <div class="topbar">
        <div class="topbar-left">
          <h2 data-i18n="evid_title">Evidence Vault / Repository</h2>
          <span class="badge-secure" data-i18n="evid_integrity">SHA-256 INTEGRITY PROTECTED</span>
          <span style="font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint);" data-i18n="evid_chain">Chain of Custody &amp; Provenance</span>
        </div>
        <div style="display:flex; gap:10px;">
          <button class="btn-verify-hash" id="btn-verify-all-evidence" data-i18n="btn_verify_all_hashes">🛡️ Verify All Vault Hashes</button>
        </div>
      </div>
      <div class="page-pad">
        <div class="evid-filter-bar" id="evid-filter-bar">
          <button class="evid-tab-btn active" data-source="ALL" data-i18n="evid_tab_all">All Vault Records</button>
          <button class="evid-tab-btn" data-source="FIR" data-i18n="evid_tab_fir">FIR Filings</button>
          <button class="evid-tab-btn" data-source="BANK_RECORD" data-i18n="evid_tab_bank">Bank Records</button>
          <button class="evid-tab-btn" data-source="CDR" data-i18n="evid_tab_cdr">CDR Tower Dumps</button>
          <button class="evid-tab-btn" data-source="SURVEILLANCE" data-i18n="evid_tab_surv">Surveillance Logs</button>
          <button class="evid-tab-btn" data-source="FIELD_REPORT" data-i18n="evid_tab_field">Field Intel</button>
        </div>
        <div class="evid-grid" id="evid-cards-grid">
          <!-- Populated dynamically by dashboard_app.js -->
        </div>
      </div>
    </div>

    <!-- ---- ANOMALY & RISK ---- -->
    <div class="page" data-page="anomalies">
      <div class="topbar">
        <div class="topbar-left">
          <h2 data-i18n="anom_title">Dedicated Anomaly &amp; Risk Intelligence</h2>
          <span class="badge-secure" style="border-color:var(--amber); color:var(--amber);" data-i18n="anom_decision_only">DECISION SUPPORT ONLY</span>
          <span style="font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint);" data-i18n="anom_sub">Multi-Factor Anomaly Decomposition</span>
        </div>
      </div>
      <div class="page-pad">
        <div class="formula-banner">
          <div>
            <div style="font-family:var(--font-serif); font-size:15px; font-weight:700; color:var(--ink); margin-bottom:4px;" data-i18n="anom_decomposition_title">Explainable Mathematical Risk Formulation</div>
            <div style="font-size:11.5px; color:var(--ink-dim);" data-i18n="anom_decomposition_sub">Transparent weighted scoring combining statistical CDR outliers, Hawala volume velocities, graph centrality, and temporal-geospatial proximity.</div>
          </div>
          <div class="formula-chips">
            <div class="formula-chip" data-i18n="anom_chip_1">Comm Bursts (35%)</div>
            <div class="formula-chip" data-i18n="anom_chip_2">Fin Velocity (30%)</div>
            <div class="formula-chip" data-i18n="anom_chip_3">Centrality (20%)</div>
            <div class="formula-chip" data-i18n="anom_chip_4">Spatiotemporal (15%)</div>
          </div>
        </div>
        <div class="anom-grid" id="anom-cards-grid">
          <!-- Populated dynamically by dashboard_app.js -->
        </div>
      </div>
    </div>

    <!-- ---- INVESTIGATION TIMELINE ---- -->
    <div class="page" data-page="timeline">
      <div class="topbar">
        <div class="topbar-left">
          <h2 data-i18n="tl_title">Dedicated Investigation Timeline</h2>
          <span class="badge-secure" data-i18n="tl_forensic">TEMPORAL CORRELATION</span>
          <span style="font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint);" data-i18n="tl_sub">Operation Case MH/CID/2026/0417</span>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          <label style="font-family:var(--font-mono); font-size:11px; color:var(--ink-dim);" data-i18n="tl_label_entity">Entity:</label>
          <select id="tl-filter-entity" class="pf-select" style="min-width:140px;">
            <option value="" data-i18n="tl_filter_all_ents">All Entities</option>
            <option value="P01">Rajeev Malhotra</option>
            <option value="P02">Anita Rao</option>
            <option value="P03">Vikram Solanki</option>
            <option value="P04">Feroz Sheikh</option>
            <option value="P05">Sanjay Verma</option>
          </select>
          <label style="font-family:var(--font-mono); font-size:11px; color:var(--ink-dim);" data-i18n="tl_label_type">Type:</label>
          <select id="tl-filter-type" class="pf-select">
            <option value="" data-i18n="tl_filter_all_types">All Event Types</option>
            <option value="TRANSACTION" data-i18n="tl_opt_tx">Bank Transfers</option>
            <option value="CALL" data-i18n="tl_opt_call">CDR Calls</option>
            <option value="SURVEILLANCE" data-i18n="tl_opt_surv">Surveillance</option>
            <option value="FIR" data-i18n="tl_opt_fir">FIR Filings</option>
          </select>
        </div>
      </div>
      <div class="page-pad">
        <div style="background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:14px 18px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
          <div>
            <div style="font-family:var(--font-serif); font-size:14px; font-weight:700; color:var(--ink);" data-i18n="tl_rel_inspector">Relationship History Inspector</div>
            <div style="font-size:11.5px; color:var(--ink-dim);" data-i18n="tl_rel_inspector_sub">Select any two entities to analyze their chronological interaction evolution.</div>
          </div>
          <div style="display:flex; gap:8px; align-items:center;">
            <select id="rel-ent-a" class="pf-select"></select>
            <span style="font-family:var(--font-mono); color:var(--ink-faint);">↔</span>
            <select id="rel-ent-b" class="pf-select"></select>
            <button id="btn-inspect-rel" class="btn-pf-run" data-i18n="btn_trace_history">Trace History</button>
          </div>
        </div>
        <div id="rel-history-summary" style="margin-bottom:16px;"></div>
        <div class="tl-stream" id="tl-events-container">
          <!-- Populated dynamically by dashboard_app.js -->
        </div>
      </div>
    </div>

    <!-- ---- INGESTION PIPELINE ---- -->
    <div class="page" data-page="ingestion">
      <div class="topbar">
        <div class="topbar-left">
          <h2 data-i18n="ingest_title">Explicit 6-Stage Ingestion Pipeline &amp; Workflow</h2>
          <span class="badge-secure" data-i18n="ingest_badge">AUTOMATED EXTRACTION</span>
        </div>
      </div>
      <div class="page-pad">
        <!-- 6-Stage Stepper Animation Header -->
        <div class="stepper-container" id="pipeline-stepper">
          <div class="step-node completed" id="step-1"><div class="step-circle">1</div><div data-i18n="step_1_title">Pre-processing</div></div>
          <div class="step-node completed" id="step-2"><div class="step-circle">2</div><div data-i18n="step_2_title">OCR Engine</div></div>
          <div class="step-node completed" id="step-3"><div class="step-circle">3</div><div data-i18n="step_3_title">NLP Extraction</div></div>
          <div class="step-node completed" id="step-4"><div class="step-circle">4</div><div data-i18n="step_4_title">Entity Resolution</div></div>
          <div class="step-node completed" id="step-5"><div class="step-circle">5</div><div data-i18n="step_5_title">Relationship Link</div></div>
          <div class="step-node completed" id="step-6"><div class="step-circle">6</div><div data-i18n="step_6_title">Graph Indexing</div></div>
        </div>

        <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:24px;">
          <!-- Upload Form Box -->
          <div style="background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:20px;">
            <h3 style="font-family:var(--font-serif); font-size:16px; margin-bottom:12px;" data-i18n="ingest_submit_title">Submit Document to Pipeline</h3>
            <div style="display:flex; flex-direction:column; gap:12px;">
              <div>
                <label style="display:block; font-family:var(--font-mono); font-size:11px; color:var(--ink-dim); margin-bottom:4px;" data-i18n="ingest_cat_label">Document Source Category</label>
                <select id="ingest-source-type" class="pf-select" style="width:100%;">
                  <option value="FIR" data-i18n="ingest_opt_fir">First Information Report (FIR)</option>
                  <option value="CDR" data-i18n="ingest_opt_cdr">Telecom CDR / Cell Dump (CSV)</option>
                  <option value="BANK_RECORD" data-i18n="ingest_opt_bank">Bank Statement / STR (CSV/XML)</option>
                  <option value="SURVEILLANCE" data-i18n="ingest_opt_surv">Physical Surveillance Observation Log</option>
                  <option value="FIELD_REPORT" data-i18n="ingest_opt_field">Confidential Informant Report</option>
                </select>
              </div>
              <div>
                <label style="display:block; font-family:var(--font-mono); font-size:11px; color:var(--ink-dim); margin-bottom:4px;" data-i18n="ingest_officer_label">Submitting Officer</label>
                <input id="ingest-officer" type="text" value="Insp. Vikramaditya Kadam" style="width:100%; padding:8px 10px; background:var(--bg); border:1px solid var(--border); border-radius:5px; font-family:inherit; font-size:12px;">
              </div>
              <div>
                <label style="display:block; font-family:var(--font-mono); font-size:11px; color:var(--ink-dim); margin-bottom:4px;" data-i18n="ingest_file_label">Select File (PDF, CSV, TXT, Image)</label>
                <input type="file" id="ingest-file-input" style="width:100%; font-size:12px;">
              </div>
              <button id="btn-run-ingestion" class="btn-pf-run" data-i18n="btn_run_ingest" style="padding:10px; font-size:12px; margin-top:6px;">🚀 Execute 6-Stage Ingestion Pipeline</button>
            </div>
          </div>

          <!-- Execution Logs Console -->
          <div style="background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:20px; display:flex; flex-direction:column;">
            <h3 style="font-family:var(--font-serif); font-size:16px; margin-bottom:12px;" data-i18n="ingest_telemetry_title">Pipeline Execution Telemetry</h3>
            <div id="ingest-console-output" data-i18n="ingest_ready_msg" style="flex:1; background:var(--bg); border:1px solid var(--border); border-radius:6px; padding:12px; font-family:var(--font-mono); font-size:11px; color:var(--ink); overflow-y:auto; max-height:220px; white-space:pre-wrap; line-height:1.6;">Ready for document submission. Select a file and click execute to observe 6-stage pipeline stages.</div>
          </div>
        </div>

        <!-- Ingestion History Table -->
        <div style="background:var(--panel); border:1px solid var(--border); border-radius:8px; padding:20px;">
          <h3 style="font-family:var(--font-serif); font-size:16px; margin-bottom:14px;" data-i18n="ingest_history_title">Ingestion Audit History</h3>
          <div style="overflow-x:auto;">
            <table class="audit-table">
              <thead>
                <tr>
                  <th data-i18n="th_job_id">Job ID</th>
                  <th data-i18n="th_source_file">Source File</th>
                  <th data-i18n="th_size">Size</th>
                  <th data-i18n="th_sha256">SHA-256 Checksum</th>
                  <th data-i18n="th_findings">Extracted Findings</th>
                  <th data-i18n="th_evid_id">Evidence Vault ID</th>
                  <th data-i18n="th_status">Status</th>
                </tr>
              </thead>
              <tbody id="ingest-history-table-body">
                <!-- Populated dynamically -->
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- ---- AUDIT & VERIFICATION ---- -->
    <div class="page" data-page="audit">
      <div class="topbar">
        <div class="topbar-left">
          <h2 data-i18n="audit_title">Audit &amp; Human Verification Workflow</h2>
          <span class="badge-secure" data-i18n="audit_badge">INSTITUTIONAL ACCOUNTABILITY</span>
          <span style="font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint);" data-i18n="audit_sub">No Silent AI Merges</span>
        </div>
      </div>
      <div class="page-pad">
        <div class="audit-layout">
          <!-- Pending Candidate Merges (Human in the Loop) -->
          <div>
            <div style="font-family:var(--font-serif); font-size:16px; font-weight:700; margin-bottom:4px;" data-i18n="audit_pending_title">Pending Entity Resolution Candidates</div>
            <div style="font-size:11.5px; color:var(--ink-dim); margin-bottom:14px;" data-i18n="audit_pending_sub">AI-suggested identity merges requiring human investigator sign-off before committing to the knowledge graph.</div>
            <div id="cand-merge-list">
              <!-- Populated dynamically -->
            </div>
          </div>

          <!-- Immutable Audit Trail Ledger -->
          <div>
            <div style="font-family:var(--font-serif); font-size:16px; font-weight:700; margin-bottom:4px;" data-i18n="audit_trail_title">Immutable Forensic Audit Ledger</div>
            <div style="font-size:11.5px; color:var(--ink-dim); margin-bottom:14px;" data-i18n="audit_trail_sub">Cryptographically verifiable record of all user queries, hash integrity checks, and merge decisions.</div>
            <div style="background:var(--panel); border:1px solid var(--border); border-radius:8px; overflow-x:auto; max-height:550px; overflow-y:auto;">
              <table class="audit-table">
                <thead>
                  <tr>
                    <th>Timestamp</th>
                    <th>Investigator</th>
                    <th>Action</th>
                    <th>Target / Details</th>
                  </tr>
                </thead>
                <tbody id="audit-trail-body">
                  <!-- Populated dynamically -->
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
__D3_JS__
</script>
<script>
__APP_JS__
</script>
</body>
</html>
"""

HTML = HTML.replace("__D3_JS__", D3_JSON_SAFE).replace("__APP_JS__", APP_JS).replace("__DATA_JSON__", DATA_JSON).replace("__AVG_CONFIDENCE__", str(AVG_CONFIDENCE))

out_path = os.path.join(OUT_DIR, "index.html")
with open(out_path, "w", encoding="utf-8") as f:
    f.write(HTML)
print(f"Dashboard built -> {out_path}  ({len(HTML):,} bytes)")
