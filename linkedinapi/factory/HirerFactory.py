from linkedinapi.model.Hirer import Hirer
from linkedinapi.model.HirerSinglePage import HirerSinglePage

class HirerFactory:
    @staticmethod
    async def create_from_hirer_single_page(hirer_single_page: HirerSinglePage) -> Hirer:
        hirer_info = Hirer()
        hirer_info.name = await hirer_single_page.get_name()
        hirer_info.slug = await hirer_single_page.get_slug()
        hirer_info.location = await hirer_single_page.get_location()
        hirer_info.role = await hirer_single_page.get_role()
        return hirer_info
