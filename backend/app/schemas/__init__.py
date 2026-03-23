"""Schemas package."""

from .auth import (
    UserRegisterRequest,
    UserLoginRequest,
    GoogleLoginRequest,
    TokenResponse,
    UserResponse,
    AuthResponse,
    ErrorResponse,
)

__all__ = [
    "UserRegisterRequest",
    "UserLoginRequest",
    "GoogleLoginRequest",
    "TokenResponse",
    "UserResponse",
    "AuthResponse",
    "ErrorResponse",
]
