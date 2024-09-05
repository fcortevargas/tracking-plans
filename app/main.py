from fastapi import FastAPI
from app.api.endpoints import router as api_router

app = FastAPI()

# Include the API router for sync
app.include_router(api_router, prefix="/api")


# Add a root route for basic information
@app.get("/")
def read_root():
    return {"message": "Welcome to the RudderStack Notion Sync API!"}
