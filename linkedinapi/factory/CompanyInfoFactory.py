from linkedinapi.model.Company import Company
from linkedinapi.model.CompanySinglePage import CompanySinglePage

class CompanyFactory:
    @staticmethod
    async def create_from_company_single_page(company_single_page: CompanySinglePage) -> Company:
        company_info = Company()
        company_info.name = await company_single_page.get_name()
        company_info.description = await company_single_page.get_description()
        company_info.website = await company_single_page.get_website()
        company_info.industry = await company_single_page.get_industry()
        company_info.company_size = await company_single_page.get_company_size()
        company_info.headquarters = await company_single_page.get_headquarters()
        return company_info
