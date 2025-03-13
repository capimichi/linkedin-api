from playwright.async_api import ElementHandle
import re

class JobPostingSearchCard:
    def __init__(self, element_handle: ElementHandle):
        self.element_handle = element_handle

    async def get_id(self) -> str:
        return await self.element_handle.get_attribute('data-job-id')

    async def get_title(self) -> str:
        title_element = await self.element_handle.query_selector('strong')
        return (await title_element.inner_text()).strip()

    async def get_company_name(self) -> str:
        company_element = await self.element_handle.query_selector('.artdeco-entity-lockup__subtitle')
        return (await company_element.inner_text()).strip()

    async def get_created_at(self) -> str:
        match = re.search(r'<time datetime="(.*?)"', await self.element_handle.inner_html())
        return match.group(1) if match else None

    async def is_simple_application(self) -> bool:
        return 'Candidatura semplice' in await self.element_handle.inner_text()
