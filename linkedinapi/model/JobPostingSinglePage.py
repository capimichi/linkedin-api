from playwright.async_api import Page

class JobPostingSinglePage:
    def __init__(self, page: Page):
        self.page = page

    async def get_title(self) -> str:
        job_title_selector = '.artdeco-card h1'
        await self.page.wait_for_selector(job_title_selector, timeout=1000)
        return (await self.page.query_selector(job_title_selector)).inner_text().strip()

    async def get_location(self) -> str:
        job_location_selector = '.job-details-jobs-unified-top-card__primary-description-container .tvm__text:first-child'
        await self.page.wait_for_selector(job_location_selector, timeout=1000)
        return (await self.page.query_selector(job_location_selector)).inner_text().strip()

    async def get_description(self) -> str:
        job_description_selector = '.jobs-box__html-content p'
        await self.page.wait_for_selector(job_description_selector, timeout=1000)
        return (await self.page.query_selector(job_description_selector)).inner_text().strip()

    async def get_skills(self) -> list:
        job_skills_selector = '.job-details-how-you-match__skills-item-subtitle'
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

    async def get_additional_skills(self) -> list:
        additional_skills_selector = '.job-details-how-you-match__skills-section-descriptive-skill'
        await self.page.wait_for_selector(additional_skills_selector, timeout=1000)
        additional_skills_object = await self.page.query_selector(additional_skills_selector)
        skills = []
        if additional_skills_object:
            additional_skills = (await additional_skills_object.inner_text()).strip()
            additional_skills = additional_skills.split('·')
            for additional_skill in additional_skills:
                skills.append(additional_skill.strip())
        return skills

    async def get_company_info(self) -> tuple:
        company_url_selector = '.job-details-jobs-unified-top-card__company-name a'
        await self.page.wait_for_selector(company_url_selector, timeout=1000)
        company_name = (await self.page.query_selector(company_url_selector)).inner_text().strip()
        company_url = (await self.page.query_selector(company_url_selector)).get_attribute('href')
        company_slug = company_url.split('company/')[1].split('/')[0]
        return company_name, company_slug

    async def is_disabled(self) -> bool:
        job_disabled_selector = '.artdeco-inline-feedback__message'
        if await self.page.query_selector(job_disabled_selector):
            job_disabled_text = (await self.page.query_selector(job_disabled_selector)).inner_text().strip().lower()
            return job_disabled_text.find('non accetta') != -1
        return False

    async def is_simple_application(self) -> bool:
        job_external_button_selector = '.jobs-apply-button--top-card .jobs-apply-button'
        await self.page.wait_for_selector(job_external_button_selector, timeout=1000)
        if await self.page.query_selector(job_external_button_selector):
            job_external_button_text = (await self.page.query_selector(job_external_button_selector)).inner_text().strip()
            return job_external_button_text.find('semplice') != -1
        return False

    async def get_external_url(self) -> str:
        job_external_button_selector = '.jobs-apply-button--top-card .jobs-apply-button'
        await self.page.click(job_external_button_selector)
        await self.page.wait_for_timeout(5000)
        if len(self.page.context.pages) > 1:
            new_page = self.page.context.pages[-1]
            return new_page.url
        return self.page.url
