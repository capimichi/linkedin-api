from typing import List, Optional, Tuple
from playwright.async_api import Page

from linkedinapi.model.Hirer import Hirer


class JobPostingSinglePage:
    """
    A class to represent a single job posting page on LinkedIn.
    """

    def __init__(self, page: Page):
        """
        Initialize the JobPostingSinglePage with a Playwright Page object.

        :param page: Playwright Page object
        """
        self.page = page

    async def get_id(self) -> Optional[int]:
        """
        Get the job ID from the job posting page.

        :return: Job ID as an integer, or None if not found
        """
        try:
            return int(self.page.url.split('jobs/view/')[1].split('/')[0])
        except Exception:
            return None

    async def get_title(self) -> Optional[str]:
        """
        Get the job title from the job posting page.

        :return: Job title as a string, or None if not found
        """
        job_title_selector = '.artdeco-card h1'
        try:
            await self.page.wait_for_selector(job_title_selector, timeout=1000)
            job_title_element = await self.page.query_selector(job_title_selector)
            return (await job_title_element.inner_text()).strip()
        except Exception:
            return None

    async def get_location(self) -> Optional[str]:
        """
        Get the job location from the job posting page.

        :return: Job location as a string, or None if not found
        """
        job_location_selector = '.job-details-jobs-unified-top-card__primary-description-container .tvm__text:first-child'
        try:
            await self.page.wait_for_selector(job_location_selector, timeout=1000)
            job_location_element = await self.page.query_selector(job_location_selector)
            return (await job_location_element.inner_text()).strip()
        except Exception:
            return None

    async def get_description(self) -> Optional[str]:
        """
        Get the job description from the job posting page.

        :return: Job description as a string, or None if not found
        """
        job_description_selector = '.jobs-box__html-content p'
        try:
            await self.page.wait_for_selector(job_description_selector, timeout=1000)
            job_description_element = await self.page.query_selector(job_description_selector)
            return (await job_description_element.inner_text()).strip()
        except Exception:
            return None

    async def get_skills(self) -> List[str]:
        """
        Get the required skills from the job posting page.

        :return: List of required skills, or an empty list if not found
        """
        job_skills_selector = '.job-details-how-you-match__skills-item-subtitle'
        try:
            await self.page.wait_for_selector(job_skills_selector, timeout=1000)
            job_skills_objects = await self.page.query_selector_all(job_skills_selector)
            skills = []
            for job_skills_object in job_skills_objects:
                job_skills = (await job_skills_object.inner_text()).strip()
                job_skills = job_skills.split(',')
                for job_skill in job_skills:
                    is_last_skill = job_skill == job_skills[-1]
                    if not is_last_skill:
                        skills.append(job_skill.strip())
                    else:
                        split_skill = job_skill.split(' e ')
                        for s in split_skill:
                            skills.append(s.strip())
            return skills
        except Exception:
            return []

    async def get_additional_skills(self) -> List[str]:
        """
        Get the additional skills from the job posting page.

        :return: List of additional skills, or an empty list if not found
        """
        additional_skills_selector = '.job-details-how-you-match__skills-section-descriptive-skill'
        try:
            await self.page.wait_for_selector(additional_skills_selector, timeout=1000)
            additional_skills_object = await self.page.query_selector(additional_skills_selector)
            skills = []
            if additional_skills_object:
                additional_skills = (await additional_skills_object.inner_text()).strip()
                additional_skills = additional_skills.split('·')
                for additional_skill in additional_skills:
                    skills.append(additional_skill.strip())
            return skills
        except Exception:
            return []

    async def get_company_info(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Get the company name and slug from the job posting page.

        :return: Tuple containing company name and slug, or (None, None) if not found
        """
        company_url_selector = '.job-details-jobs-unified-top-card__company-name a'
        try:
            await self.page.wait_for_selector(company_url_selector, timeout=1000)
            company_name_element = await self.page.query_selector(company_url_selector)
            company_name = (await company_name_element.inner_text()).strip()
            company_url = (await company_name_element.get_attribute('href'))
            company_slug = company_url.split('company/')[1].split('/')[0]
            return company_name, company_slug
        except Exception:
            return None, None

    async def is_disabled(self) -> bool:
        """
        Check if the job posting is disabled.

        :return: True if the job posting is disabled, False otherwise
        """
        job_disabled_selector = '.artdeco-inline-feedback__message'
        try:
            if await self.page.query_selector(job_disabled_selector):
                job_disabled_element = await self.page.query_selector(job_disabled_selector)
                job_disabled_text = (await job_disabled_element.inner_text()).strip().lower()
                return job_disabled_text.find('non accetta') != -1
            return False
        except Exception:
            return False

    async def is_simple_application(self) -> bool:
        """
        Check if the job posting is a simple application.

        :return: True if the job posting is a simple application, False otherwise
        """
        job_external_button_selector = '.jobs-apply-button--top-card .jobs-apply-button'
        try:
            await self.page.wait_for_selector(job_external_button_selector, timeout=1000)
            if await self.page.query_selector(job_external_button_selector):
                job_external_button_element = await self.page.query_selector(job_external_button_selector)
                job_external_button_text = (await job_external_button_element.inner_text()).strip()
                return job_external_button_text.find('semplice') != -1
            return False
        except Exception:
            return False

    async def get_external_url(self) -> Optional[str]:
        """
        Get the external URL for the job application.

        :return: External URL as a string, or None if not found
        """
        job_external_button_selector = '.jobs-apply-button--top-card .jobs-apply-button'
        try:
            await self.page.click(job_external_button_selector)
            await self.page.wait_for_timeout(5000)
            if len(self.page.context.pages) > 1:
                new_page = self.page.context.pages[-1]
                return new_page.url
            return self.page.url
        except Exception:
            return None

    async def get_hirers(self) -> List[Hirer]:
        """
        Get the hirer information (name, link, role) from the job posting page.

        :return: List of tuples containing hirer name, link, and role, or an empty list if not found
        """
        hirer_info_selector = '.hirer-card__hirer-information'
        try:
            await self.page.wait_for_selector(hirer_info_selector, timeout=1000)
            hirer_elements = await self.page.query_selector_all(hirer_info_selector)
            hirers: List[Hirer] = []
            for hirer_element in hirer_elements:
                name_element = await hirer_element.query_selector('.jobs-poster__name strong')
                link_element = await hirer_element.query_selector('a')
                role_element = await hirer_element.query_selector('.linked-area .text-body-small')
                
                name = (await name_element.inner_text()).strip() if name_element else None
                link = (await link_element.get_attribute('href')) if link_element else None
                role = (await role_element.inner_text()).strip() if role_element else None

                hirer = Hirer()
                hirer.set_name(name)
                hirer.set_url(link)
                hirer.set_role(role)

                hirers.append(hirer)
            return hirers
        except Exception:
            return []
