from typing import Optional

from pydantic import BaseModel


class Hirer(BaseModel):
    """
    Model representing a hirer on LinkedIn.
    """
    slug: Optional[str] = None
    name: Optional[str] = None
    position: Optional[str] = None

    def get_slug(self) -> Optional[str]:
        return self.slug
    
    def set_slug(self, value: Optional[str]) -> None:
        self.slug = value
        
    def get_name(self) -> Optional[str]:
        return self.name

    def set_name(self, value: Optional[str]) -> None:
        self.name = value

    def get_position(self) -> Optional[str]:
        return self.position

    def set_position(self, value: Optional[str]) -> None:
        self.position = value

