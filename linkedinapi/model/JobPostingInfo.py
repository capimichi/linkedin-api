from typing import List, Optional
from pydantic import BaseModel

class JobPostingInfo(BaseModel):
    """
    Model representing detailed information about a job posting from LinkedIn.
    """
    id: str
    title: Optional[str] = None
    company_name: Optional[str] = None
    company_slug: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills: List[str] = []
    is_simple: bool = False
    external_url: Optional[str] = None
    disabled: bool = False


