"""
SUTRA — Synthetic Dataset Generator
====================================
Generates a realistic, INTERCONNECTED crime-network dataset for the
investigation demo case. All data is fictional.

Design goal (see project blueprint, Part 5 - "Hidden Network Demo"):
The investigator should NOT be able to see the full network from any
single record. The connections only become visible once CDRs, vehicle
records, lease records and transactions are cross-referenced together
— which is exactly what the entity-resolution + graph-analytics engine
(Phases 2-3) is built to reveal.

Run:  python3 generate_dataset.py
Output: CSV files in ../data/  +  one combined dataset.json
"""

import json
import csv
import os
import random
from datetime import datetime, timedelta

random.seed(42)  # reproducible output

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(OUT_DIR, exist_ok=True)

# ------------------------------------------------------------------
# 1. CORE ENTITIES
# ------------------------------------------------------------------

# People — includes ONE deliberate duplicate-identity pair
# (P01 "Rajeev Malhotra" is later also mentioned as "R. Malhotra" in
# a different source document — this is what the Entity Resolution
# engine in Phase 2 is supposed to catch and merge)
people = [
    {"person_id": "P01", "name": "Rajeev Malhotra", "alias_seen": "R. Malhotra", "role_notes": "Frequently named across multiple source documents"},
    {"person_id": "P02", "name": "Feroz Sheikh", "alias_seen": "", "role_notes": "Prior assault case on record (2022)"},
    {"person_id": "P03", "name": "Anita Rao", "alias_seen": "A. Rao", "role_notes": "Chartered accountant; signatory on multiple accounts"},
    {"person_id": "P04", "name": "Sanjay Verma", "alias_seen": "", "role_notes": "No prior record"},
    {"person_id": "P05", "name": "Deepak Nair", "alias_seen": "", "role_notes": "No prior record"},
    {"person_id": "P06", "name": "Vikram Solanki", "alias_seen": "", "role_notes": "No prior record"},
    {"person_id": "P07", "name": "Meena Iyer", "alias_seen": "", "role_notes": "Company director on record"},
    {"person_id": "P08", "name": "Arjun Kapoor", "alias_seen": "", "role_notes": "No prior record"},
    {"person_id": "P09", "name": "Kavita Joshi", "alias_seen": "", "role_notes": "Unrelated contact - noise entity"},
    {"person_id": "P10", "name": "Imran Qureshi", "alias_seen": "", "role_notes": "Unrelated contact - noise entity"},
]

phones = [
    {"phone_id": "PH01", "number": "+91 98•••1142", "owner_person_id": "P01"},
    {"phone_id": "PH02", "number": "+91 77•••8834", "owner_person_id": "P02"},
    {"phone_id": "PH03", "number": "+91 99•••2207", "owner_person_id": "P03"},
    {"phone_id": "PH04", "number": "+91 88•••5561", "owner_person_id": "P06"},
    {"phone_id": "PH05", "number": "+91 90•••3390", "owner_person_id": "P08"},
    {"phone_id": "PH06", "number": "+91 82•••7743", "owner_person_id": "P09"},
]

vehicles = [
    {"vehicle_id": "V01", "plate_number": "MH-04 GK 7729", "type": "Truck", "owner_org_id": "O02"},
    {"vehicle_id": "V02", "plate_number": "MH-02 CJ 4410", "type": "SUV", "owner_person_id": "P07"},
    {"vehicle_id": "V03", "plate_number": "MH-01 AX 1183", "type": "Sedan", "owner_person_id": "P09"},
]

locations = [
    {"location_id": "L01", "name": "Warehouse, Andheri East", "type": "Warehouse"},
    {"location_id": "L02", "name": "Farmhouse, Alibaug", "type": "Residence"},
    {"location_id": "L03", "name": "Office, Nariman Point", "type": "Commercial"},
    {"location_id": "L04", "name": "Godown, Bhiwandi", "type": "Storage"},
    {"location_id": "L05", "name": "Cafe, Bandra", "type": "Public"},
]

organizations = [
    {"org_id": "O01", "name": "Shree Trading Co.", "incorporated": "2025-12-01", "director_person_id": "P07", "notes": "Recently incorporated, no operational footprint"},
    {"org_id": "O02", "name": "Global Freight Logistics", "incorporated": "2019-03-11", "director_person_id": "P04", "notes": "Established transport contractor"},
]

accounts = [
    {"account_id": "A01", "holder_person_id": "P03", "bank": "HDFC"},
    {"account_id": "A02", "holder_org_id": "O01", "bank": "ICICI"},
    {"account_id": "A03", "holder_person_id": "P01", "bank": "SBI"},
    {"account_id": "A04", "holder_person_id": "P09", "bank": "Axis"},
]

# ------------------------------------------------------------------
# 2. CALLS  (CDRs) — includes an intentional burst (suspicious pattern)
# ------------------------------------------------------------------
def rand_time(base, day_range=30):
    return base + timedelta(days=random.randint(0, day_range),
                             hours=random.randint(6, 23),
                             minutes=random.randint(0, 59))

base_date = datetime(2026, 1, 10)
calls = []
call_id = 1

def add_calls(caller, receiver, n, duration_range=(20, 600), burst=False):
    global call_id
    for _ in range(n):
        t = rand_time(datetime(2026, 2, 11) if burst else base_date, day_range=1 if burst else 30)
        calls.append({
            "call_id": f"C{call_id:03d}", "caller_phone_id": caller, "receiver_phone_id": receiver,
            "timestamp": t.isoformat(), "duration_sec": random.randint(*duration_range)
        })
        call_id += 1

