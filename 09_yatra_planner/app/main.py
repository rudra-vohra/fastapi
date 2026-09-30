from fastapi import FastAPI
from .routes.planner import router as planner_router
from .routes.stream import router as stream_router

app = FastAPI(
    title="Yatra Planner API",
    description="Aggregate travel data from multiple sources to provide single plan with SSE support",
    version="1.0.0",
)

app.include_router(planner_router)
app.include_router(stream_router)


@app.get("/",tags=["System"])
def read_root():
    return {
        "message": "Welcome to the Yatra Planner API!",
        'app':'Yatra Planner API',
        'version':'1.0.0',
        'endpoints': {
            'POST /plan': 'Create a travel plan (Aggregated)',
            'GET /plan/stream': 'Stream  a travel plan (SSE)',
            'GET /plan/cache-stats':'View cache statistics for travel plans',
            'DELETE /plan/cache':'Clear cache for travel plans'
        }
    }






