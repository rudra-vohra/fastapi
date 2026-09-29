from fastapi import FastAPI
import uvicorn

# inside FastAPI function the data inserted is used for the docs preperation 
app = FastAPI(
    title="basic test app",
    description=(
        "learning fastAPI"
    ),
    version="1.1.2",
    docs_url="/docs",
    redoc_url="/redoc"
)

@app.get("/")
def read_root():
    '''Root endpoint - Health Check'''

    # FastAPI automatically converts the dict into JSON
    return {
        "message":"The servers is up and running",
        "status":"healthy"
    }

# Additional info for the docs purpose
@app.get(
    "/users/active",
    summary="Get active users",
    description=(
        "Fetches all the currently active users"
    ),
    tags=["users"],
    response_description="List of all currently active users",
    deprecated=False,
)
def list_active_users():
    return [
        {"id": 1,"name" : "John"},
        {"id": 2,"name" : "Jack"},
        {"id": 3,"name" : "Will"},
    ]


# ONE OF THE WAYS TO RUN THE UVICORN SERVER WITHOUT USING TERMINAL
"""
if __name__ == "__main__":
    uvicorn.run("main:app",host="127.0.0.1",port=8000,reload=True)

"""