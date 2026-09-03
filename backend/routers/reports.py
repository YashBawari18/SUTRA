import os
from fastapi import APIRouter, Depends
from auth import require_role, TokenData
from database import SessionLocal, neo4j_conn
from models import Case, Evidence

router = APIRouter()

@router.post("/generate")
def generate_report(case_id: str, language: str = "English", user: TokenData = Depends(require_role("senior_investigator"))):
    """
    Generates a live multilingual case report using Anthropic LLM (PRD Gap #31).
    """
    db = SessionLocal()
    neo4j_session = neo4j_conn.get_session()
    
    try:
        # 1. Fetch Case Meta
        case = db.query(Case).filter(Case.id == case_id).first()
        evidence_count = db.query(Evidence).filter(Evidence.case_id == case_id).count()
        
        # 2. Fetch Graph Meta (Top Entities)
        top_entities_query = """
        MATCH (n {case_id: $case_id})
        WHERE n:Person OR n:Organization
        RETURN n.name as name, labels(n)[0] as type
        LIMIT 10
        """
        entities_result = neo4j_session.run(top_entities_query, case_id=case_id)
        entities = [f"{r['name']} ({r['type']})" for r in entities_result]
        
        # 3. Construct Context for LLM
        context = f"""
        CASE ID: {case_id}
        TITLE: {case.title if case else 'Unknown'}
        TOTAL EVIDENCE FILES: {evidence_count}
        KEY ENTITIES INVOLVED: {', '.join(entities)}
        """
        
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            return {
                "case_id": case_id,
                "language": language,
                "report": f"MOCK REPORT ({language})\n\nFACT:\nCase {case_id} has {evidence_count} evidence items.\n\nAI INFERENCE:\nThe network revolves around {len(entities)} key entities.\n\nINVESTIGATIVE LEAD:\nVerify cross-source overlapping entities.",
                "generated_by": user.username
            }
            
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        prompt = f"""
        You are SUTRA's report generator. Based on the following live case context, generate an intelligence report.
        The report MUST be written in {language}.
        The report MUST strictly use the following 3 sections:
        
        FACT: (Summarize the verified data)
        AI INFERENCE: (Provide logical network deduction)
        INVESTIGATIVE LEAD: (Suggest what to investigate next)
        
        CONTEXT:
        {context}
        """
        
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=600,
            temperature=0.2,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return {
            "case_id": case_id,
            "language": language,
            "report": "".join(b.text for b in response.content if b.type == "text"),
            "generated_by": user.username
        }
    finally:
        db.close()
        neo4j_session.close()

