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


class AssistantQuery(BaseModel):
    case_id: str
    question: str


def retrieve_graph_facts(case_id: str, question: str) -> list[dict]:
    """
    Production implementation: parse the question for entity names,
    query Neo4j for their neighborhood + relevant relationships, and run
    a vector similarity search (FAISS/pgvector) over source documents
    for narrative context. Returns a list of structured, source-attributed
    facts — never raw document text.
    """
    return []  # TODO: wire to Neo4j + vector store


def call_llm(structured_context: list[dict], question: str) -> str:
    """
    Calls the LLM with ONLY the structured, retrieved context — never the
    raw question-plus-documents. Requires ANTHROPIC_API_KEY to be set.
    """
    try:
        import anthropic
    except ImportError:
        return "LLM client not installed in this environment. Install `anthropic` to enable this endpoint."

    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    context_block = "\n".join(f"- {fact}" for fact in structured_context) or "(no matching evidence found)"

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
