from typing import Optional

from pydantic import BaseModel


class Company(BaseModel):
    """
    Model representing a company on LinkedIn.
    """
    slug: Optional[str] = None
    name: Optional[str] = None
    website: Optional[str] = None

    def get_slug(self) -> Optional[str]:
        return self.slug
    
    def set_slug(self, value: Optional[str]) -> None:
        self.slug = value
        
    def get_name(self) -> Optional[str]:
        return self.name

    def set_name(self, value: Optional[str]) -> None:
        self.name = value

    def get_website(self) -> Optional[str]:
        return self.website

    def set_website(self, value: Optional[str]) -> None:
        self.website = value
