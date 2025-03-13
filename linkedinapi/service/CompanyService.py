from injector import inject

from linkedinapi.client.LinkedinClient import LinkedinClient
from linkedinapi.model.Company import Company


class CompanyService:

    @inject
    def __init__(self, linkedin_client: LinkedinClient):
        self.linkedin_client = linkedin_client

    async def get_company(self, username: str, company_slug: str) -> Company:
        return await self.linkedin_client.get_company(username, company_slug)
