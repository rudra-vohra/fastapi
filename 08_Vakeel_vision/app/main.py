from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.database import init_db
from app.routes.contracts import router as contracts_router
from app.routes.analysis import router as analysis_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    init_db()
    yield
    print("Shutting down...")

app = FastAPI(
    title="Vakeel Vision API",
    description = "AI powered contract analysis using Gemini",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(contracts_router)
app.include_router(analysis_router)

@app.get("/")
async def root():
    return {
        'app': 'Vakeel Vision API',
        'version': '0.1.0',
        'endpoints':{
            "POST /contract/upload": "Upload a PDF or TXT contract for analysis",
            'GET /contracts': 'Retrieve a list of all uploaded contracts',
            'GET /contract/{contract_id}': 'Retrieve the analysis of a specific contract by its ID',
            'POST /analysis/analyse/{contract_id}': 'Analyze a specific contract using AI and return the results',
            'GET /analysis/{analysis_id}': 'Retrieve insights from the analysis of a specific contract by its ID',
            'GET /analysis/contract/{contract_id}': 'Retrieve all analyses for a specific contract by its ID'
        }
    }
