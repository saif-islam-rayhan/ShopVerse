"""Authentication routes (register, login, Google OAuth)."""

from fastapi import APIRouter, HTTPException, status, Depends
from bson import ObjectId
from datetime import datetime
import logging

from app.config import get_database
from app.schemas import (
    UserRegisterRequest,
    UserLoginRequest,
    GoogleLoginRequest,
    AuthResponse,
    UserResponse,
    UpdateProfileRequest,
    ProfileResponse,
)
from app.controllers import AuthController
from app.middleware import get_current_user_id

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
    return await AuthController.register_user(
        email=request.email,
        password=request.password,
        username=request.username,
    )


@router.post("/login", response_model=AuthResponse)
async def login(request: UserLoginRequest):
    """
    User login with email and password.
    
    - **email**: Registered email address
    - **password**: Account password
    """
    return await AuthController.login_user(
        email=request.email,
        password=request.password,
    )


@router.post("/google", response_model=AuthResponse)
async def google_login(request: GoogleLoginRequest):
    """
    Google OAuth login.
    
    - **token**: Google ID token from frontend
    """
    return await AuthController.google_login(google_token=request.token)


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
    
    user_data = dict(user)
    user_data['_id'] = str(user_data['_id'])
    return UserResponse(**user_data)


@router.get("/profile", response_model=ProfileResponse)
async def get_profile(user_id: str = Depends(get_current_user_id)):
    """
    Get user profile (protected route).
    
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
    
    user_data = dict(user)
    user_data['_id'] = str(user_data['_id'])
    return ProfileResponse(**user_data)


@router.put("/profile", response_model=ProfileResponse)
async def update_profile(
    request: UpdateProfileRequest,
    user_id: str = Depends(get_current_user_id)
):
    """
    Update user profile (protected route).
    
    Allows updating: full_name, address, profile_picture
    
    Requires valid JWT token in Authorization header.
    """
    db = get_database()
    users_collection = db["users"]
    
    try:
        user_oid = ObjectId(user_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID in token",
        )
    
    # Build update data with only provided fields
    update_data = {}
    if request.full_name is not None:
        update_data["full_name"] = request.full_name
    if request.address is not None:
        update_data["address"] = request.address
    if request.profile_picture is not None:
        update_data["profile_picture"] = request.profile_picture
    
    # Add updated_at timestamp
    update_data["updated_at"] = datetime.utcnow()
    
    # Update user document
    result = await users_collection.find_one_and_update(
        {"_id": user_oid},
        {"$set": update_data},
        return_document=True
    )
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    result_data = dict(result)
    result_data['_id'] = str(result_data['_id'])
    return ProfileResponse(**result_data)
