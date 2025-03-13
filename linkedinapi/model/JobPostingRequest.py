from pydantic import BaseModel

class JobPostingRequest(BaseModel):
    """
    Model for job posting request parameters.
    """
    username: str
    job_id: int

    def get_username(self) -> str:
        """
        Get the username from the request.

        Returns:
            str: LinkedIn username
        """
        return self.username

    def get_job_id(self) -> int:
        """
        Get the job ID from the request.

        Returns:
            int: LinkedIn job ID
        """
        return self.job_id