from fastapi import FastAPI
from .routes.analyse import router as analyse_router
from .databse import create_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here
    print("Starting up the application...")
    create_tables()  # Create database tables on startup
    yield
    print("Shutting down the application...")


app = FastAPI(
    title="Netra Vision API",
    description="AI powered crop disease detection using Gemini Vision. Upload plant phots, get disease diagnosis and treatment recommendations.",
    version="1.0.0",
    lifespan = lifespan
)

app.include_router(analyse_router)


@app.get("/")
def root():
    return {
        "app":"Netra Vision",
        "endpoints":{
            "POST /analyse":"Upload an image for disease detection",
            "POST /analyse/batch":"Upload multiple images for disease detection",
            "GET /analyses":"Get a list of all analyses",
            "GET /analyses/{analysis_id}":"Get a specific analysis by ID",
        }
    }

