from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlmodel import Session,select
import uuid
from ..services.image import validate_image, resize_image_if_needed, save_image
from ..services.vision import analyse_image as analyse_image_service
from ..databse import get_session
from ..models import Result,Analysis

router = APIRouter(
    prefix="/analyse",
    tags=["Analysis"]
)

async def process_single_image(file: UploadFile):
    '''Process a single image for disease detection'''

    content = await file.read()

    validation_result = validate_image(content, file.content_type)
    if not validation_result["is_valid"]:
        raise HTTPException(status_code=400, detail=validation_result["message"])

    processed = resize_image_if_needed(content)

    extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    unique_name = f"{uuid.uuid4().hex}.{extension}"

    path = save_image(processed, "uploads", unique_name)

    result = await analyse_image_service(path, file.content_type)
    return result


@router.post("/")
async def analyse_image(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
    ):
    '''Analyse a single image for disease detection'''
    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")

    # Here you would add the logic to send the image to the Gemini Vision API for analysis
    result = Result(**await process_single_image(file))

    db_analysis = Analysis(
        image_name=file.filename,
        result=result.model_dump()
    )
    session.add(db_analysis)
    session.commit()
    session.refresh(db_analysis)

    return {
        "message": "Image analysis completed successfully.",
        "result": result,
    }

@router.post("/batch")
async def analyse_images_batch(
    files: list[UploadFile] = File(...),
    session: Session = Depends(get_session)
):
    '''Analyse multiple images for disease detection'''
    results = []
    for file in files:
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"Invalid file type for {file.filename}. Please upload an image.")
        result = Result(**await process_single_image(file))
        db_analysis = Analysis(
            image_name=file.filename,
            result=result.model_dump()
        )
        session.add(db_analysis)
        session.commit()
        session.refresh(db_analysis)
        results.append(result)

    return {
        "message": "Batch image analysis completed successfully.",
        "results": results,
    }   

@router.get("/analyses")
def get_all_analyses(session: Session = Depends(get_session)):
    '''Get a list of all analyses'''
    query = select(Analysis)
    analyses = session.exec(query).all()
    if not analyses:
        raise HTTPException(status_code=404, detail="No analyses found")
    return analyses

@router.get("/analyses/{analysis_id}")
def get_analysis_by_id(analysis_id: int, session: Session = Depends(get_session)):
    '''Get a specific analysis by ID'''
    query = select(Analysis).where(Analysis.id == analysis_id)
    analysis = session.exec(query).first()
    if analysis is None:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis



