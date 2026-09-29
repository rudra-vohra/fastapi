from fastapi import FastAPI
from routes.chat import router as chat_router

app = FastAPI(
    title="RAG Practice API",
    description="API for RAG Practice",
)

app.include_router(chat_router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the RAG Practice API!"}

