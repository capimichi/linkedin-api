from typing import List, Optional
from pydantic import BaseModel

class Hirer(BaseModel):
    """
    Model representing detailed information about a hirer from LinkedIn.
    """
    url: Optional[str] = None
    name: Optional[str] = None
    role: Optional[str] = None

    def get_url(self) -> Optional[str]:
        return self.url

    def set_url(self, value: Optional[str]) -> None:
        self.url = value

    def get_name(self) -> Optional[str]:
        return self.name

    def set_name(self, value: Optional[str]) -> None:
        self.name = value

    def get_role(self) -> Optional[str]:
        return self.role

    def set_role(self, value: Optional[str]) -> None:
        self.role = value

