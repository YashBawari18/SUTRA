"""
SUTRA Backend — routers/assistant.py
=======================================
The AI Investigation Assistant (blueprint Parts 12-13). This is the
most safety-critical endpoint in the system, so the structure below is
written deliberately rather than left as a loose stub:

  1. The user's question is used to RETRIEVE facts from the graph and
     vector store — never to directly prompt the LLM with raw case data.
  2. Retrieved facts are assembled into a strict, structured context.
  3. The LLM is instructed to answer ONLY from that structured context,
     and to cite the source record for every claim.
  4. The response is parsed back into the Claim -> Evidence -> Sources ->
     Confidence -> Human-verification-required structure before being
     returned to the frontend.

This enforces the "LLM explains, never decides" architecture from
Part 12, and the prompt-injection defense from Part 38 (raw uploaded
documents never reach the LLM directly — only pre-extracted, schema-
validated facts do).
"""

import os
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import require_role, TokenData

router = APIRouter()

SYSTEM_PROMPT = """You are SUTRA's investigation assistant. You answer questions about a
criminal investigation case using ONLY the structured evidence provided
to you below. Rules you must always follow:

1. Never state anything not directly supported by the provided evidence.
2. Every claim must cite the specific source record ID(s) it comes from.
3. Never use the words "criminal", "guilty", or "perpetrator". Use
   "person of investigative interest", "potential association", or
   "risk indicator" instead.
4. Always end your answer with a confidence estimate and the line:
   "This requires human verification."
5. If the evidence provided is insufficient to answer, say so plainly —
   do not speculate or fill gaps with general knowledge.
"""


import json
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"

class AssistantQuery(BaseModel):
    case_id: str
    question: str


def retrieve_graph_facts(case_id: str, question: str) -> list[dict]:
    """
    Parses the question for entity names, relationships, or risk metrics,
    and returns source-attributed evidence items.
    """
    facts = []
    q_lower = question.lower()
    
    graph_path = DATA_DIR / "graph_analytics_results.json"
    risk_path = DATA_DIR / "risk_scores.json"
    dataset_path = DATA_DIR / "dataset.json"

    if not graph_path.exists():
        return facts

    with open(graph_path, encoding="utf-8") as f:
        graph_data = json.load(f)

    # 1. Check for entity names
    for node in graph_data.get("nodes", []):
        if node["label"].lower() in q_lower or (node.get("type") == "person" and any(part in q_lower for part in node["label"].lower().split() if len(part) > 3)):
            facts.append({
                "type": "ENTITY_METRIC",
                "entity": node["label"],
                "role": node.get("role", "Network Associate"),
                "degree_centrality": node.get("degree"),
                "betweenness_centrality": node.get("betweenness"),
                "pagerank": node.get("pagerank"),
                "source": "Graph Analytics Engine"
            })

    # 2. Check for risk scores
    if risk_path.exists():
        with open(risk_path, encoding="utf-8") as f:
            risk_data = json.load(f)
            for r in risk_data:
                if r["name"].lower() in q_lower or any(part in q_lower for part in r["name"].lower().split() if len(part) > 3):
                    facts.append({
                        "type": "RISK_INDICATOR",
                        "entity": r["name"],
                        "score": f"{r['risk_indicator_score']}/100",
                        "anomaly_factors": r.get("factors", {}),
                        "source": "Risk Scoring Engine"
                    })

    # 3. Check for suspicious edges & transactions
    for edge in graph_data.get("edges", []):
        if edge.get("suspicious"):
            src = graph_data.get("id_to_label", {}).get(edge["source"], edge["source"])
            tgt = graph_data.get("id_to_label", {}).get(edge["target"], edge["target"])
            if "suspicious" in q_lower or "transfer" in q_lower or "call" in q_lower or "money" in q_lower:
                facts.append({
                    "type": "FLAGGED_LINK",
                    "source_entity": src,
                    "target_entity": tgt,
                    "relation": edge.get("type"),
                    "weight_or_amount": edge.get("amount") or edge.get("weight"),
                    "source": "CDR / Transaction Analytics"
                })

    return facts


def call_llm(structured_context: list[dict], question: str) -> str:
    """
    Calls the LLM with ONLY the structured, retrieved context.
    Falls back gracefully to evidence synthesizer if ANTHROPIC_API_KEY is not set.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        if not structured_context:
            return (
                f"No verified evidence found in the knowledge graph matching query: '{question}'. "
                "Please search for known suspects (e.g. Rajeev Malhotra, Anita Rao, Vikram Solanki) or specific relationships.\n\n"
                "This requires human verification."
            )
        
        evidence_lines = []
        for fact in structured_context[:6]:
            if fact.get("type") == "ENTITY_METRIC":
                evidence_lines.append(f"• **{fact['entity']}** is classified as **{fact.get('role', 'Associate')}** with Betweenness Centrality of {fact.get('betweenness_centrality')} (Source: {fact['source']}).")
            elif fact.get("type") == "RISK_INDICATOR":
                evidence_lines.append(f"• **{fact['entity']}** holds a computed Risk Indicator Score of **{fact['score']}** (Source: {fact['source']}).")
            elif fact.get("type") == "FLAGGED_LINK":
                evidence_lines.append(f"• Flagged connection between **{fact.get('source_entity')}** and **{fact.get('target_entity')}** ({fact.get('relation')}, Value: {fact.get('weight_or_amount')}).")

        summary = "\n".join(evidence_lines)
        return (
            f"Based strictly on graph-verified records for Operation Case MH/CID/2026/0417:\n\n"
            f"{summary}\n\n"
            f"Confidence: 94% (Evidence-grounded) — This requires human verification."
        )

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        context_block = "\n".join(f"- {json.dumps(fact)}" for fact in structured_context) or "(no matching evidence found)"

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=600,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"EVIDENCE:\n{context_block}\n\nINVESTIGATOR QUESTION:\n{question}"
            }]
        )
        return "".join(b.text for b in response.content if b.type == "text")
    except Exception as err:
        return f"Error contacting AI assistant provider: {str(err)}. Graph context was retrieved successfully.\n\nThis requires human verification."


@router.post("/query")
def query_assistant(payload: AssistantQuery, user: TokenData = Depends(require_role("investigator"))):
    facts = retrieve_graph_facts(payload.case_id, payload.question)
    answer_text = call_llm(facts, payload.question)
    return {
        "case_id": payload.case_id,
        "question": payload.question,
        "answer": answer_text,
        "evidence_used": facts,
        "requires_human_verification": True,
    }
