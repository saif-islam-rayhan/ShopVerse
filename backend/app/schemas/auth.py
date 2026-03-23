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
    created_at: datetime
    auth_provider: str = "local"
    
    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "_id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "username": "john_doe",
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
