from typing import List, Optional

from playwright.async_api import Page

from linkedinapi.model.JobPostingSearchCard import JobPostingSearchCard


class JobPostingSearchPage:
    def __init__(self, page: Page):
        self.page = page

    async def search_jobs(self, query: str, location: str, filter_date: Optional[int] = None) -> None:
        jobs_url = "https://www.linkedin.com/jobs/search"
        await self.page.goto(jobs_url)

        search_selector = 'input[aria-label="Cerca per qualifica, competenza o azienda"]'
        await self.page.wait_for_selector(search_selector)
        await self.page.fill(search_selector, query)
        await self.page.wait_for_timeout(500)

        location_selector = 'input[aria-label="Città, stato o CAP"]'
        await self.page.wait_for_selector(location_selector)
        await self.page.fill(location_selector, location)
        await self.page.wait_for_timeout(500)

        await self.page.keyboard.press('Enter')
        await self.page.wait_for_timeout(5000)

        if filter_date:
            await self.page.click("#searchFilter_timePostedRange")
            await self.page.wait_for_timeout(1500)
            for i in range(2):
                await self.page.keyboard.press('Tab')
                await self.page.wait_for_timeout(500)
            for i in range(filter_date):
                await self.page.keyboard.press('ArrowDown')
                await self.page.wait_for_timeout(500)
            for i in range(2):
                await self.page.keyboard.press('Tab')
                await self.page.wait_for_timeout(500)
            await self.page.keyboard.press('Enter')
            await self.page.wait_for_timeout(1500)

    async def get_job_cards(self) -> List[JobPostingSearchCard]:
        job_cards = []
        scroll_container_selector = '.scaffold-layout__list'
        await self.page.wait_for_selector(scroll_container_selector)
        scroll_container = await self.page.query_selector(scroll_container_selector)
        scroll_container_bounds = await scroll_container.bounding_box()
        scroll_container_x = scroll_container_bounds['x']
        scroll_container_y = scroll_container_bounds['y']

        await self.page.mouse.move(scroll_container_x + 100, scroll_container_y + 100)
        await self.page.wait_for_timeout(1500)

        for i in range(8):
            await self.page.mouse.wheel(0, 400)
            await self.page.wait_for_timeout(500)

        job_card_selector = '.job-card-container'
        await self.page.wait_for_selector(job_card_selector)
        job_card_elements = await self.page.query_selector_all(job_card_selector)

        for job_card_element in job_card_elements:
            job_card = JobPostingSearchCard(job_card_element)
            job_cards.append(job_card)

        return job_cards

    async def has_next_page(self) -> bool:
        next_page_selector = 'button[aria-label="Visualizza pagina successiva"]'
        return await self.page.query_selector(next_page_selector) is not None

    async def go_to_next_page(self) -> None:
        next_page_selector = 'button[aria-label="Visualizza pagina successiva"]'
        await self.page.click(next_page_selector)
        await self.page.wait_for_timeout(1000)
