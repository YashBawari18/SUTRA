import uuid

def normalize_entity_value(value: str, label: str) -> str:
    """
    Normalizes a string for matching based on entity type.
    """
    val = value.strip().upper()
    if label == "PHONE":
        # Strip non-numeric
        val = ''.join(filter(str.isdigit, val))
        if len(val) == 10:
            val = f"+91{val}" # Defaulting to India for SUTRA context demo
    elif label == "EMAIL":
        val = val.lower()
    elif label in ["PERSON", "ORG"]:
        # Remove common prefixes/suffixes
        prefixes = ["MR.", "MRS.", "DR.", "M/S", "PVT", "LTD"]
        for p in prefixes:
            val = val.replace(p, "").strip()
    return val

def generate_entity_id(normalized_value: str, label: str) -> str:
    """
    Generates a deterministic ID based on normalized value to passively resolve exact matches.
    """
    safe_val = "".join(c for c in normalized_value if c.isalnum())
    prefix = label[:3].upper()
    # Simple hash for demo purposes; production uses stronger uuid5 or deterministic hashing
    hashed = str(abs(hash(safe_val)))[:8]
    return f"{prefix}-{hashed}"

def resolve_entities(extracted_entities: list) -> list:
    """
    Takes raw extracted entities and normalizes them, assigning deterministic IDs.
    Returns resolved entities.
    """
    resolved = []
    for ent in extracted_entities:
        norm_val = normalize_entity_value(ent["value"], ent["label"])
        ent_id = generate_entity_id(norm_val, ent["label"])
        resolved.append({
            "id": ent_id,
            "raw_value": ent["value"],
            "normalized_value": norm_val,
            "label": ent["label"],
            "source": ent["source"]
        })
        
    return resolved
