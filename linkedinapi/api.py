from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
import uvicorn

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.controller.login_controller import login_controller
from linkedinapi.controller.job_posting_controller import job_posting_controller

default_container: DefaultContainer = DefaultContainer.getInstance()

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn API",
    description="API for interacting with LinkedIn data",
    version="1.0.0",
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "LinkedIn API is running"}

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(login_controller)
app.include_router(job_posting_controller)

# Run the application (for development)
if __name__ == "__main__":
    host = default_container.get_var('api_host')
    port = default_container.get_var('api_port')
    uvicorn.run(
        app,
        host=host,
        port=port,
    )
