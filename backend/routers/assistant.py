import os
import json
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from auth import require_role, TokenData
from database import neo4j_conn, SessionLocal
from models import Evidence

router = APIRouter()

SYSTEM_PROMPT = """You are SUTRA's AI Investigation Copilot. You assist investigators by analyzing criminal network data and evidence.
CRITICAL RULE: You MUST output your response strictly as a JSON object adhering to the SUTRA AI Response Contract:
{
    "finding": "String describing the factual finding",
    "observed_evidence": ["Fact 1 from context", "Fact 2 from context"],
    "analytical_basis": "String explaining how the evidence leads to the inference",
    "inference": "Your logical deduction based ONLY on the evidence",
    "confidence": "High/Medium/Low percentage",
    "supporting_evidence_ids": ["E-123", "E-456"],
    "suggested_next_checks": ["Check X", "Verify Y"],
    "human_verification_required": true
}
Do NOT output any conversational text before or after the JSON.
Do NOT hallucinate. If the context is empty or insufficient, state that in the finding and inference.
"""

class AssistantQuery(BaseModel):
    case_id: str
    question: str

def retrieve_context(case_id: str, question: str) -> list[dict]:
    """
    RAG Retrieval: Fetches relevant graph structures and raw evidence text.
    """
    context = []
    q_lower = question.lower()
    neo4j_session = neo4j_conn.get_session()
    db = SessionLocal()
    
    try:
        # 0. Prompt Injection Defense (Gap Check)
        malicious_patterns = ["ignore previous", "forget instructions", "system prompt", "you are now"]
        if any(p in q_lower for p in malicious_patterns):
            return {
                "finding": "SECURITY ALERT: Suspicious query pattern detected.",
                "observed_evidence": ["The query contained patterns attempting to override system constraints."],
                "analytical_basis": "Input validation identified malicious intent.",
                "inference": "The user may be attempting to bypass the AI Copilot's strict evidence-grounding rules.",
                "confidence": "100%",
                "supporting_evidence_ids": [],
                "suggested_next_checks": ["Review audit logs for user activity", "Escalate to admin"],
                "human_verification_required": True
            }

        # 1. Graph Retrieval (Nodes and relationships for context)
        graph_query = """
        MATCH (n {case_id: $case_id})-[r]-(m {case_id: $case_id})
        RETURN n.name as source, type(r) as rel, m.name as target, r.evidence_id as evidence_id LIMIT 15
        """
        result = neo4j_session.run(graph_query, case_id=case_id)
        for record in result:
            # Simple keyword matching for RAG
            if record["source"].lower() in q_lower or record["target"].lower() in q_lower or "who" in q_lower or "what" in q_lower:
                context.append({
                    "fact": f"{record['source']} {record['rel']} {record['target']}",
                    "evidence_id": record.get("evidence_id")
                })
        
        # 2. PostgreSQL Evidence Metadata
        evidence_records = db.query(Evidence).filter(Evidence.case_id == case_id).all()
        for ev in evidence_records:
            if ev.file_name.lower() in q_lower or "evidence" in q_lower:
                context.append({
                    "fact": f"Evidence File: {ev.file_name} (Type: {ev.file_type}, Hash: {ev.sha256_hash})",
                    "evidence_id": ev.id
                })
                
    finally:
        neo4j_session.close()
        db.close()
        
    return context

def call_llm(structured_context: list[dict], question: str) -> dict:
    """
    Calls Anthropic LLM and forces the Response Contract.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    
    context_block = json.dumps(structured_context, indent=2)
    
    if not api_key:
        # Mock Response Contract if no key provided
        return {
            "finding": f"Mock finding for query: {question}",
            "observed_evidence": [c["fact"] for c in structured_context],
            "analytical_basis": "Mock analytical basis due to missing API key.",
            "inference": "The subject appears central to the network based on the retrieved facts.",
            "confidence": "85%",
            "supporting_evidence_ids": list(set([c["evidence_id"] for c in structured_context if c.get("evidence_id")])),
            "suggested_next_checks": ["Configure ANTHROPIC_API_KEY", "Verify connections manually"],
            "human_verification_required": True
        }

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=800,
            temperature=0.0,
            system=SYSTEM_PROMPT,
            messages=[{
                "role": "user",
                "content": f"EVIDENCE CONTEXT:\n{context_block}\n\nINVESTIGATOR QUESTION:\n{question}"
            }]
        )
        
        response_text = "".join(b.text for b in response.content if b.type == "text")
        
        # Clean potential markdown wrapping
        if response_text.startswith("```json"):
            response_text = response_text[7:-3]
            
        return json.loads(response_text)
    except Exception as err:
        return {
            "finding": "Error contacting AI assistant provider.",
            "observed_evidence": [],
            "analytical_basis": str(err),
            "inference": "System failure.",
            "confidence": "0%",
            "supporting_evidence_ids": [],
            "suggested_next_checks": ["Check API logs"],
            "human_verification_required": True
        }

@router.post("/query")
def query_assistant(payload: AssistantQuery, user: TokenData = Depends(require_role("investigator"))):
    context = retrieve_context(payload.case_id, payload.question)
    response_contract = call_llm(context, payload.question)
    return {
        "case_id": payload.case_id,
        "question": payload.question,
        "contract": response_contract
    }

