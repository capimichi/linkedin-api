from typing import Optional

from pydantic import BaseModel


class Hirer(BaseModel):
    """
    Model representing detailed information about a hirer from LinkedIn.
    """
    slug: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None

    def get_slug(self) -> Optional[str]:
        return self.slug
    
    def set_slug(self, value: Optional[str]) -> None:
        self.slug = value
        
    def get_name(self) -> Optional[str]:
        return self.name

    def set_name(self, value: Optional[str]) -> None:
        self.name = value

    def get_role(self) -> Optional[str]:
        return self.role

    def set_role(self, value: Optional[str]) -> None:
        self.role = value

