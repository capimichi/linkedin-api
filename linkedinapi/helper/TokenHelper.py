import datetime

import jwt


class TokenHelper:
    
    @staticmethod
    def generate_token(username: str, secret_key: str, duration_hours: int = 1) -> str:
        """
        Generate a JWT token for the given username.
        
        Args:
            username: The username to include in the token
            secret_key: The secret key to use for encoding the token
            duration_hours: The duration in hours for which the token is valid
            
        Returns:
            A JWT token as a string
        """
        payload = {
            "username": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=duration_hours)  # Token expires in 1 hour
        }
        return jwt.encode(payload, secret_key, algorithm="HS256")
    
    @staticmethod
    def decode_token(token: str, secret_key: str) -> dict:
        """
        Decode a JWT token to extract the username.
        
        Args:
            token: The JWT token to decode
            secret_key: The secret key to use for decoding the token
            
        Returns:
            A dictionary containing the decoded token payload
        """
        try:
            payload = jwt.decode(token, secret_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")
