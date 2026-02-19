from fastapi import FastAPI, Depends, HTTPException
from contextlib import asynccontextmanager
from fda_client import FDAClient

# Global client instance
fda_client: FDAClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    Initializes the FDAClient on startup and closes it on shutdown.
    """
    global fda_client
    # Initialize the client. Pass API key if you have one, e.g., from environment variables.
    fda_client = FDAClient(api_key=None) 
    yield
    # Clean up resources
    if fda_client:
        await fda_client.close()

app = FastAPI(title="FDA API Service", lifespan=lifespan)

# Dependency to get the FDA client instance
def get_fda_client() -> FDAClient:
    if fda_client is None:
        raise HTTPException(status_code=500, detail="FDA Client not initialized")
    return fda_client

@app.get("/")
async def root():
    return {"message": "FDA API Service is running"}

# TODO: Define your API endpoints here.
# Example usage in an endpoint:
# 
# @app.get("/example-fetch")
# async def fetch_example(client: FDAClient = Depends(get_fda_client)):
#     data = await client.fetch_data("drug/event.json", params={"limit": 1})
#     return data
