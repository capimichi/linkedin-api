import json
import os
import time
from typing import List, Optional

from injector import inject
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from linkedinapi.factory.CompanyFactory import CompanyFactory
from linkedinapi.factory.HirerFactory import HirerFactory
from linkedinapi.factory.JobPostingInfoFactory import JobPostingInfoFactory
from linkedinapi.factory.JobPostingListingItemFactory import JobPostingListingItemFactory
from linkedinapi.model.Company import Company
from linkedinapi.model.CompanySinglePage import CompanySinglePage
from linkedinapi.model.Hirer import Hirer
from linkedinapi.model.HirerSinglePage import HirerSinglePage
from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.model.JobPostingListingItem import JobPostingListingItem
from linkedinapi.model.JobPostingSearchPage import JobPostingSearchPage
from linkedinapi.model.JobPostingSinglePage import JobPostingSinglePage
from linkedinapi.variable.SessionDirVariable import SessionDirVariable


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

    async def search(self, username: str, query: str, location: str, limit_first_page: bool = False,
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

            job_search_page = JobPostingSearchPage(page)
            await job_search_page.search_jobs(query, location, filter_date)

            job_postings = []
            has_next_page = True

            while has_next_page:
                job_cards = await job_search_page.get_job_cards()
                for job_card in job_cards:
                    job_posting = await JobPostingListingItemFactory.create_from_job_posting_search_card(job_card)
                    job_postings.append(job_posting)
                if limit_first_page:
                    has_next_page = False
                else:
                    has_next_page = await job_search_page.has_next_page()
                    if has_next_page:
                        await job_search_page.go_to_next_page()

            await browser.close()
            return job_postings

    async def get_job_posting(self, username: str, job_id: int) -> Optional[JobPostingInfo]:  # Return should be JobPostingInfo, needs import
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

    async def get_company(self, username: str, company_slug: str) -> Optional[Company]:
        """
        Get detailed information about a specific company.
        
        Args:
            username: LinkedIn username to load browser session
            company_slug: LinkedIn company slug
            
        Returns:
            CompanyInfo object containing detailed company information
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            session = await browser.new_context(storage_state=self.get_session_path(username))
            page = await session.new_page()

            # Navigate to company page
            company_url = f"https://www.linkedin.com/company/{company_slug}/"
            await page.goto(company_url)

            await page.wait_for_timeout(2000)

            company_single_page = CompanySinglePage(page)
            company_info = await CompanyFactory.create_from_company_single_page(company_single_page)

            await browser.close()
            return company_info

    async def get_hirer(self, username: str, hirer_slug: str) -> Optional[Hirer]:
        """
        Get detailed information about a specific hirer.
        
        Args:
            username: LinkedIn username to load browser session
            hirer_slug: LinkedIn hirer slug
            
        Returns:
            Hirer object containing detailed hirer information
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            session = await browser.new_context(storage_state=self.get_session_path(username))
            page = await session.new_page()

            # Navigate to hirer page
            hirer_url = f"https://www.linkedin.com/in/{hirer_slug}/"
            await page.goto(hirer_url)

            await page.wait_for_timeout(2000)

            hirer_single_page = HirerSinglePage(page)
            hirer_info = await HirerFactory.create_from_hirer_single_page(hirer_single_page)

            await browser.close()
            return hirer_info

    async def login(self, username: str, password: str) -> None:
        """
        Login to LinkedIn using provided credentials.
        
        Automates the login process and saves the session for future use.
        
        Args:
            username: LinkedIn username/email
            password: LinkedIn password
        """
        if self._is_already_logged_in(username):
            return
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=self.headless)
            session = await browser.new_context(storage_state=self.get_session_path(username))
            page = await session.new_page()
            
            # Navigate to login page
            await page.goto("https://www.linkedin.com/login")
            
            # Fill in credentials and submit
            await page.fill("input#username", username)
            await page.fill("input#password", password)
            await page.click("button[type=submit]")
            
            # Wait for login to complete
            await page.wait_for_timeout(50000)
            
            # Save session state for future use
            await page.context.storage_state(path=self.get_session_path(username))
            await browser.close()
