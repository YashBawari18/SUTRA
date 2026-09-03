"""
SUTRA — Entity Extraction Engine (Lightweight NER)
=====================================================
Real, working extraction of entities from raw unstructured text
(FIR paragraphs, surveillance notes) using:
  - Regex patterns for structured entities (phone numbers, vehicle
    plates, money amounts, dates, case IDs)
  - A gazetteer (known-name lookup) built from the case dataset for
    PERSON / LOCATION / ORGANIZATION, with fuzzy fallback for partial
    or misspelled mentions

This is the honest, buildable version of "NLP entity extraction" for
a prototype stage (blueprint Part 6). A production system would swap
the gazetteer + regex layer for a fine-tuned transformer/IndicNLP
model trained on real FIR text — the pipeline position stays the same,
only the extraction method underneath changes.

Run:  python3 entity_extraction.py
"""

import json
import os
import re
import difflib

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
with open(os.path.join(DATA_DIR, "dataset.json"), encoding="utf-8") as f:
    data = json.load(f)

# ------------------------------------------------------------------
# Build gazetteers from known case entities
# ------------------------------------------------------------------
person_names = [p["name"] for p in data["people"]]
location_names = [l["name"] for l in data["locations"]]
# also register short-form place names (e.g. "Andheri East" from
# "Warehouse, Andheri East") so mentions without the full label still match
for l in data["locations"]:
    if "," in l["name"]:
        short = l["name"].split(",", 1)[1].strip()
        if short not in location_names:
            location_names.append(short)
org_names = [o["name"] for o in data["organizations"]]

# ------------------------------------------------------------------
# Regex patterns for structured entity types
# ------------------------------------------------------------------
PATTERNS = {
    "PHONE": re.compile(r"\+?\d{2}\s?\d{2}[•\d]{2,}\d{4}|\+91[\s-]?\d{5}[•\d]*\d{4}"),
    "VEHICLE": re.compile(r"\b[A-Z]{2}-\d{2}\s?[A-Z]{2}\s?\d{4}\b"),
    "MONEY": re.compile(r"₹\s?[\d,]+(?:\.\d+)?|Rs\.?\s?[\d,]+(?:\.\d+)?|INR\s?[\d,]+"),
    "DATE": re.compile(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"),
    "CASE_ID": re.compile(r"\bFIR-\d+\b|\bCase[- ]ID[:\s]*\S+"),
    "TIME": re.compile(r"\b\d{3,4}\s?hrs\b|\b\d{1,2}:\d{2}\s?(?:AM|PM)?\b"),
}


def extract_gazetteer_entities(text, names, entity_type, fuzzy_threshold=0.82):
    """Finds exact + near-exact (fuzzy) matches of known names in free text."""
    found = []
    text_upper = text.upper()
    for name in names:
        if name.upper() in text_upper:
            idx = text_upper.find(name.upper())
            found.append({"text": text[idx:idx+len(name)], "type": entity_type, "matched_entity": name, "match": "exact"})
            continue
        # fuzzy fallback: scan capitalized word windows for close matches
        words = re.findall(r"[A-Z][A-Za-z.]*(?:\s+[A-Z][A-Za-z.]*){0,2}", text)
        for w in words:
            ratio = difflib.SequenceMatcher(None, w.upper(), name.upper()).ratio()
            if ratio >= fuzzy_threshold:
                found.append({"text": w, "type": entity_type, "matched_entity": name, "match": f"fuzzy ({ratio:.2f})"})
    return found


def extract_regex_entities(text):
    found = []
    for label, pattern in PATTERNS.items():
        for m in pattern.finditer(text):
            found.append({"text": m.group(), "type": label, "match": "pattern"})
    return found


def extract_all(text):
    results = []
    results += extract_regex_entities(text)
    results += extract_gazetteer_entities(text, person_names, "PERSON")
    results += extract_gazetteer_entities(text, location_names, "LOCATION")
    results += extract_gazetteer_entities(text, org_names, "ORGANIZATION")
    # de-duplicate identical (text, type) pairs
    seen = set()
    unique = []
    for r in results:
        key = (r["text"], r["type"])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique


print("=" * 72)
print("SUTRA ENTITY EXTRACTION — running on raw FIR text")
print("=" * 72)

extraction_log = []
for fir in data["fir_records"]:
    text = fir["description"]
    entities = extract_all(text)
    print(f"\n{fir['case_id']} ({fir['station']}, reliability: {fir['source_reliability']})")
    print(f"  Source text: {text[:90]}...")
    print(f"  Extracted {len(entities)} entities:")
    for e in sorted(entities, key=lambda x: x["type"]):
        matched = f" -> {e['matched_entity']}" if "matched_entity" in e else ""
        print(f"    [{e['type']:12s}] {e['text']}{matched}   ({e['match']})")
    extraction_log.append({"case_id": fir["case_id"], "entities": entities})

out_path = os.path.join(DATA_DIR, "extraction_results.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(extraction_log, f, indent=2)
print(f"\nSaved -> {out_path}")
