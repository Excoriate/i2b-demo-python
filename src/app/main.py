from fastapi import FastAPI

# TODO: Import API routers once created, e.g.:
# from .api.v1 import endpoints as v1_endpoints
# from .core.config import settings # Assuming settings are loaded here

# Initialize FastAPI app
# TODO: Add project metadata like title, version from pyproject.toml or settings
app = FastAPI(title="i2b-demo-python API")

# TODO: Include API routers
# app.include_router(v1_endpoints.router, prefix="/api/v1")

@app.get("/")
async def read_root():
    """
    Root endpoint providing a welcome message.
    """
    return {"message": "Welcome to the i2b-demo-python API"}

# Placeholder for startup/shutdown events if needed
# @app.on_event("startup")
# async def startup_event():
#     # Initialize DB connection, etc.
#     pass

# @app.on_event("shutdown")
# async def shutdown_event():
#     # Close DB connection, etc.
#     pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
