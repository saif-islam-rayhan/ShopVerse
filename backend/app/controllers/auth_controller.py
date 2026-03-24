"""Authentication controller handling all auth business logic."""

from fastapi import HTTPException, status
from datetime import datetime
from app.utils import create_access_token, verify_password, hash_password
from app.utils import validate_email, validate_password
from app.services import GoogleAuthService, UserService
from app.schemas import UserResponse, TokenResponse, AuthResponse
from app.config import get_database
import logging

logger = logging.getLogger(__name__)


class AuthController:
    """Controller for authentication operations."""

    @staticmethod
    async def google_login(google_token: str) -> AuthResponse:
        """
        Authenticate user with Google token.

        Process:
        1. Verify Google token with Google API
        2. Extract user info (email, name, picture)
        3. Find or create user in database
        4. Generate JWT token
        5. Return user and token

        Args:
            google_token: Google ID token from frontend

        Returns:
            AuthResponse with user data and JWT token

        Raises:
            HTTPException: If token is invalid or verification fails
        """
        try:
            # Step 1: Verify Google token
            logger.info("Verifying Google token...")
            user_info = await GoogleAuthService.verify_google_token(google_token)

            # Step 2: Get or create user in database
            logger.info(f"Getting or creating user: {user_info['email']}")
            user = await UserService.get_or_create_user(
                email=user_info["email"],
                name=user_info["name"],
                picture=user_info.get("picture"),
                google_id=user_info["google_id"],
                auth_provider="google"
            )

            # Step 3: Generate JWT token
            user_id = str(user["_id"])
            access_token = create_access_token(data={"sub": user_id})

            logger.info(f"User authenticated successfully: {user['email']}")

            # Step 4: Prepare response
            user_data = dict(user)
            user_data['_id'] = str(user['_id'])
            user_response = UserResponse(**user_data)
            token_response = TokenResponse(
                access_token=access_token,
                expires_in=30 * 60,  # 30 minutes
            )

            return AuthResponse(user=user_response, token=token_response)

        except ValueError as e:
            logger.error(f"Google token validation error: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=str(e),
            )
        except Exception as e:
            logger.error(f"Google authentication error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Authentication failed",
            )

    @staticmethod
    async def register_user(email: str, password: str, username: str) -> AuthResponse:
        """
        Register new user with email and password.

        Process:
        1. Validate email format
        2. Validate password strength
        3. Check if email already exists
        4. Hash password
        5. Create user in database
        6. Generate JWT token
        7. Return user and token

        Args:
            email: User email
            password: User password (plain text)
            username: User username

        Returns:
            AuthResponse with user data and JWT token

        Raises:
            HTTPException: If validation fails or email already exists
        """
        try:
            # Step 1: Validate email
            is_valid_email, email_msg = validate_email(email)
            if not is_valid_email:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=email_msg,
                )

            # Step 2: Validate password
            is_valid_password, password_msg = validate_password(password)
            if not is_valid_password:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=password_msg,
                )

            # Step 3: Check if email exists
            db = get_database()
            users_collection = db["users"]
            existing_user = await users_collection.find_one(
                {"email": email.lower()}
            )
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email already registered",
                )

            # Step 4: Hash password
            hashed_password = hash_password(password)

            # Step 5: Create user
            user_dict = {
                "email": email.lower(),
                "username": username,
                "password": hashed_password,
                "auth_provider": "local",
                "google_id": None,
                "picture": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "last_login": datetime.utcnow(),
                "is_active": True,
                "is_email_verified": False,  # Should verify email in production
            }

            result = await users_collection.insert_one(user_dict)
            user_dict["_id"] = result.inserted_id

            logger.info(f"User registered: {email}")

            # Step 6: Generate JWT token
            user_id = str(result.inserted_id)
            access_token = create_access_token(data={"sub": user_id})

            # Step 7: Prepare response
            user_data = dict(user_dict)
            user_data['_id'] = str(user_data['_id'])
            user_response = UserResponse(**user_data)
            token_response = TokenResponse(
                access_token=access_token,
                expires_in=30 * 60,
            )

            return AuthResponse(user=user_response, token=token_response)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Registration error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Registration failed",
            )

    @staticmethod
    async def login_user(email: str, password: str) -> AuthResponse:
        """
        Login user with email and password.

        Process:
        1. Find user by email
        2. Verify password
        3. Check if user is active
        4. Generate JWT token
        5. Update last login
        6. Return user and token

        Args:
            email: User email
            password: User password (plain text)

        Returns:
            AuthResponse with user data and JWT token

        Raises:
            HTTPException: If credentials are invalid
        """
        try:
            # Step 1: Find user
            db = get_database()
            users_collection = db["users"]
            user = await users_collection.find_one(
                {"email": email.lower()}
            )

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            # Step 2: Verify password
            if not verify_password(password, user["password"]):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )

            # Step 3: Check if user is active
            if not user.get("is_active", True):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="User account is inactive",
                )

            # Step 4: Update last login
            await users_collection.update_one(
                {"_id": user["_id"]},
                {"$set": {"last_login": datetime.utcnow()}}
            )

            # Step 5: Generate JWT token
            user_id = str(user["_id"])
            access_token = create_access_token(data={"sub": user_id})

            logger.info(f"User logged in: {email}")

            # Step 6: Prepare response
            user_data = dict(user)
            user_data['_id'] = str(user_data['_id'])
            user_response = UserResponse(**user_data)
            token_response = TokenResponse(
                access_token=access_token,
                expires_in=30 * 60,
            )

            return AuthResponse(user=user_response, token=token_response)

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Login error: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Login failed",
            )
