from injector import inject
from typing import List, Optional, Any
from linkedinapi.model.JobPostingListingItem import JobPostingListingItem
from linkedinapi.variable.SessionDirVariable import SessionDirVariable
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
import os
import re
import json
import time

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
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            session = browser.new_context(storage_state=self.get_session_path(username))
            page = session.new_page()

            # Navigate to LinkedIn jobs page
            jobs_url = "https://www.linkedin.com/jobs/"
            page.goto(jobs_url)

            # Fill in job search query
            search_selector = 'input[aria-label="Cerca per qualifica, competenza o azienda"]'
            page.wait_for_selector(search_selector)
            page.fill(search_selector, query)

            page.wait_for_timeout(500)

            # Fill in location
            location_selector = 'input[aria-label="Città, stato o CAP"]'
            page.wait_for_selector(location_selector)
            page.fill(location_selector, location)

            page.wait_for_timeout(500)

            # Submit search
            page.keyboard.press('Enter')
            page.wait_for_timeout(5000)

            # Apply date filter if specified
            if filter_date:
                # Click on the date filter dropdown
                page.click("#searchFilter_timePostedRange")
                page.wait_for_timeout(1500)

                # Navigate to the filter options
                for i in range(2):
                    page.keyboard.press('Tab')
                    page.wait_for_timeout(500)

                # Select the appropriate date filter option
                for i in range(filter_date):
                    page.keyboard.press('ArrowDown')
                    page.wait_for_timeout(500)

                # Apply the filter
                for i in range(2):
                    page.keyboard.press('Tab')
                    page.wait_for_timeout(500)

                page.keyboard.press('Enter')
                page.wait_for_timeout(1500)

            has_next_page = True
            job_postings = []
            
            # Iterate through all result pages
            while has_next_page:
                # Scroll inside the job listings container to load all jobs
                scroll_container_selector = '.scaffold-layout__list'
                page.wait_for_selector(scroll_container_selector)
                scroll_container_x = page.query_selector(scroll_container_selector).bounding_box()['x']
                scroll_container_y = page.query_selector(scroll_container_selector).bounding_box()['y']

                page.mouse.move(scroll_container_x + 100, scroll_container_y + 100)
                page.wait_for_timeout(1500)

                # Scroll down multiple times to ensure all content is loaded
                for i in range(8):
                    page.mouse.wheel(0, 400)
                    page.wait_for_timeout(500)

                # Select job card elements
                job_card_selector = '.job-card-container'
                job_footer_item_selector = '.job-card-container__footer-item time'
                            
                page.wait_for_selector(job_card_selector)
                page.wait_for_selector(job_footer_item_selector)
                
                job_cards = page.query_selector_all(job_card_selector)

                # Extract data from each job card
                for job_card in job_cards:
                    job_posting = JobPostingListingItem()
                    
                    # Extract job ID
                    job_id = job_card.get_attribute('data-job-id')
                    job_posting.id = job_id
                    
                    # Extract job title
                    job_title = job_card.query_selector('strong').inner_text().strip()
                    job_posting.title = job_title

                    # Extract company name
                    job_company = job_card.query_selector('.artdeco-entity-lockup__subtitle').inner_text().strip()
                    job_posting.company_name = job_company

                    # Extract datetime using regex
                    match = re.search(r'<time datetime="(.*?)"', job_card.inner_html())
                    if match:
                        job_date = match.group(1)
                        job_posting.created_at = job_date

                    # Check if the job has simple application
                    is_simple = job_card.inner_text().find('Candidatura semplice') != -1
                    job_posting.is_simple = is_simple

                    job_postings.append(job_posting)

                # Check if there is a next page or stop if limited to first page
                if limit_first_page:
                    has_next_page = False
                else:
                    next_page_selector = 'button[aria-label="Visualizza pagina successiva"]'
                    has_next_page = page.query_selector(next_page_selector) is not None
                    if has_next_page:
                        page.click(next_page_selector)
                        page.wait_for_timeout(1000)

            browser.close()
            return job_postings
            
    def get_job_posting_info(self, username: str, job_id: str) -> Any:  # Return should be JobPostingInfo, needs import
        """
        Get detailed information about a specific job posting.
        
        Args:
            username: LinkedIn username to load browser session
            job_id: LinkedIn job posting ID
            
        Returns:
            JobPostingInfo object containing detailed job information
        """
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=self.headless)
            session = browser.new_context(storage_state=self.get_session_path(username))
            page = session.new_page()

            # Navigate to job posting page
            job_url = f"https://www.linkedin.com/jobs/view/{job_id}/"
            page.goto(job_url)

            job_posting = JobPostingInfo()  # This class needs to be imported
            job_posting.id = job_id

            # Check if job posting is not found
            job_not_found_selector = '.jobs-no-job__error-msg'
            if(page.query_selector(job_not_found_selector)):
                job_posting.disabled = True
                browser.close()
                return job_posting

            # Extract job title
            job_title_selector = '.artdeco-card h1'
            try:
                page.wait_for_selector(job_title_selector, timeout=1000)
                job_posting.title = page.query_selector(job_title_selector).inner_text().strip()
            except Exception as e:
                pass

            # Extract job location
            job_location_selector = '.job-details-jobs-unified-top-card__primary-description-container .tvm__text:first-child'
            try:
                page.wait_for_selector(job_location_selector, timeout=1000)
                job_posting.location = page.query_selector(job_location_selector).inner_text().strip()
            except Exception as e:
                pass

            # Extract job description
            job_description_selector = '.jobs-box__html-content p'
            try:
                page.wait_for_selector(job_description_selector, timeout=1000)
                job_posting.description = page.query_selector(job_description_selector).inner_text().strip()
            except Exception as e:
                pass

            # Extract required skills
            job_skills_selector = '.job-details-how-you-match__skills-item-subtitle'
            try:
                page.wait_for_selector(job_skills_selector, timeout=1000)
                job_skills_objects = page.query_selector_all(job_skills_selector)
            except Exception as e:
                job_skills_objects = []

            # Process and normalize skills list
            skills = []
            for job_skills_object in job_skills_objects:
                job_skills = job_skills_object.inner_text().strip()
                job_skills = job_skills.split(',')
                for job_skill in job_skills:
                    is_last_skill = job_skill == job_skills[-1]
                    if not is_last_skill:
                        skills.append(job_skill.strip())
                    else:
                        # Handle skills separated by "e" (Italian for "and")
                        split_skill = job_skill.split(' e ')
                        for s in split_skill:
                            skills.append(s.strip())

            # Extract additional skills
            additional_skills_selector = '.job-details-how-you-match__skills-section-descriptive-skill'
            try:
                page.wait_for_selector(additional_skills_selector, timeout=1000)
                additional_skills_object = page.query_selector(additional_skills_selector)
                if additional_skills_object:
                    additional_skills = additional_skills_object.inner_text().strip()
                    additional_skills = additional_skills.split('·')
                    for additional_skill in additional_skills:
                        skills.append(additional_skill.strip())
            except Exception as e:
                pass
            
            job_posting.skills = skills

            # Extract company information
            company_url_selector = '.job-details-jobs-unified-top-card__company-name a'
            try:
                page.wait_for_selector(company_url_selector, timeout=1000)
                company_name = page.query_selector(company_url_selector).inner_text().strip()
                company_url = page.query_selector(company_url_selector).get_attribute('href')
                # Extract company slug from URL
                company_slug = company_url.split('company/')[1].split('/')[0]
                job_posting.company_slug = company_slug
                job_posting.company_name = company_name
            except Exception as e:
                pass
            
            # Check if job listing is disabled
            is_disabled = False
            job_disabled_selector = '.artdeco-inline-feedback__message'
            if(page.query_selector(job_disabled_selector)):
                job_disabled_text = page.query_selector(job_disabled_selector).inner_text().strip().lower()
                is_disabled = job_disabled_text.find('non accetta') != -1
            
            job_posting.disabled = is_disabled

            # Check application type and external URL if not disabled
            if not is_disabled:
                job_external_button_selector = '.jobs-apply-button--top-card .jobs-apply-button'
                try:
                    page.wait_for_selector(job_external_button_selector, timeout=1000)
                    if page.query_selector(job_external_button_selector):
                        job_external_button_text = page.query_selector(job_external_button_selector).inner_text().strip()
                        # Check if it's a simple application (keyword "semplice")
                        job_posting.is_simple = job_external_button_text.find('semplice') != -1
                except Exception as e:
                    pass
            
                # Get external URL for non-simple applications
                if (not job_posting.is_simple):
                    page.click(job_external_button_selector)
                    page.wait_for_timeout(5000)

                    # Check if application opened in a new tab
                    if len(page.context.pages) > 1:
                        new_page = page.context.pages[-1]
                        external_url = new_page.url
                    else:
                        external_url = page.url
                    
                    job_posting.external_url = external_url

            browser.close()
            return job_posting

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

