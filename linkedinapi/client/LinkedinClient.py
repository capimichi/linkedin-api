import asyncio

from injector import inject
from typing import List, Optional, Any

from playwright.async_api import async_playwright

from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.model.JobPostingListingItem import JobPostingListingItem
from linkedinapi.variable.SessionDirVariable import SessionDirVariable
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import os
import re
import json
import time
from linkedinapi.model.JobPostingSinglePage import JobPostingSinglePage
from linkedinapi.factory.JobPostingInfoFactory import JobPostingInfoFactory

class LinkedinClient:
    """
    LinkedIn client for interacting with LinkedIn's job search functionality.
    
    This class provides methods to search for jobs, get detailed job information,
    and authenticate with LinkedIn using Playwright for browser automation.
    """

    headless: bool = True

    @inject
    def __init__(self, session_dir: SessionDirVariable) -> None:
        """
        Initialize the LinkedIn client.
        
        Args:
            session_dir: Directory path where browser session data will be stored
        """
        self.session_dir = session_dir

    def get_session_path(self, username: str) -> str:
        """
        Get the path to the browser session file for a specific user.
        
        Creates an empty session file if it doesn't exist.
        
        Args:
            username: LinkedIn username
            
        Returns:
            Full path to the session file
        """
        p = os.path.join(self.session_dir, "linkedin_" + username + '.json')
        if not os.path.exists(p):
            with open(p, 'w') as f:
                f.write('{}')
        return p

    def _is_already_logged_in(self, username: str) -> bool:
        """
        Check if the user is already logged in by verifying the session file.
        
        Args:
            username: LinkedIn username
            
        Returns:
            True if the user is already logged in, False otherwise
        """
        session_path = self.get_session_path(username)
        if not os.path.exists(session_path):
            return False
        
        with open(session_path, 'r') as f:
            session_data = json.load(f)
        
        if 'cookies' not in session_data:
            return False
        
        current_time = time.time()
        for cookie in session_data['cookies']:
            if cookie.get('expires', 0) > current_time:
                return True
        
        return False



    def search(self, username: str, query: str, location: str, limit_first_page: bool = False, 
               filter_date: Optional[int] = None) -> List[JobPostingListingItem]:
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(self._search(username, query, location, limit_first_page, filter_date))


    async def _search(self, username: str, query: str, location: str, limit_first_page: bool = False,
               filter_date: Optional[int] = None) -> List[JobPostingListingItem]:
        """
        Search for job listings on LinkedIn with specified criteria.
        
        Args:
            username: LinkedIn username to load browser session
            query: Job search query (title, skill, or company)
            location: Location to search in
            limit_first_page: If True, only return results from the first page
            filter_date: Filter for job posting date (None=no filter, 1=24h, 2=week, etc.)
            
        Returns:
            List of job posting items matching the search criteria
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            session = await browser.new_context(storage_state=self.get_session_path(username))
            page = await session.new_page()

            # Navigate to LinkedIn jobs page
            jobs_url = "https://www.linkedin.com/jobs/"
            await page.goto(jobs_url)

            # Fill in job search query
            search_selector = 'input[aria-label="Cerca per qualifica, competenza o azienda"]'
            await page.wait_for_selector(search_selector)
            await page.fill(search_selector, query)

            await page.wait_for_timeout(500)

            # Fill in location
            location_selector = 'input[aria-label="Città, stato o CAP"]'
            await page.wait_for_selector(location_selector)
            await page.fill(location_selector, location)

            await page.wait_for_timeout(500)

            # Submit search
            await page.keyboard.press('Enter')
            await page.wait_for_timeout(5000)

            # Apply date filter if specified
            if filter_date:
                # Click on the date filter dropdown
                await page.click("#searchFilter_timePostedRange")
                await page.wait_for_timeout(1500)

                # Navigate to the filter options
                for i in range(2):
                    await page.keyboard.press('Tab')
                    await page.wait_for_timeout(500)

                # Select the appropriate date filter option
                for i in range(filter_date):
                    await page.keyboard.press('ArrowDown')
                    await page.wait_for_timeout(500)

                # Apply the filter
                for i in range(2):
                    await page.keyboard.press('Tab')
                    await page.wait_for_timeout(500)

                await page.keyboard.press('Enter')
                await page.wait_for_timeout(1500)

            has_next_page = True
            job_postings = []
            
            # Iterate through all result pages
            while has_next_page:
                # Scroll inside the job listings container to load all jobs
                scroll_container_selector = '.scaffold-layout__list'
                await page.wait_for_selector(scroll_container_selector)
                scroll_container_x = (await page.query_selector(scroll_container_selector)).bounding_box()['x']
                scroll_container_y = (await page.query_selector(scroll_container_selector)).bounding_box()['y']

                await page.mouse.move(scroll_container_x + 100, scroll_container_y + 100)
                await page.wait_for_timeout(1500)

                # Scroll down multiple times to ensure all content is loaded
                for i in range(8):
                    await page.mouse.wheel(0, 400)
                    await page.wait_for_timeout(500)

                # Select job card elements
                job_card_selector = '.job-card-container'
                job_footer_item_selector = '.job-card-container__footer-item time'
                            
                await page.wait_for_selector(job_card_selector)
                await page.wait_for_selector(job_footer_item_selector)
                
                job_cards = await page.query_selector_all(job_card_selector)

                # Extract data from each job card
                for job_card in job_cards:
                    job_posting = JobPostingListingItem()
                    
                    # Extract job ID
                    job_id = await job_card.get_attribute('data-job-id')
                    job_posting.id = job_id
                    
                    # Extract job title
                    job_title = (await job_card.query_selector('strong')).inner_text().strip()
                    job_posting.title = job_title

                    # Extract company name
                    job_company = (await job_card.query_selector('.artdeco-entity-lockup__subtitle')).inner_text().strip()
                    job_posting.company_name = job_company

                    # Extract datetime using regex
                    match = re.search(r'<time datetime="(.*?)"', await job_card.inner_html())
                    if match:
                        job_date = match.group(1)
                        job_posting.created_at = job_date

                    # Check if the job has simple application
                    is_simple = (await job_card.inner_text()).find('Candidatura semplice') != -1
                    job_posting.is_simple = is_simple

                    job_postings.append(job_posting)

                # Check if there is a next page or stop if limited to first page
                if limit_first_page:
                    has_next_page = False
                else:
                    next_page_selector = 'button[aria-label="Visualizza pagina successiva"]'
                    has_next_page = await page.query_selector(next_page_selector) is not None
                    if has_next_page:
                        await page.click(next_page_selector)
                        await page.wait_for_timeout(1000)

            await browser.close()
            return job_postings

    async def get_job_posting_info(self, username: str, job_id: int) -> Optional[JobPostingInfo]:  # Return should be JobPostingInfo, needs import
        """
        Get detailed information about a specific job posting.
        
        Args:
            username: LinkedIn username to load browser session
            job_id: LinkedIn job posting ID
            
        Returns:
            JobPostingInfo object containing detailed job information
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            session = await browser.new_context(storage_state=self.get_session_path(username))
            page = await session.new_page()

            # Navigate to job posting page
            job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
            await page.goto(job_url)

            job_posting_single_page = JobPostingSinglePage(page)
            job_posting_info = await JobPostingInfoFactory.create_from_job_posting_single_page(job_posting_single_page)

            await browser.close()
            return job_posting_info

    def login(self, username: str, password: str) -> None:
        """
        Login to LinkedIn using provided credentials.
        
        Automates the login process and saves the session for future use.
        
        Args:
            username: LinkedIn username/email
            password: LinkedIn password
        """
        if self._is_already_logged_in(username):
            return
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            session = browser.new_context(storage_state=self.get_session_path(username))
            page = session.new_page()
            
            # Navigate to login page
            page.goto("https://www.linkedin.com/login")
            
            # Fill in credentials and submit
            page.fill("input#username", username)
            page.fill("input#password", password)
            page.click("button[type=submit]")
            
            # Wait for login to complete
            page.wait_for_timeout(50000)
            
            # Save session state for future use
            page.context.storage_state(path=self.get_session_path(username))
            browser.close()

