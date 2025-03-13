from linkedinapi.model.JobPostingListingItem import JobPostingListingItem
from linkedinapi.model.JobPostingSearchCard import JobPostingSearchCard

class JobPostingListingItemFactory:
    @staticmethod
    async def create_from_job_posting_search_card(job_posting_search_card: JobPostingSearchCard) -> JobPostingListingItem:
        job_posting = JobPostingListingItem()
        job_posting.id = await job_posting_search_card.get_id()
        job_posting.title = await job_posting_search_card.get_title()
        job_posting.company_name = await job_posting_search_card.get_company_name()
        job_posting.metadata = await job_posting_search_card.get_metadata()
        job_posting.created_at = await job_posting_search_card.get_created_at()
        job_posting.is_simple = await job_posting_search_card.is_simple_application()
        return job_posting
