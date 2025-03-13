from typing import Optional

from fastapi import APIRouter, HTTPException, Depends

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.controller import get_current_username
from linkedinapi.model.Company import Company
from linkedinapi.service.CompanyService import CompanyService

company_controller = APIRouter(
    prefix="/companies",
    tags=["Companies"],
)

@company_controller.get("/{company_slug}")
async def get_company(company_slug: str, username: str = Depends(get_current_username)) -> Company:
    """
    Get detailed information about a specific company.
    
    Args:
        company_slug: LinkedIn company slug
        username: LinkedIn username to load browser session
        
    Returns:
        CompanyInfo object containing detailed company information
    """
    default_container: DefaultContainer = DefaultContainer.getInstance()
    company_service: CompanyService = default_container.get(CompanyService)

    try:
        company_details = await company_service.get_company(username, company_slug)
        return company_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving company details: {str(e)}")
