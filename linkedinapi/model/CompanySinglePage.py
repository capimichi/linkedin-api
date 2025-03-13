from typing import Optional

from playwright.async_api import Page

class CompanySinglePage:
    """
    A class to represent a single company page on LinkedIn.
    """

    def __init__(self, page: Page):
        """
        Initialize the CompanySinglePage with a Playwright Page object.

        :param page: Playwright Page object
        """
        self.page = page

    async def get_name(self) -> Optional[str]:
        """
        Get the company name from the company page.

        :return: Company name as a string, or None if not found
        """
        name_selector = '.org-top-card-summary__title'
        try:
            await self.page.wait_for_selector(name_selector, timeout=1000)
            name_element = await self.page.query_selector(name_selector)
            return (await name_element.inner_text()).strip()
        except Exception:
            return None

    async def get_description(self) -> Optional[str]:
        """
        Get the company description from the company page.

        :return: Company description as a string, or None if not found
        """
        description_selector = '.org-top-card-summary__tagline'
        try:
            await self.page.wait_for_selector(description_selector, timeout=1000)
            description_element = await self.page.query_selector(description_selector)
            return (await description_element.inner_text()).strip()
        except Exception:
            return None

    async def get_website(self) -> Optional[str]:
        """
        Get the company website from the company page.

        :return: Company website as a string, or None if not found
        """
        website_selector = '.org-about-company-module__company-page-url'
        try:
            await self.page.wait_for_selector(website_selector, timeout=1000)
            website_element = await self.page.query_selector(website_selector)
            return (await website_element.inner_text()).strip()
        except Exception:
            return None

    async def get_industry(self) -> Optional[str]:
        """
        Get the company industry from the company page.

        :return: Company industry as a string, or None if not found
        """
        industry_selector = '.org-about-company-module__industry'
        try:
            await self.page.wait_for_selector(industry_selector, timeout=1000)
            industry_element = await self.page.query_selector(industry_selector)
            return (await industry_element.inner_text()).strip()
        except Exception:
            return None

    async def get_company_size(self) -> Optional[str]:
        """
        Get the company size from the company page.

        :return: Company size as a string, or None if not found
        """
        size_selector = '.org-about-company-module__company-size-definition-text'
        try:
            await self.page.wait_for_selector(size_selector, timeout=1000)
            size_element = await self.page.query_selector(size_selector)
            return (await size_element.inner_text()).strip()
        except Exception:
            return None

    async def get_headquarters(self) -> Optional[str]:
        """
        Get the company headquarters from the company page.

        :return: Company headquarters as a string, or None if not found
        """
        headquarters_selector = '.org-about-company-module__headquarters'
        try:
            await self.page.wait_for_selector(headquarters_selector, timeout=1000)
            headquarters_element = await self.page.query_selector(headquarters_selector)
            return (await headquarters_element.inner_text()).strip()
        except Exception:
            return None
