from injector import inject
from linkedinapi.client.LinkedinClient import LinkedinClient
from linkedinapi.helper.TokenHelper import TokenHelper
from linkedinapi.manager.SecretManager import SecretManager


class LoginService:

    @inject
    def __init__(self, linkedin_client: LinkedinClient, secret_manager: SecretManager):
        self.linkedin_client = linkedin_client
        self.secret_manager = secret_manager
        
    def login(self, username: str, password: str):
        """
        Login to LinkedIn using provided credentials and generate a token.
        
        Args:
            username: LinkedIn username/email
            password: LinkedIn password
            
        Returns:
            A dictionary containing the login status and token
        """
        try:
            self.linkedin_client.login(username, password)
            token = TokenHelper.generate_token(
                username,
                self.secret_manager.get_secret_key(),
                24
            )
            return {"status": "success", "token": token}
        except Exception as e:
            return {"status": "error", "message": str(e)}

