"""JWT verification middleware."""

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import logging
from app.utils import verify_token, extract_token_from_header
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)
security = HTTPBearer()


async def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """
    Verify JWT token from Authorization header.
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        Decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return payload


async def get_current_user_id(token_payload: Dict[str, Any] = Depends(verify_jwt_token)) -> str:
    """
    Get current user ID from token payload.
    
    Args:
        token_payload: Decoded JWT payload
        
    Returns:
        User ID
        
    Raises:
        HTTPException: If user ID not in token
    """
    user_id = token_payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token: user ID not found",
        )
    return user_id
