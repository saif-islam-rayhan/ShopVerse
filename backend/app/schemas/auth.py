"""Pydantic schemas for authentication."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserRegisterRequest(BaseModel):
    """User registration request schema."""
    email: EmailStr
    password: str
    username: str = Field(..., min_length=3, max_length=50)
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123",
                "username": "john_doe"
            }
        }


class UserLoginRequest(BaseModel):
    """User login request schema."""
    email: EmailStr
    password: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "SecurePass123"
            }
        }


class GoogleLoginRequest(BaseModel):
    """Google login request schema."""
    token: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "token": "google-oauth-token-here"
            }
        }


class TokenResponse(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800
            }
        }


class UserResponse(BaseModel):
    """User response schema (safe data)."""
    id: str = Field(..., alias="_id")
    email: str
    username: str
    full_name: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    auth_provider: str = "local"
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "address": "123 Main St",
                "profile_picture": "https://example.com/pic.jpg",
                "created_at": "2024-01-01T12:00:00",
                "auth_provider": "local"
            }
        }


class AuthResponse(BaseModel):
    """Complete authentication response."""
    user: UserResponse
    token: TokenResponse
    
    class Config:
        json_schema_extra = {
            "example": {
                "user": {
                    "_id": "507f1f77bcf86cd799439011",
                    "email": "user@example.com",
                    "username": "john_doe",
                    "created_at": "2024-01-01T12:00:00",
                    "auth_provider": "local"
                },
                "token": {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                    "token_type": "bearer",
                    "expires_in": 1800
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response schema."""
    detail: str
    status_code: int = 400
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Invalid credentials",
                "status_code": 401
            }
        }


class UpdateProfileRequest(BaseModel):
    """Update user profile request schema."""
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    address: Optional[str] = Field(None, max_length=500)
    profile_picture: Optional[str] = Field(None, max_length=1000)
    
    class Config:
        json_schema_extra = {
            "example": {
                "full_name": "John Doe",
                "address": "123 Main Street, New York, NY 10001",
                "profile_picture": "https://example.com/profile.jpg"
            }
        }


class ProfileResponse(BaseModel):
    """Profile response schema."""
    id: str = Field(..., alias="_id")
    email: str
    username: str
    full_name: Optional[str] = None
    address: Optional[str] = None
    profile_picture: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "username": "john_doe",
                "full_name": "John Doe",
                "address": "123 Main Street, New York, NY 10001",
                "profile_picture": "https://example.com/profile.jpg",
                "created_at": "2024-01-01T12:00:00",
                "updated_at": "2024-01-15T12:00:00"
            }
        }
