from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import createTable
from routes.reviews import router as revies_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    print('lifespan started')
    createTable()
    print('Database Tables Created')
    yield
    # Shutting down
    print('Shutting down')


app = FastAPI(
    title='Rangmanch Review API',
    description=(
        'Theatre reviews for Rangmanch plays'
    ),
    lifespan=lifespan
)

app.include_router(revies_router)


@app.get('/',tags=['system'])
def root():
    return {
        'message':'Welcome to Rangmanch API'
    }

