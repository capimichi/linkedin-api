from typing import List, Optional

from pydantic import BaseModel

from linkedinapi.model.Company import Company
from linkedinapi.model.Hirer import Hirer


class JobPostingInfo(BaseModel):
    """
    Model representing detailed information about a job posting from LinkedIn.
    """
    id: Optional[int] = None
    title: Optional[str] = None
    company: Optional[Company] = None
    location: Optional[str] = None
    description: Optional[str] = None
    skills: List[str] = []
    is_simple: bool = False
    external_url: Optional[str] = None
    disabled: bool = False

    hirers: List[Hirer] = []


