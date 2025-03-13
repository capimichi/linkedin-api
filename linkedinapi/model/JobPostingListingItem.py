from typing import Optional, List

from pydantic import BaseModel


class JobPostingListingItem(BaseModel):
    """
    Model representing a job posting listing item from LinkedIn search results.
    """
    id: Optional[int] = None
    title: Optional[str] = None
    company_name: Optional[str] = None
    metadata_items: List[str] = []
    created_at: Optional[str] = None
    is_simple: bool = False


