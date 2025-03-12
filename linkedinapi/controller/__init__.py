from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials

from linkedinapi.api import default_container
from linkedinapi.container.DefaultContainer import DefaultContainer
from linkedinapi.helper.TokenHelper import TokenHelper
from linkedinapi.manager.SecretManager import SecretManager

security_scheme = HTTPBearer()

async def get_current_username(token_credentials: HTTPAuthorizationCredentials = Depends(security_scheme)):
    """Dependency to extract the user from the Bearer token"""
    default_container: DefaultContainer = DefaultContainer.getInstance()
    secret_manager: SecretManager = default_container.get(SecretManager)
    try:
        token_data = TokenHelper.decode_token(token_credentials.credentials, secret_manager.get_secret_key())
        return token_data['username']
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
