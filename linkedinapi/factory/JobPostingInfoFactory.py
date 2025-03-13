from linkedinapi.model.JobPostingInfo import JobPostingInfo
from linkedinapi.model.JobPostingSinglePage import JobPostingSinglePage

class JobPostingInfoFactory:
    @staticmethod
    async def create_from_job_posting_single_page(job_posting_single_page: JobPostingSinglePage) -> JobPostingInfo:
        job_posting_info = JobPostingInfo()
        job_posting_info.id = await job_posting_single_page.get_id()
        job_posting_info.title = await job_posting_single_page.get_title()
        job_posting_info.location = await job_posting_single_page.get_location()
        job_posting_info.description = await job_posting_single_page.get_description()
        job_posting_info.skills = await job_posting_single_page.get_skills() + await job_posting_single_page.get_additional_skills()
        job_posting_info.company_name, job_posting_info.company_slug = await job_posting_single_page.get_company_info()
        job_posting_info.disabled = await job_posting_single_page.is_disabled()
        job_posting_info.is_simple = await job_posting_single_page.is_simple_application()
        if not job_posting_info.is_simple:
            job_posting_info.external_url = await job_posting_single_page.get_external_url()

        job_posting_info.hirers = await job_posting_single_page.get_hirers()
        return job_posting_info
