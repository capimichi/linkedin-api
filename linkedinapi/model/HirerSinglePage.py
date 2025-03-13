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

    async def get_position(self) -> Optional[str]:
        """
        Get the hirer position from the hirer page.

        :return: Hirer position as a string, or None if not found
        """
        position_selector = '.pv-top-card--list li:nth-child(2)'
        try:
            await self.page.wait_for_selector(position_selector, timeout=1000)
            position_element = await self.page.query_selector(position_selector)
            return (await position_element.inner_text()).strip()
        except Exception:
            return None
