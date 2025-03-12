from typing import Optional
from pydantic import BaseModel

class JobPostingListingItem(BaseModel):
    """
    Model representing a job posting listing item from LinkedIn search results.
    """
    id: Optional[str] = None
    title: Optional[str] = None
    company_name: Optional[str] = None
    created_at: Optional[str] = None
    is_simple: bool = False


