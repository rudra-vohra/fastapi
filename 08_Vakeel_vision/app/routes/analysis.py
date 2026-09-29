from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.config import GEMINI_API_KEY
from app.database import contracts_collection, analysis_collection
from app.service.contract_analyzer import analyze_contract

router = APIRouter(prefix="/analysis", tags=["Analysis"])


def _convert_obj(obj):
    """Recursively convert MongoDB ObjectId values to strings."""
    if isinstance(obj, list):
        return [_convert_obj(value) for value in obj]
    if isinstance(obj, dict):
        return {
            ("id" if key == "_id" else key): _convert_obj(value)
            for key, value in obj.items()
        }
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj


@router.post("/analyse/{contract_id}")
async def analyse_contract(contract_id: str):
    '''Endpoint to analyze a specific contract using AI and return the results.'''
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key is not configured.")

    contract = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")

    if not contract.get("text_content"):
        raise HTTPException(status_code=400, detail="Contract has no text content to analyze.")

    contracts_collection.update_one({"_id": ObjectId(contract_id)}, {"$set": {"status": "analyzing"}})

    result = await analyze_contract(contract_id, contract["text_content"])
    doc = result.model_dump()

    insert_result = analysis_collection.insert_one(doc)
    result.id = str(insert_result.inserted_id)

    contracts_collection.update_one({"_id": ObjectId(contract_id)}, {"$set": {"status": "analyzed"}})

    return {
        'message': 'Contract analyzed successfully.',
        'analysis_result': result.model_dump(),
        'analysis_id': result.id    
    }

@router.get('/')
def list_analyses():
    """
    List all analyses performed.
    """
    analyses = [_convert_obj(doc) for doc in analysis_collection.find({})]
    return {"analyses": analyses}


@router.get("/{analysis_id}")
def get_analysis(analysis_id: str):
    """
    Retrieve the results of a specific analysis by ID.
    """
    analysis = analysis_collection.find_one({"_id": ObjectId(analysis_id)})

    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")

    return {"analysis": _convert_obj(analysis)}


@router.get("/contract/{contract_id}")
async def get_analyses_for_contract(contract_id: str):
    """Get all analyses for a specific contract."""
    analyses = []
    cursor = analysis_collection.find({"contract_id": contract_id})

    for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        analyses.append(doc)

    return {"analyses": analyses, "total": len(analyses)}



