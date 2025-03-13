from fastapi import APIRouter, HTTPException, Depends

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.controller import get_current_username
from linkedinapi.model.Hirer import Hirer
from linkedinapi.service.HirerService import HirerService

hirer_controller = APIRouter(
    prefix="/hirers",
    tags=["Hirers"],
)

@hirer_controller.get("/{hirer_slug}")
async def get_hirer(hirer_slug: str, username: str = Depends(get_current_username)) -> Hirer:
    """
    Get detailed information about a specific hirer.
    
    Args:
        hirer_slug: LinkedIn hirer slug
        username: LinkedIn username to load browser session
        
    Returns:
        Hirer object containing detailed hirer information
    """
    default_container: DefaultContainer = DefaultContainer.getInstance()
    hirer_service: HirerService = default_container.get(HirerService)

    try:
        hirer_details = await hirer_service.get_hirer(username, hirer_slug)
        return hirer_details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving hirer details: {str(e)}")
