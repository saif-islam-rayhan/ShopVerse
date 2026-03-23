"""Authentication routes (register, login, Google OAuth)."""

from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime, timedelta
from bson import ObjectId
import logging

from app.config import get_database
from app.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    GoogleLoginRequest,
    AuthResponse,
    UserResponse,
    TokenResponse,
)
from app.models import User
from app.utils import (
    hash_password,
    verify_password,
    validate_email,
    validate_password,
    create_access_token,
)
from app.middleware import get_current_user_id
from app.config.settings import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(request: UserRegisterRequest):
    """
    Register a new user.
    
    - **email**: User email address (must be unique)
    - **password**: User password (min 8 chars, 1 uppercase, 1 lowercase, 1 digit)
    - **username**: User username (3-50 chars)
    """
    db = get_database()
    
    # Validate email format
    is_valid_email, email_msg = validate_email(request.email)
    if not is_valid_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_msg,
        )
    
    # Validate password strength
    is_valid_password, password_msg = validate_password(request.password)
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_msg,
        )
    
    # Check if user already exists
    users_collection = db["users"]
    existing_user = await users_collection.find_one({"email": request.email.lower()})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    
    # Create user
    hashed_password = hash_password(request.password)
    user_dict = {
        "email": request.email.lower(),
        "username": request.username,
        "password": hashed_password,
        "auth_provider": "local",
        "provider_id": None,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "is_active": True,
    }
    
    result = await users_collection.insert_one(user_dict)
    user_id = str(result.inserted_id)
    
    # Create token
    access_token = create_access_token(data={"sub": user_id})
    
    user_dict["_id"] = result.inserted_id
    user_response = UserResponse(**user_dict)
    token_response = TokenResponse(
        access_token=access_token,
        expires_in=settings.access_token_expire_minutes * 60,
    )
    
    logger.info(f"User registered: {request.email}")
    
    return AuthResponse(user=user_response, token=token_response)


@router.post("/login", response_model=AuthResponse)
async def login(request: UserLoginRequest):
    """
    User login with email and password.
    
    - **email**: Registered email address
    - **password**: Account password
    """
    db = get_database()
    users_collection = db["users"]
    
    # Find user by email
    user = await users_collection.find_one({"email": request.email.lower()})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Verify password
    if not verify_password(request.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    
    # Check if user is active
    if not user.get("is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )
    
    # Create token
    user_id = str(user["_id"])
    access_token = create_access_token(data={"sub": user_id})
    
    user_response = UserResponse(**user)
    token_response = TokenResponse(
        access_token=access_token,
        expires_in=settings.access_token_expire_minutes * 60,
    )
    
    logger.info(f"User logged in: {request.email}")
    
    return AuthResponse(user=user_response, token=token_response)


@router.post("/google", response_model=AuthResponse)
async def google_login(request: GoogleLoginRequest):
    """
    Google OAuth login.
    
    - **token**: Google ID token from frontend
    """
    db = get_database()
    
    try:
        # Import google auth utilities
        from google.auth.transport import requests
        from google.oauth2 import id_token
        
        # Verify Google token
        idinfo = id_token.verify_oauth2_token(
            request.token, 
            requests.Request(), 
            settings.google_client_id
        )
        
        # Extract user info from token
        google_id = idinfo["sub"]
        email = idinfo.get("email", "").lower()
        username = idinfo.get("name", email.split("@")[0])
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Google token does not contain email",
            )
        
        users_collection = db["users"]
        
        # Find or create user
        user = await users_collection.find_one({"provider_id": google_id})
        
        if not user:
            # Check if email already exists with different provider
            user = await users_collection.find_one({"email": email})
            
            if user:
                # Link Google account to existing user
                await users_collection.update_one(
                    {"_id": user["_id"]},
                    {
                        "$set": {
                            "provider_id": google_id,
                            "auth_provider": "google",
                            "updated_at": datetime.utcnow(),
                        }
                    },
                )
            else:
                # Create new user
                user_dict = {
                    "email": email,
                    "username": username,
                    "password": "",  # No password for OAuth users
                    "auth_provider": "google",
                    "provider_id": google_id,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                    "is_active": True,
                }
                result = await users_collection.insert_one(user_dict)
                user = {**user_dict, "_id": result.inserted_id}
        
        # Create token
        user_id = str(user["_id"])
        access_token = create_access_token(data={"sub": user_id})
        
        user_response = UserResponse(**user)
        token_response = TokenResponse(
            access_token=access_token,
            expires_in=settings.access_token_expire_minutes * 60,
        )
        
        logger.info(f"User logged in via Google: {email}")
        
        return AuthResponse(user=user_response, token=token_response)
        
    except ValueError as e:
        logger.error(f"Invalid Google token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token",
        )
    except Exception as e:
        logger.error(f"Google authentication error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google authentication failed",
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user(user_id: str = Depends(get_current_user_id)):
    """
    Get current user information (protected route).
    
    Requires valid JWT token in Authorization header.
    """
    db = get_database()
    users_collection = db["users"]
    
    try:
        user = await users_collection.find_one({"_id": ObjectId(user_id)})
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    return UserResponse(**user)
