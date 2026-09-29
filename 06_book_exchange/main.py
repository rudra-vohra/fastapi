from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from routes.book_routes import router as book_router
from routes.user_routes import router as user_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    create_tables()
    print('database tables created')
    yield

    print('Shutting down...')

app = FastAPI(
    title="Book Exchange API",
    description="A simple book exchange API",
    version="0.1.0",
    lifespan = lifespan,
)

app.include_router(book_router)
app.include_router(user_router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Book Exchange API!",
    }

