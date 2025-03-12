from typing import Optional
from pydantic import BaseModel

class JobPostingRequest(BaseModel):
    """
    Model for job posting request parameters.
    """
    username: str
    job_id: str
