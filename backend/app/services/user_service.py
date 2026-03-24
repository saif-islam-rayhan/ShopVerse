"""User management service."""

from datetime import datetime
from bson import ObjectId
from app.config import get_database
from app.models import User
from app.utils import hash_password
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service for user management operations."""

    @staticmethod
    async def get_or_create_user(
        email: str,
        name: str,
        picture: str = None,
        google_id: str = None,
        auth_provider: str = "google"
    ) -> dict:
        """
        Get existing user by email or create new user.

        Args:
            email: User email (unique identifier)
            name: User full name
            picture: User profile picture URL
            google_id: Google account ID
            auth_provider: Authentication provider (google, local, etc.)

        Returns:
            User document from database
        """
        db = get_database()
        users_collection = db["users"]

        try:
            # Check if user already exists
            existing_user = await users_collection.find_one(
                {"email": email.lower()}
            )

            if existing_user:
                logger.info(f"User found: {email}")
                # Update last login and picture if available
                await users_collection.update_one(
                    {"_id": existing_user["_id"]},
                    {
                        "$set": {
                            "last_login": datetime.utcnow(),
                            "picture": picture or existing_user.get("picture"),
                        }
                    }
                )
                existing_user["picture"] = picture or existing_user.get("picture")
                existing_user["last_login"] = datetime.utcnow()
                return existing_user

            # Create new user
            new_user = {
                "email": email.lower(),
                "name": name,
                "picture": picture,
                "auth_provider": auth_provider,
                "google_id": google_id,
                "password": "",  # No password for OAuth users
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": datetime.utcnow(),
                "is_active": True,
                "is_email_verified": True,  # Google accounts are pre-verified
            }

            result = await users_collection.insert_one(new_user)
            new_user["_id"] = result.inserted_id

            logger.info(f"New user created: {email}")
            return new_user

        except Exception as e:
            logger.error(f"Error in get_or_create_user: {e}")
            raise

    @staticmethod
    async def get_user_by_id(user_id: str) -> dict:
        """
        Get user by ID.

        Args:
            user_id: User ID (MongoDB ObjectId)

        Returns:
            User document or None
        """
        db = get_database()
        users_collection = db["users"]

        try:
            user = await users_collection.find_one(
                {"_id": ObjectId(user_id)}
            )
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None

    @staticmethod
    async def get_user_by_email(email: str) -> dict:
        """
        Get user by email.

        Args:
            email: User email

        Returns:
            User document or None
        """
        db = get_database()
        users_collection = db["users"]

        try:
            user = await users_collection.find_one(
                {"email": email.lower()}
            )
            return user
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None

    @staticmethod
    async def update_profile(
        user_id: str,
        full_name: str = None,
        address: str = None,
        profile_picture: str = None
    ) -> dict:
        """
        Update user profile.

        Args:
            user_id: User ID (MongoDB ObjectId string)
            full_name: User full name
            address: User address
            profile_picture: User profile picture URL

        Returns:
            Updated user document or None
        """
        db = get_database()
        users_collection = db["users"]

        try:
            # Build update data with only provided fields
            update_data = {}
            if full_name is not None:
                update_data["full_name"] = full_name
            if address is not None:
                update_data["address"] = address
            if profile_picture is not None:
                update_data["profile_picture"] = profile_picture
            
            # Add updated_at timestamp
            update_data["updated_at"] = datetime.utcnow()

            # Update user document
            user = await users_collection.find_one_and_update(
                {"_id": ObjectId(user_id)},
                {"$set": update_data},
                return_document=True
            )
            
            logger.info(f"User profile updated: {user_id}")
            return user
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            raise
