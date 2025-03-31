from fastapi import FastAPI
from .api.v1 import endpoints as v1_endpoints
from .core.config import settings

# Initialize FastAPI app using settings
app = FastAPI(title=settings.PROJECT_NAME)

# Include API routers
app.include_router(v1_endpoints.router, prefix=settings.API_V1_STR)

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

# Note: The main guard below is primarily for debugging.
# In production, use `just run` or Docker/Compose which calls uvicorn directly.
if __name__ == "__main__":
    import uvicorn
    # Use settings for host/port when running directly
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
