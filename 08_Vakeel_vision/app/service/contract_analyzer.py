from google import genai
from app.service.prompt import CONTRACT_ANALYSIS_PROMPT
from app.config import GEMINI_API_KEY
import json
from app.models import AnalysisResult, ClauseAnalysis, RiskFlag





client = genai.Client(api_key=GEMINI_API_KEY)


async def analyze_contract(contract_id: str,text_content: str):
    '''Analyzes the contract text using the Gemini API and returns the analysis results.'''

    prompt = CONTRACT_ANALYSIS_PROMPT.format(contract_text=text_content[:15000])
    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=prompt,
    )

    response_text = json.loads(interaction.output_text)

    if isinstance(response_text, str):
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            data = response_text
    else:
        data = response_text
    
    if isinstance(data, dict) and "candidates" in data:
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
    elif isinstance(data, dict):
        raw_text = json.dumps(data)
    else:
        raw_text = str(data)


    raw_text = raw_text.strip()

    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    raw_text = raw_text.strip()

    analysis_data = json.loads(raw_text)
    key_clauses = [
            ClauseAnalysis(**clause)
            for clause in analysis_data.get("key_clauses", [])
    ]
    
    risk_flags = []
    for risk in analysis_data.get("risk_flags", []):
        # Gemini may use ``clause_title`` for the field named ``risk_title``
        # in the Pydantic model.
        normalized_risk = dict(risk)
        if "risk_title" not in normalized_risk and "clause_title" in normalized_risk:
            normalized_risk["risk_title"] = normalized_risk.pop("clause_title")
        risk_flags.append(RiskFlag(**normalized_risk))
    
    result = AnalysisResult(
            contract_id=contract_id,
            summary=analysis_data.get("summary", ""),
            contract_type=analysis_data.get("contract_type", "Unknown"),
            key_clauses=key_clauses,
            risk_flags=risk_flags,
            overall_risk_level=analysis_data.get("overall_risk_level", "low"),
            recommendations=analysis_data.get("recommendations", []),
    )
    return result


