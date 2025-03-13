import uvicorn
from fastapi import FastAPI
from starlette.responses import RedirectResponse

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.controller.company_controller import company_controller
from linkedinapi.controller.hirer_controller import hirer_controller
from linkedinapi.controller.job_posting_controller import job_posting_controller
from linkedinapi.controller.login_controller import login_controller

default_container: DefaultContainer = DefaultContainer.getInstance()

# Initialize FastAPI app
app = FastAPI(
    title="LinkedIn API",
    description="API for interacting with LinkedIn data",
    version="1.0.0",
    servers=[
        {
            "url": default_container.get_var('api_base_url'),
            "description": "Server"
        },
    ]
)

# Root endpoint
@app.get("/")
async def root():
    # please redirect to the documentation
    return RedirectResponse(url="/docs")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(login_controller)
app.include_router(job_posting_controller)
app.include_router(company_controller)
app.include_router(hirer_controller)

# Run the application (for development)
if __name__ == "__main__":
    host = default_container.get_var('api_host')
    port = default_container.get_var('api_port')
    uvicorn.run(
        app,
        host=host,
        port=port,
    )
