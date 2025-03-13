from injector import inject

from linkedinapi.client.LinkedinClient import LinkedinClient
from linkedinapi.model.Hirer import Hirer


class HirerService:

    @inject
    def __init__(self, linkedin_client: LinkedinClient):
        self.linkedin_client = linkedin_client

    async def get_hirer(self, username: str, hirer_slug: str) -> Hirer:
        return await self.linkedin_client.get_hirer(username, hirer_slug)
