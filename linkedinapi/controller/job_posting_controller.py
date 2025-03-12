from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.helper.TokenHelper import TokenHelper
from linkedinapi.service.JobPostingService import JobPostingService
from linkedinapi.model.JobPostingRequest import JobPostingRequest
from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.controller import get_current_username

job_posting_controller = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
)

@job_posting_controller.get("/{job_id}")
async def get_job_details(job_id: int, username: str = Depends(get_current_username)) -> JobPostingInfo:
    """
    Get detailed information about a specific job posting.
    
    Args:
        job_id: LinkedIn job posting ID
        username: LinkedIn username to load browser session
        
    Returns:
        JobPostingInfo object containing detailed job information
    """

    default_container: DefaultContainer = DefaultContainer.getInstance()
    job_posting_service: JobPostingService = default_container.get(JobPostingService)
    
    try:
        job_details = await job_posting_service.get_job_details(username, job_id)
        return job_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job details: {str(e)}")
