from fastapi import APIRouter
from pydantic import BaseModel
from injector import inject

from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.service.LoginService import LoginService

class LoginRequest(BaseModel):
    username: str
    password: str

login_controller = APIRouter()

@login_controller.post("/login")
async def login(login_request: LoginRequest):
    default_container: DefaultContainer = DefaultContainer.getInstance()
    login_service: LoginService = default_container.get(LoginService)
    
    return login_service.login(login_request.username, login_request.password)
