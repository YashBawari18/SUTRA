"""
SUTRA — Entity Resolution Engine
==================================
Real, working implementation (not simulated) of the entity-resolution
step described in the blueprint (Part 7).

Problem it solves: NLP extraction from different documents produces
different-looking mentions of the SAME real person — e.g. "Rajeev
Malhotra" in one FIR and "R. Malhotra" in a surveillance note. Without
resolving these, the knowledge graph ends up with duplicate,
disconnected nodes and hides real connections.

Method: combines name similarity with shared-attribute evidence
(phone, location, organization) into one transparent, explainable
confidence score. No black-box ML model — every score is fully
traceable, which matters for a law-enforcement context.

Run:  python3 entity_resolution.py
"""

import json
import os
import difflib
import re

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

with open(os.path.join(DATA_DIR, "dataset.json"), encoding="utf-8") as f:
    data = json.load(f)

people = data["people"]

# ------------------------------------------------------------------
# Simulated raw NLP "mentions" pulled from different source documents.
# In a real system these would come out of the NER pipeline (Phase 5).
# Each mention may or may not carry extra context (a phone number
# seen nearby in the same document, a location mentioned nearby).
# ------------------------------------------------------------------
raw_mentions = [
    {"mention_id": "M01", "extracted_name": "R. Malhotra", "source_doc": "Surveillance-09",
     "context_phone": "+91 98•••1142", "context_location": None},
    {"mention_id": "M02", "extracted_name": "A. Rao", "source_doc": "FIR-031",
     "context_phone": None, "context_location": "Office, Nariman Point"},
    {"mention_id": "M03", "extracted_name": "Vikram S.", "source_doc": "CDR-annotation",
     "context_phone": "+91 88•••5561", "context_location": None},
    {"mention_id": "M04", "extracted_name": "Ferozz Shiekh", "source_doc": "Informant-tip-22",  # misspelled — realistic noisy input
     "context_phone": None, "context_location": None},
]

phones_by_person = {}
for ph in data["phones"]:
    phones_by_person.setdefault(ph["owner_person_id"], []).append(ph["number"])

locations_by_person = set()
loc_lookup = {loc["location_id"]: loc["name"] for loc in data["locations"]}
person_locations = {}
for v in data["visits"]:
    if v.get("person_id"):
        person_locations.setdefault(v["person_id"], set()).add(loc_lookup.get(v["location_id"], ""))


def normalize(name: str) -> str:
    return re.sub(r"[.\s]+", " ", name.strip().lower())


def initials_match(short: str, full: str) -> bool:
    """Handles 'R. Malhotra' vs 'Rajeev Malhotra' style abbreviations."""
    s_parts = normalize(short).split()
    f_parts = normalize(full).split()
    if len(s_parts) != len(f_parts):
        return False
    for s, f in zip(s_parts, f_parts):
        if s == f:
            continue
        if len(s) <= 2 and f.startswith(s.rstrip(".")):
            continue
        return False
    return True


def name_similarity(a: str, b: str) -> float:
    if initials_match(a, b) or initials_match(b, a):
        return 0.55
    return difflib.SequenceMatcher(None, normalize(a), normalize(b)).ratio() * 0.55


def resolve_mention(mention, candidates):
    """Score this mention against every known person; return ranked matches
    with a full, human-readable breakdown of WHY each score was given."""
    results = []
    for person in candidates:
        breakdown = {}
        name_score = name_similarity(mention["extracted_name"], person["name"])
        breakdown["name_similarity"] = round(name_score, 3)

        phone_score = 0.0
        if mention.get("context_phone") and mention["context_phone"] in phones_by_person.get(person["person_id"], []):
            phone_score = 0.25
        breakdown["shared_phone"] = phone_score

        loc_score = 0.0
        if mention.get("context_location") and mention["context_location"] in person_locations.get(person["person_id"], set()):
            loc_score = 0.15
        breakdown["shared_location"] = loc_score

        total = min(1.0, name_score + phone_score + loc_score)
        results.append({
            "person_id": person["person_id"], "person_name": person["name"],
            "confidence": round(total, 3), "breakdown": breakdown
        })
    results.sort(key=lambda r: r["confidence"], reverse=True)
    return results


MERGE_THRESHOLD = 0.60
REVIEW_THRESHOLD = 0.40

print("=" * 70)
print("SUTRA ENTITY RESOLUTION — resolving raw mentions against known people")
print("=" * 70)

resolution_log = []
for mention in raw_mentions:
    ranked = resolve_mention(mention, people)
    best = ranked[0]
    if best["confidence"] >= MERGE_THRESHOLD:
        decision = "AUTO-MERGE (flagged for investigator confirmation)"
    elif best["confidence"] >= REVIEW_THRESHOLD:
        decision = "SUGGESTED MATCH (requires manual review)"
    else:
        decision = "NO CONFIDENT MATCH (kept as separate/unknown entity)"

    print(f"\nMention '{mention['extracted_name']}'  (source: {mention['source_doc']})")
    print(f"  -> Best match: {best['person_name']} ({best['person_id']})")
    print(f"     Confidence: {best['confidence']*100:.1f}%")
    for k, v in best["breakdown"].items():
        if v:
            print(f"       + {k.replace('_',' ')}: {v}")
    print(f"     Decision: {decision}")

    resolution_log.append({
        "mention": mention["extracted_name"], "source_doc": mention["source_doc"],
        "matched_person_id": best["person_id"], "matched_person_name": best["person_name"],
        "confidence": best["confidence"], "breakdown": best["breakdown"], "decision": decision
    })

out_path = os.path.join(DATA_DIR, "entity_resolution_results.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(resolution_log, f, indent=2)

print("\n" + "=" * 70)
print(f"Saved full results -> {out_path}")
print("=" * 70)
