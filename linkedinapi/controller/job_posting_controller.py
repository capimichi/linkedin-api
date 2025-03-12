from fastapi import APIRouter, HTTPException, Depends
from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.service.JobPostingService import JobPostingService
from linkedinapi.model.JobPostingRequest import JobPostingRequest
from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.util.TokenUtil import TokenUtil
from linkedinapi.controller import security_scheme

job_posting_controller = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)

@job_posting_controller.get("/{job_id}")
async def get_job_details(job_id: str, token: str = Depends(security_scheme)):
    """
    Get detailed information about a specific job posting.
    
    Args:
        job_id: LinkedIn job posting ID
        token: Bearer token containing the username
        
    Returns:
        JobPostingInfo object containing detailed job information
    """
    try:
        username = TokenUtil.decode_token(token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    default_container: DefaultContainer = DefaultContainer.getInstance()
    job_posting_service: JobPostingService = default_container.get(JobPostingService)
    
    try:
        job_details = job_posting_service.get_job_details(username, job_id)
        return job_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job details: {str(e)}")

@job_posting_controller.post("/details")
async def get_job_details_by_post(request: JobPostingRequest, token: str = Depends(security_scheme)):
    """
    Get detailed information about a job posting using POST request.
    
    Args:
        request: Job posting request containing job_id
        token: Bearer token containing the username
        
    Returns:
        JobPostingInfo object containing detailed job information
    """
    try:
        username = TokenUtil.decode_token(token)
        print(username)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
    
    default_container: DefaultContainer = DefaultContainer.getInstance()
    job_posting_service: JobPostingService = default_container.get(JobPostingService)
    
    try:
        job_details = job_posting_service.get_job_details(username, request.job_id)
        return job_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job details: {str(e)}")
