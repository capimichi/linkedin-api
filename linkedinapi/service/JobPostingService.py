from typing import List, Optional

from injector import inject

from linkedinapi.client.LinkedinClient import LinkedinClient
from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.model.JobPostingListingItem import JobPostingListingItem


class JobPostingService:
    """
    Service for retrieving and processing job posting information.
    """
    
    @inject
    def __init__(self, linkedin_client: LinkedinClient):
        """
        Initialize the job posting service with LinkedIn client dependency.
        
        Args:
            linkedin_client: Client for interacting with LinkedIn
        """
        self.linkedin_client = linkedin_client
    
    async def get_job_posting(self, username: str, job_id: int) -> JobPostingInfo:
        """
        Get detailed information about a specific job posting.
        
        Args:
            username: LinkedIn username to load browser session
            job_id: LinkedIn job posting ID
            
        Returns:
            JobPostingInfo object containing detailed job information
        """
        return await self.linkedin_client.get_job_posting(username, job_id)

    async def get_job_posting_listing_items(self, username: str, query: str, location: str, limit_first_page: bool, date_filter: Optional[int]) -> List[JobPostingListingItem]:
        """
        Get a list of job postings based on search criteria.

        Args:
            username: LinkedIn username to load browser session
            query: Search query for job postings
            location: Location filter for job postings
            limit_first_page: Flag to limit search to first page of results
            date_filter: Date filter for job postings

        Returns:
            List of JobPostingInfo objects containing job posting information
        """
        return await self.linkedin_client.search(
            username,
            query,
            location,
            limit_first_page,
            date_filter
        )
    
