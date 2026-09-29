from fastapi import APIRouter,UploadFile, File, HTTPException
import os
import uuid
from app.config import ALLOWED_EXTENSIONS,ALLOWED_SIZE,UPLOAD_DIR
from app.models import Contract
from app.database import contracts_collection, analysis_collection
from app.service.document_parser import extract_text
from bson import ObjectId

router = APIRouter(prefix="/contracts", tags=["Contracts"])


@router.post("/upload")
async def upload_contract(file: UploadFile = File(...)):
    '''Endpoint to upload a contract file (PDF or TXT) for analysis.'''
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and TXT files are allowed.")

    content = await file.read()
    size_mb = len(content) / (1024 * 1024)

    if size_mb > ALLOWED_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the 50 MB limit.")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    unique_filename = f"{uuid.uuid4()}{ext}"

    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    with open(file_path, "wb") as f:
        f.write(content)

    parsed = extract_text(file_path)

    contract_data = Contract(
        filename=unique_filename,
        original_filename=file.filename,
        text_content=parsed['text'] if isinstance(parsed, dict) else parsed,
        page_count= int(parsed['page_count']) if isinstance(parsed, dict) else len(parsed.splitlines()),
        word_count=int(parsed['word_count']) if isinstance(parsed, dict) else len(parsed.split()),
    )

    doc = contract_data.model_dump()
    result = contracts_collection.insert_one(doc)
    contract_data.id = str(result.inserted_id)

    return {
        'message': 'Contract uploaded and parsed successfully.',
        'contract': contract_data.model_dump(),
        'id': contract_data.id
    }


@router.get("/")
async def get_contracts():
    '''Endpoint to retrieve a list of all uploaded contracts.'''
    contracts = []
    for contract in contracts_collection.find({},{'text_content': 0}):
        doc = Contract(**contract)
        doc.id = str(contract["_id"])
        contracts.append(doc)
    return {
        'contracts': contracts
    }

@router.get("/{contract_id}")
async def get_contract_by_id(contract_id: str):
    '''Endpoint to retrieve the analysis of a specific contract by its ID.'''
    contract = contracts_collection.find_one({"_id": ObjectId(contract_id)})
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found.")
    doc = Contract(**contract)
    doc.id = str(contract["_id"])

    return {
        'contract': doc.model_dump()
    }






