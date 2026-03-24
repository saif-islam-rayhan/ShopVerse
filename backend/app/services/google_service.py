"""Google OAuth service for token verification and authentication."""

import requests
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)


class GoogleAuthService:
    """Service for Google OAuth token verification."""

    @staticmethod
    async def verify_google_token(access_token: str) -> dict:
        """
        Verify Google access token and extract user information.

        Args:
            access_token: Google access token from frontend (from useGoogleLogin)

        Returns:
            Dictionary with user information (email, name, picture, google_id)

        Raises:
            ValueError: If token is invalid
        """
        try:
            logger.info("Verifying Google access token...")
            
            # Verify token by calling Google tokeninfo endpoint
            tokeninfo_url = f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}"
            tokeninfo_response = requests.get(tokeninfo_url, timeout=10)
            
            if tokeninfo_response.status_code != 200:
                raise ValueError("Invalid or expired access token")
            
            token_info = tokeninfo_response.json()
            
            if token_info.get('error'):
                raise ValueError(f"Token error: {token_info.get('error_description', 'Unknown error')}")
            
            # Validate that the token was issued for our client
            # Access tokens usually use 'audience' or 'issued_to', while ID tokens use 'aud'
            token_audience = token_info.get('aud') or token_info.get('audience') or token_info.get('issued_to')
            
            if settings.google_client_id and token_audience and token_audience != settings.google_client_id:
                raise ValueError("Token audience mismatch: Invalid Google Client ID")

            # Get user info using the access token
            userinfo_url = f"https://www.googleapis.com/oauth2/v1/userinfo?access_token={access_token}"
            userinfo_response = requests.get(userinfo_url, timeout=10)
            
            if userinfo_response.status_code != 200:
                raise ValueError("Failed to retrieve user information")
            
            userinfo = userinfo_response.json()
            
            logger.info(f"Google token verified for: {userinfo.get('email')}")
            
            # Extract user information
            user_info = {
                "google_id": userinfo.get("id"),
                "email": userinfo.get("email"),
                "name": userinfo.get("name", ""),
                "picture": userinfo.get("picture", ""),
                "email_verified": userinfo.get("verified_email", False),
            }
            
            return user_info
            
        except ValueError as e:
            logger.error(f"Google token verification failed: {e}")
            raise ValueError(f"Invalid Google token: {str(e)}")
        except Exception as e:
            logger.error(f"Google token error: {e}")
            raise ValueError(f"Google authentication error: {str(e)}")
