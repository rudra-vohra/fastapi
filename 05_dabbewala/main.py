from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_table
from routes.orders import router as orders_router
from routes.stats import router as stats_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    print("Starting up the Dabbewala API...")
    create_table()
    print("Database tables created.")  # Create the database tables if they don't exist
    yield

    # Shutdown tasks can be performed here if needed
    print("Shutting down the Dabbewala API...")


app = FastAPI(
    title="Dabbewala API",
    description=(
        "This API provides information about the Dabbewala order services, including order creation, status updates, and tracking."
    ),
    lifespan = lifespan
)


app.include_router(orders_router)
app.include_router(stats_router)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Dabbewala API!"
    }

