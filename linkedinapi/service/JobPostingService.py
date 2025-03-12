from injector import inject
from linkedinapi.client.LinkedinClient import LinkedinClient
from linkedinapi.model.JobPostingInfo import JobPostingInfo

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
    
    def get_job_details(self, username: str, job_id: str) -> JobPostingInfo:
        """
        Get detailed information about a specific job posting.
        
        Args:
            username: LinkedIn username to load browser session
            job_id: LinkedIn job posting ID
            
        Returns:
            JobPostingInfo object containing detailed job information
        """
        return self.linkedin_client.get_job_posting_info(username, job_id)
    