add_calls("PH01", "PH02", 27, burst=True)          # the flagged burst
add_calls("PH01", "PH03", 9)
add_calls("PH01", "PH04", 14)
add_calls("PH03", "PH04", 6)
add_calls("PH04", "PH05", 31)                       # courier-style high frequency
add_calls("PH02", "PH06", 4)                        # noise
add_calls("PH05", "PH06", 3)                        # noise

# ------------------------------------------------------------------
# 3. TRANSACTIONS — includes one large flagged transfer
# ------------------------------------------------------------------
transactions = [
    {"txn_id": "T001", "sender_account_id": "A01", "receiver_account_id": "A02",
     "amount": 1840000, "timestamp": "2026-02-12T15:20:00", "mode": "NEFT"},
    {"txn_id": "T002", "sender_account_id": "A03", "receiver_account_id": "A01",
     "amount": 250000, "timestamp": "2026-01-18T11:05:00", "mode": "IMPS"},
    {"txn_id": "T003", "sender_account_id": "A04", "receiver_account_id": "A02",
     "amount": 12000, "timestamp": "2026-01-22T09:40:00", "mode": "UPI"},
    {"txn_id": "T004", "sender_account_id": "A02", "receiver_account_id": "A01",
     "amount": 60000, "timestamp": "2026-02-01T17:10:00", "mode": "NEFT"},
]

# ------------------------------------------------------------------
# 4. VISITS / EVENTS  (location correlation, vehicle movement)
# ------------------------------------------------------------------
visits = [
    {"visit_id": "VS01", "person_id": "P01", "location_id": "L02", "timestamp": "2026-02-05T21:00:00", "notes": "GPS-tagged surveillance"},
    {"visit_id": "VS02", "person_id": "P02", "location_id": "L02", "timestamp": "2026-02-05T21:10:00", "notes": "GPS-tagged surveillance"},
    {"visit_id": "VS03", "person_id": "P03", "location_id": "L03", "timestamp": "2026-01-15T10:00:00", "notes": "Registered workplace"},
    {"visit_id": "VS04", "person_id": "P05", "location_id": "L01", "timestamp": "2026-01-20T14:00:00", "notes": "Registered workplace"},
    {"visit_id": "VS05", "person_id": "P04", "location_id": "L04", "timestamp": "2026-01-25T13:00:00", "notes": "Lease signed - cash payment"},
    {"visit_id": "VS06", "person_id": "P06", "location_id": "L01", "timestamp": "2026-02-02T18:00:00", "notes": ""},
    {"visit_id": "VS07", "person_id": "P06", "location_id": "L04", "timestamp": "2026-02-06T23:15:00", "notes": "Bridges two otherwise separate sites"},
    {"vehicle_visit": True, "visit_id": "VS08", "vehicle_id": "V01", "location_id": "L04", "timestamp": "2026-02-07T23:40:00", "notes": "6 trips recorded at odd hours"},
    {"vehicle_visit": True, "visit_id": "VS09", "vehicle_id": "V02", "location_id": "L02", "timestamp": "2026-02-05T20:55:00", "notes": ""},
]

# ------------------------------------------------------------------
# 5. FIR / SOURCE DOCUMENTS  (raw unstructured text for the NLP demo)
# ------------------------------------------------------------------
fir_records = [
    {
        "case_id": "FIR-031", "date": "2026-02-14", "station": "PS Andheri",
        "description": (
            "On 14/02/2026, surveillance team reported that RAJEEV MALHOTRA (M/42) was observed "
            "meeting FEROZ SHEIKH near the warehouse at ANDHERI EAST at approx. 2130 hrs. A vehicle "
            "bearing registration MH-04 GK 7729 was seen departing the location at 2245 hrs. Phone "
            "records indicate the number +91 98•••1142, registered to the same individual, made "
            "repeated contact with +91 77•••8834 over the preceding 48 hours. The complainant also "
            "named SHREE TRADING CO. as the entity operating the leased premises."
        ),
        "source_reliability": "High"
    },
    {
        "case_id": "FIR-014", "date": "2026-01-26",
        "station": "PS Bhiwandi",
        "description": (
            "Local intelligence report (unverified) suggests SANJAY VERMA leased a godown in "
            "BHIWANDI approximately three months prior under a cash arrangement. No formal complaint "
            "has been filed. Source: field informant."
        ),
        "source_reliability": "Low"
    },
]

# ------------------------------------------------------------------
# WRITE OUTPUT
# ------------------------------------------------------------------
def write_csv(filename, rows):
    if not rows:
        return
    path = os.path.join(OUT_DIR, filename)
    keys = sorted({k for row in rows for k in row.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  wrote {filename:30s} ({len(rows)} rows)")

print("Generating SUTRA synthetic dataset...")
write_csv("people.csv", people)
write_csv("phones.csv", phones)
write_csv("vehicles.csv", vehicles)
write_csv("locations.csv", locations)
write_csv("organizations.csv", organizations)
write_csv("accounts.csv", accounts)
write_csv("calls.csv", calls)
write_csv("transactions.csv", transactions)
write_csv("visits.csv", visits)
write_csv("fir_records.csv", fir_records)

combined = {
    "people": people, "phones": phones, "vehicles": vehicles, "locations": locations,
    "organizations": organizations, "accounts": accounts, "calls": calls,
    "transactions": transactions, "visits": visits, "fir_records": fir_records,
}
with open(os.path.join(OUT_DIR, "dataset.json"), "w", encoding="utf-8") as f:
    json.dump(combined, f, indent=2)
print(f"  wrote dataset.json (combined)")

print("\nDone. Total entities:",
      len(people)+len(phones)+len(vehicles)+len(locations)+len(organizations)+len(accounts),
      "| Total relational records:",
      len(calls)+len(transactions)+len(visits))
