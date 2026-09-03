import re
import spacy

# Load the spaCy English model (assuming en_core_web_sm is installed)
try:
    nlp = spacy.load("en_core_web_sm")
except Exception:
    print("Warning: SpaCy model 'en_core_web_sm' not found. NLP extraction may be mocked or fail.")
    nlp = None

# Regex patterns for structured identifiers
REGEX_PATTERNS = {
    "phone": r"\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
    "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b",
    "account_number": r"\b(?:ACCT|AC|account)[\s:-]*([0-9]{8,12})\b",
    "vehicle": r"\b[A-Z]{2}[ -]?[0-9]{1,2}[ -]?[A-Z]{1,2}[ -]?[0-9]{4}\b" # e.g. MH 12 AB 1234
}

def extract_entities_from_text(text: str):
    """
    Runs NLP NER and Regex to extract entities.
    Returns a tuple of (entities list, relationships list).
    """
    entities = []
    
    # 1. Regex Extraction
    for label, pattern in REGEX_PATTERNS.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            entities.append({
                "value": match.group(0).strip(),
                "label": label.upper(),
                "confidence": 1.0,
                "source": "regex"
            })

    # 2. NLP NER Extraction
    if nlp:
        doc = nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE", "DATE"]:
                # Normalization happens in resolution module, but we store raw here
                entities.append({
                    "value": ent.text.strip(),
                    "label": ent.label_,
                    "confidence": 0.85, # Base confidence for sm model
                    "source": "nlp"
                })
                
    # Basic deduplication at extraction time
    unique_entities = []
    seen = set()
    for e in entities:
        key = (e["value"].lower(), e["label"])
        if key not in seen:
            seen.add(key)
            unique_entities.append(e)

    # 3. Basic Relationship Extraction (Proximity based)
    # If a person and another entity are in the same sentence, assume relationship
    relationships = []
    if nlp:
        for sent in doc.sents:
            sent_text = sent.text
            persons_in_sent = [e for e in unique_entities if e["label"] == "PERSON" and e["value"] in sent_text]
            phones_in_sent = [e for e in unique_entities if e["label"] == "PHONE" and e["value"] in sent_text]
            vehicles_in_sent = [e for e in unique_entities if e["label"] == "VEHICLE" and e["value"] in sent_text]
            locations_in_sent = [e for e in unique_entities if e["label"] == "GPE" and e["value"] in sent_text]
            
            for p in persons_in_sent:
                for ph in phones_in_sent:
                    relationships.append({"source": p["value"], "target": ph["value"], "type": "OWNS_PHONE", "confidence": 0.7})
                for v in vehicles_in_sent:
                    relationships.append({"source": p["value"], "target": v["value"], "type": "USED_VEHICLE", "confidence": 0.7})
                for loc in locations_in_sent:
                    relationships.append({"source": p["value"], "target": loc["value"], "type": "LOCATED_AT", "confidence": 0.6})

    return unique_entities, relationships
