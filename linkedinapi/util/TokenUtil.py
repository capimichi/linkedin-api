import datetime

import jwt
from fastapi.security import HTTPAuthorizationCredentials

SECRET_KEY = "your_secret_key"  # Replace with a secure secret key

class TokenUtil:
    
    @staticmethod
    def generate_token(username: str) -> str:
        """
        Generate a JWT token for the given username.
        
        Args:
            username: The username to include in the token
            
        Returns:
            A JWT token as a string
        """
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expires in 1 hour
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    
    @staticmethod
    def decode_token(token: HTTPAuthorizationCredentials) -> str:
        """
        Decode a JWT token to extract the username.
        
        Args:
            token: The JWT token to decode
            
        Returns:
            The username extracted from the token
        """
        try:
            payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
            return payload["username"]
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
