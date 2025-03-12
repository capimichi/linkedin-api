from injector import inject
from linkedinapi.util.TokenUtil import TokenUtil
from linkedinapi.client.LinkedinClient import LinkedinClient

class LoginService:

    @inject
    def __init__(self, linkedin_client: LinkedinClient):
        self.linkedin_client = linkedin_client
        
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
            token = TokenUtil.generate_token(username)
            return {"status": "success", "token": token}
        except Exception as e:
            return {"status": "error", "message": str(e)}

