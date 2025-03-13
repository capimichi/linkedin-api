from typing import Optional

from playwright.async_api import Page


class HirerSinglePage:
    """
    A class to represent a single hirer page on LinkedIn.
    """

    def __init__(self, page: Page):
        """
        Initialize the HirerSinglePage with a Playwright Page object.

        :param page: Playwright Page object
        """
        self.page = page

    async def get_name(self) -> Optional[str]:
        """
        Get the hirer name from the hirer page.

        :return: Hirer name as a string, or None if not found
        """
        name_selector = 'h1'
        try:
            await self.page.wait_for_selector(name_selector, timeout=1000)
            name_element = await self.page.query_selector(name_selector)
            return (await name_element.inner_text()).strip()
        except Exception:
            return None

    async def get_slug(self) -> Optional[str]:
        """
        Get the hirer slug from the hirer page.

        :return: Hirer slug as a string, or None if not found
        """
        try:
            return self.page.url.split('in/')[1].split('/')[0]
        except Exception:
            return None

    async def get_location(self) -> Optional[str]:
        """
        Get the hirer location from the hirer page.

        :return: Hirer location as a string, or None if not found
        """
        location_selector = '.text-body-small.inline.t-black--light.break-words'
        try:
            await self.page.wait_for_selector(location_selector, timeout=1000)
            location_element = await self.page.query_selector(location_selector)
            return (await location_element.inner_text()).strip()
        except Exception:
            return None

    async def get_role(self) -> Optional[str]:
        """
        Get the hirer role from the hirer page.

        :return: Hirer role as a string, or None if not found
        """
        role_selector = '.text-body-medium.break-words'
        try:
            await self.page.wait_for_selector(role_selector, timeout=1000)
            role_element = await self.page.query_selector(role_selector)
            return (await role_element.inner_text()).strip()
        except Exception:
            return None
