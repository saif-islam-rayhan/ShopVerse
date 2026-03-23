"""User database model."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom type for MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)
    
    def __repr__(self):
        return f"ObjectId('{self}')"


class User(BaseModel):
    """User model for database operations."""
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    email: EmailStr
    username: str
    password: str  # Hashed password
    auth_provider: str = "local"  # 'local', 'google'
    provider_id: Optional[str] = None  # Google ID if OAuth
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = True
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "_id": ObjectId(),
                "email": "user@example.com",
                "username": "john_doe",
                "password": "$2b$12$...",  # bcrypt hash
                "auth_provider": "local",
                "provider_id": None,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
                "is_active": True
            }
        }
