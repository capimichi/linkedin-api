from typing import Optional, List

from fastapi import APIRouter, HTTPException, Depends

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.controller import get_current_username
from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.model.JobPostingListingItem import JobPostingListingItem
from linkedinapi.service.JobPostingService import JobPostingService

job_posting_controller = APIRouter(
    prefix="/job-postings",
    tags=["Job postings"],
)


@job_posting_controller.get("/{job_id}")
async def get_job_posting(job_id: int, username: str = Depends(get_current_username)) -> JobPostingInfo:
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
        job_details = await job_posting_service.get_job_posting(username, job_id)
        return job_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job details: {str(e)}")


@job_posting_controller.get("/")
async def get_job_postings(query: str, location: str, limit_first_page: bool = True, date_filter: Optional[int] = None,
                           username: str = Depends(get_current_username)) -> List[JobPostingListingItem]:
    """
    Get a list of job postings based on search criteria.
    
    Args:
        query: Search query for job postings
        location: Location filter for job postings
        limit_first_page: Flag to limit search to first page of results
        date_filter: Date filter for job postings
        username: LinkedIn username to load browser session
        
    Returns:
        List of JobPostingInfo objects containing job posting information
    """

    default_container: DefaultContainer = DefaultContainer.getInstance()
    job_posting_service: JobPostingService = default_container.get(JobPostingService)

    try:
        job_postings = await job_posting_service.get_job_posting_listing_items(
            username,
            query,
            location,
            limit_first_page,
            date_filter
        )
        return job_postings
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving job postings: {str(e)}")
