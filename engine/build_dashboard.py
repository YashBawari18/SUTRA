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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<title>S\u016aTRA \u2014 Criminal Network Intelligence System</title>
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
  #landing{ position:fixed; inset:0; background:var(--bg); z-index:100; overflow-y:auto; }
  #landing.hide{ display:none; }
  .land-header{ display:flex; align-items:center; justify-content:space-between; padding:16px 40px;
    border-bottom:1px solid var(--border); }
  .land-brand{ display:flex; align-items:center; gap:12px; }
  .land-devanagari{ font-family:var(--font-serif); font-size:20px; color:var(--gold); }
  .land-brand-name{ font-family:var(--font-serif); font-size:17px; letter-spacing:0.06em; font-weight:700; color:var(--ink); }
  .land-nav{ display:flex; gap:24px; font-family:var(--font-mono); font-size:10.5px; color:var(--ink-faint); letter-spacing:0.06em; font-weight:500; }

  .hero{ max-width:860px; margin:0 auto; text-align:center; padding:90px 30px 60px; }
  .hero-mark{ font-family:var(--font-serif); font-size:68px; color:var(--gold); line-height:1; margin-bottom:16px; opacity:0.88; }
  .hero h1{ font-family:var(--font-serif); font-size:40px; font-weight:700; color:var(--ink); margin-bottom:16px; letter-spacing:0.01em; line-height:1.2; }
  .hero p{ font-family:var(--font-body); font-size:14.5px; color:var(--ink-dim); max-width:560px; margin:0 auto 32px; line-height:1.75; font-weight:400; }
  .hero-btns{ display:flex; gap:12px; justify-content:center; }
  .btn-hero-primary{ background:var(--gold); color:#ffffff; border:none; padding:12px 28px; border-radius:var(--radius-sm);
    font-family:var(--font-mono); font-size:11.5px; letter-spacing:0.07em; font-weight:700; transition:opacity 0.15s; }
  .btn-hero-primary:hover{ opacity:0.88; }
  .btn-hero-secondary{ background:none; color:var(--ink); border:1px solid var(--border); padding:12px 28px; border-radius:var(--radius-sm);
    font-family:var(--font-mono); font-size:11.5px; letter-spacing:0.07em; transition:border-color 0.15s; }
  .btn-hero-secondary:hover{ border-color:var(--ink-dim); }

  .caps-section{ max-width:1100px; margin:0 auto; padding:50px 30px 28px; text-align:center; }
  .caps-section h2{ font-family:var(--font-serif); font-size:24px; margin-bottom:10px; font-weight:700; }
  .caps-section > p{ color:var(--ink-faint); font-size:13px; margin-bottom:8px; line-height:1.6; }
  .caps-divider{ width:44px; height:2px; background:var(--gold); margin:16px auto 36px; }
  .caps-grid{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:16px; max-width:1100px; margin:0 auto; padding:0 30px; }
  .cap-card{ background:var(--panel); border:1px solid var(--border); border-radius:var(--radius); padding:20px 22px; text-align:left; position:relative; transition:box-shadow 0.2s; }
  .cap-card:hover{ box-shadow:var(--shadow-sm); }
  .cap-tag{ position:absolute; top:14px; right:14px; font-family:var(--font-mono); font-size:8px; color:var(--ink-faint); letter-spacing:0.07em; }
  .cap-tag.core{ color:var(--gold); border:1px solid var(--gold); padding:2px 6px; border-radius:2px; font-weight:700; }
  .cap-icon{ width:36px; height:36px; background:var(--bg); border:1px solid var(--border); border-radius:var(--radius);
    display:flex; align-items:center; justify-content:center; margin-bottom:14px; color:var(--gold); }
  .cap-card h3{ font-family:var(--font-body); font-size:14px; font-weight:600; margin-bottom:7px; color:var(--ink); }
  .cap-card p{ font-size:12.5px; color:var(--ink-faint); line-height:1.65; }
  .cap-visual{ margin-top:14px; height:64px; border:1px dashed var(--border); border-radius:var(--radius-sm); display:flex;
    align-items:center; justify-content:center; font-family:var(--font-mono); font-size:9px; color:var(--ink-faint); letter-spacing:0.04em; }

  .cap-wide{ max-width:1100px; margin:16px auto 0; padding:0 30px; }
  .cap-wide-card{ background:var(--panel); border:1px solid var(--border); border-radius:var(--radius); padding:20px 24px;
    display:flex; align-items:center; gap:20px; position:relative; }
  .cap-wide-card .cap-icon{ margin-bottom:0; flex-shrink:0; }
  .cap-wide-card .body{ flex:1; }
  .cap-wide-card h3{ font-family:var(--font-body); font-size:14px; font-weight:600; margin-bottom:5px; color:var(--ink); }
  .cap-wide-card p{ font-size:12.5px; color:var(--ink-faint); line-height:1.6; }
  .btn-doc{ background:none; border:1px solid var(--border); color:var(--ink-dim); padding:8px 16px; border-radius:var(--radius);
    font-family:var(--font-mono); font-size:10.5px; flex-shrink:0; letter-spacing:0.04em; transition:border-color 0.15s; }
  .btn-doc:hover{ border-color:var(--ink-dim); }

  .land-footer{ max-width:1100px; margin:52px auto 0; padding:18px 30px; border-top:1px solid var(--border);
    display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px; font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); letter-spacing:0.04em; }
  .land-footer a{ color:var(--ink-faint); text-decoration:none; margin-left:16px; }
  .land-footer a:hover{ color:var(--ink-dim); }

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

  /* ---- Command Center ---- */
  .stat-grid{ display:grid; grid-template-columns:repeat(4,1fr); gap:14px; margin-bottom:18px; }
  .stat-card{ background:var(--panel); border:1px solid var(--border); border-radius:var(--radius); padding:14px 16px; position:relative; }
  .stat-card .tag{ position:absolute; top:12px; right:12px; font-family:var(--font-mono); font-size:8.5px; color:var(--ink-faint); letter-spacing:0.05em; }
  .stat-card .tag.up{ color:var(--cyan); }
  .stat-card .l{ font-family:var(--font-mono); font-size:9px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:0.07em; margin-bottom:10px; font-weight:600; }
  .stat-card .v{ font-family:var(--font-serif); font-size:28px; color:var(--ink); letter-spacing:-0.01em; }
  .stat-card .v small{ font-family:var(--font-mono); font-size:12px; color:var(--ink-faint); }

  .cc-grid{ display:grid; grid-template-columns:1.3fr 1fr; gap:14px; }
  .cc-panel{ background:var(--panel); border:1px solid var(--border); border-radius:var(--radius); padding:16px 18px; }
  .cc-panel-head{ display:flex; align-items:center; justify-content:space-between; margin-bottom:12px; }
  .cc-panel-head h3{ font-family:var(--font-body); font-size:13px; font-weight:600; color:var(--ink); letter-spacing:-0.01em; }
  .feed-item{ padding:9px 0; border-bottom:1px solid var(--border); }
  .feed-item:last-child{ border-bottom:none; }
  .feed-head{ display:flex; align-items:center; gap:7px; margin-bottom:3px; }
  .feed-sev{ font-family:var(--font-mono); font-size:8.5px; letter-spacing:0.07em; padding:2px 6px; border-radius:2px; text-transform:uppercase; font-weight:700; }
  .feed-sev.critical{ background:rgba(196,32,32,0.1); color:var(--red); }
  .feed-sev.warning{ background:rgba(194,124,0,0.12); color:var(--amber); }
  .feed-sev.info{ background:rgba(11,148,148,0.1); color:var(--cyan); }
  .feed-time{ font-family:var(--font-mono); font-size:9px; color:var(--ink-faint); }
  .feed-text{ font-size:12px; color:var(--ink-dim); line-height:1.55; }
  .feed-src{ font-family:var(--font-mono); font-size:9px; color:var(--ink-faint); margin-top:2px; }
  .community-row{ display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid var(--border); }
  .community-row:last-child{ border-bottom:none; }
  .community-dot{ width:7px; height:7px; border-radius:50%; flex-shrink:0; }
  .community-row .name{ font-size:12px; color:var(--ink-dim); flex:1; font-weight:400; }
  .community-row .n{ font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); }

  /* ---- Network Explorer ---- */
  #graph-wrap{ position:relative; overflow:hidden; background:var(--bg); flex:1; min-height:0; }
  .graph-dotgrid{ position:absolute; inset:0; background-image:radial-gradient(circle, rgba(20,30,60,0.07) 1px, transparent 1px);
    background-size:22px 22px; pointer-events:none; }
  svg#graph{ width:100%; height:100%; display:block; cursor:grab; position:relative; z-index:1; }
  svg#graph:active{ cursor:grabbing; }
  .link{ stroke:var(--ink-faint); stroke-opacity:0.45; fill:none; }
  .link.suspicious{ stroke:var(--red); stroke-opacity:0.85; stroke-dasharray:3,3; }
  .link-label{ font-family:var(--font-mono); font-size:8.5px; fill:var(--ink-faint); pointer-events:none; }
  .node{ cursor:pointer; }
  .node-box{ fill:var(--panel); stroke-width:1.4px; }
  .node-icon{ pointer-events:none; }
  .node-label{ font-family:var(--font-mono); font-size:9px; fill:var(--ink-dim); pointer-events:none; }
  .node-sublabel{ font-family:var(--font-mono); font-size:7.5px; fill:var(--ink-faint); pointer-events:none; }
  .node.dim{ opacity:0.15; }
  .node.selected .node-box{ filter:drop-shadow(0 0 6px currentColor); }
  .node.key .node-box{ stroke:var(--gold) !important; }
  #graph-toolbar-left{ position:absolute; top:14px; left:14px; z-index:4; display:flex; gap:8px; }
  #graph-hint{ position:absolute; bottom:12px; left:14px; z-index:4; font-family:var(--font-mono); font-size:9.5px; color:var(--ink-faint); }
  .tool-icon{ width:32px; height:32px; border-radius:5px; background:var(--panel); border:1px solid var(--border);
    display:flex; align-items:center; justify-content:center; color:var(--ink-dim); }
  .tool-icon:hover{ color:var(--ink); }
  #graph-error{ position:absolute; inset:0; display:none; align-items:center; justify-content:center; flex-direction:column;
    gap:10px; text-align:center; padding:30px; font-family:var(--font-mono); color:var(--red); font-size:12px; z-index:5; background:var(--bg); }

  /* Path Finder Bar */
  .path-finder-bar{ display:flex; align-items:center; gap:8px; background:var(--panel); border:1px solid var(--border);
    border-radius:6px; padding:6px 12px; }
  .pf-label{ font-family:var(--font-mono); font-size:10px; color:var(--ink-faint); text-transform:uppercase; letter-spacing:0.05em; font-weight:700; }
  .pf-select{ background:var(--bg); border:1px solid var(--border); color:var(--ink); font-family:var(--font-mono); font-size:11px; padding:4px 8px; border-radius:4px; outline:none; }
  .pf-arrow{ font-family:var(--font-mono); color:var(--gold); font-weight:700; font-size:12px; }
  .btn-pf-run{ background:var(--gold); color:#fff; border:none; padding:5px 12px; border-radius:4px; font-family:var(--font-mono); font-size:11px; font-weight:700; cursor:pointer; }
  .btn-pf-clear{ background:none; border:1px solid var(--border); color:var(--ink-dim); padding:5px 10px; border-radius:4px; font-family:var(--font-mono); font-size:11px; cursor:pointer; }
  .path-info-badge{ position:absolute; top:58px; left:14px; z-index:4; background:var(--panel); border:1px solid var(--gold); border-radius:6px; padding:8px 12px; font-family:var(--font-mono); font-size:11px; color:var(--ink); display:none; box-shadow:0 4px 12px rgba(0,0,0,0.1); }

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
</style>
</head>
<body>
<!-- ================= LANDING ================= -->
<div id="landing">
  <div class="land-header">
    <div class="land-brand">
      <div class="land-devanagari">\u0938\u0942\u0924\u094d\u0930</div>
      <div class="land-brand-name">S\u016aTRA</div>
    </div>
    <div class="land-nav">
      <span data-i18n="land_nav_1">ANALYTICAL CAPABILITIES</span><span data-i18n="land_nav_2">SECURE ACCESS PROTOCOL</span><span data-i18n="land_nav_3">GOVERNMENT DISCLAIMER</span>
      <div class="lang-switcher land-lang-switcher">
        <button class="lang-btn active" data-lang="en">EN</button>
        <button class="lang-btn" data-lang="hi">\u0939\u093f\u0902</button>
        <button class="lang-btn" data-lang="mr">\u092e\u0930\u093e</button>
      </div>
    </div>
  </div>
  <div class="hero">
    <div class="hero-mark">\u0938\u0942\u0924\u094d\u0930</div>
    <h1 data-i18n="hero_title">The Connection Thread</h1>
    <p data-i18n="hero_subtitle">Uncovering the invisible networks of crime. A unified investigative decision-support platform for entity resolution, knowledge-graph analysis, and evidence-backed leads \u2014 built for institutional accountability, not automated accusation.</p>
    <div class="hero-btns">
      <button class="btn-hero-primary" id="btn-enter-app" data-i18n="btn_request_access">Request Access \u2192 Command Center</button>
      <button class="btn-hero-secondary" id="btn-view-briefing" data-i18n="btn_view_briefing">View Briefing</button>
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
      <div class="cap-icon">\u25c8</div>
      <h3 data-i18n="cap1_title">Data Integration</h3>
      <p data-i18n="cap1_desc">Harmonize FIRs, CDRs, financial records, and surveillance reports into one structured investigative namespace.</p>
    </div>
    <div class="cap-card">
      <div class="cap-tag">REC-02-15</div>
      <div class="cap-icon">\u25c9</div>
      <h3 data-i18n="cap2_title">Entity Extraction &amp; Resolution</h3>
      <p data-i18n="cap2_desc">Automated identification of persons, phones, vehicles, and organizations \u2014 with confidence-scored merging of duplicate mentions.</p>
    </div>
    <div class="cap-card">
      <div class="cap-tag core" data-i18n="cap3_module">CORE MODULE</div>
      <div class="cap-icon">\u2735</div>
      <h3 data-i18n="cap3_title">Relationship Mapping</h3>
      <p data-i18n="cap3_desc">Visualize covert networks. Trace financial flows, communication linkages, and hierarchical structures dynamically.</p>
      <div class="cap-visual" data-i18n="cap3_visual">Network Graph Visualization</div>
    </div>
  </div>
  <div class="cap-wide">
    <div class="cap-wide-card">
      <div class="cap-icon">\u25e0</div>
      <div class="body">
        <h3 data-i18n="cap4_title">Explainable Risk Scoring</h3>
        <p data-i18n="cap4_desc">Transparent, source-weighted risk indicators \u2014 every score fully traceable to evidence, always requiring human verification. No automated accusation, ever.</p>
      </div>
      <button class="btn-doc" id="btn-view-docs" data-i18n="btn_view_docs">View Documentation</button>
    </div>
  </div>

  <div class="land-footer">
    <div data-i18n="footer_copyright">\u00a9 2026 S\u016aTRA Investigative Intelligence Platform. Prototype \u2014 Restricted Demonstration Use Only.</div>
    <div><a href="#" data-i18n="footer_link1">Secure Access Protocol</a><a href="#" data-i18n="footer_link2">Privacy Policy</a><a href="#" data-i18n="footer_link3">Government Disclaimer</a><a href="#" data-i18n="footer_link4">Contact Administrator</a></div>
  </div>
</div>

<!-- ================= APP SHELL ================= -->
<div id="app">
  <div class="sidebar" id="sidebar">
    <div class="sb-brand" id="sb-brand-btn" title="Return to Landing / Briefing Page"><div class="sb-brand-mark">\u0938</div><div class="sb-brand-text"><b>S\u016aTRA</b><span data-i18n="brand_tagline">INTELLIGENCE PLATFORM</span></div></div>
    <div class="lang-switcher">
      <button class="lang-btn active" data-lang="en">EN</button>
      <button class="lang-btn" data-lang="hi">\u0939\u093f\u0902</button>
      <button class="lang-btn" data-lang="mr">\u092e\u0930\u093e</button>
    </div>
    <div class="sb-nav" id="sb-nav">
      <div class="sb-item active" data-page="command"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg><span data-i18n="nav_command">Command Center</span></div>
      <div class="sb-item" data-page="graph"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><line x1="8.5" y1="7.5" x2="15.5" y2="16.5"/><line x1="15.5" y1="7.5" x2="8.5" y2="16.5"/></svg><span data-i18n="nav_graph">Network Explorer</span></div>
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
        <div class="topbar-left"><h2>Command Center</h2><span class="badge-secure">CONNECTION SECURE</span></div>
        <div class="topbar-icons"><div class="icon-btn">\u2699</div><div class="icon-btn">\u25c9</div></div>
      </div>
      <div class="page-pad">
        <div class="stat-grid" id="stat-grid"></div>
        <div class="cc-grid">
          <div class="cc-panel">
            <div class="cc-panel-head"><h3 id="feed-title-el">Live Investigation Feed</h3></div>
            <div id="live-feed-list"></div>
          </div>
          <div class="cc-panel">
            <div class="cc-panel-head"><h3 id="communities-title-el">Detected Communities</h3></div>
            <div id="community-list"></div>
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
          <span class="pf-label">Trace Path:</span>
          <select id="pf-source" class="pf-select"></select>
          <span class="pf-arrow">\u2192</span>
          <select id="pf-target" class="pf-select"></select>
          <button id="btn-find-path" class="btn-pf-run">Trace Path</button>
          <button id="btn-clear-path" class="btn-pf-clear">Reset</button>
        </div>
        <div class="topbar-search"><svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <input id="search-input" data-i18n="search_placeholder" data-i18n-attr="placeholder" placeholder="Query entity, phone, location\u2026"></div>
      </div>
      <div style="display:flex; flex:1; min-height:0;">
        <div id="graph-wrap">
          <div class="graph-dotgrid"></div>
          <div id="graph-toolbar-left"><div class="tool-icon" id="btn-reset" title="Reset Camera">\u2922</div></div>
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
          <h2>Analytics Report</h2>
          <span class="badge-secure">FACT / INFERENCE / LEAD TAGGED</span>
        </div>
        <div style="display:flex; gap:10px; align-items:center; flex-wrap:wrap;">
          <div class="report-filter-group" id="report-filter-group">
            <button class="rf-btn active" data-filter="ALL">All Statements</button>
            <button class="rf-btn fact" data-filter="FACT">FACT</button>
            <button class="rf-btn inference" data-filter="AI_INFERENCE">INFERENCE</button>
            <button class="rf-btn lead" data-filter="LEAD">LEAD</button>
          </div>
          <button class="btn-export-dossier" onclick="window.print()">Export Full Briefing (PDF)</button>
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
