from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

# ==========================================
# Authentication & User Schemas
# ==========================================
class UserBase(BaseModel):
    """
    Base attributes for User entity validation.
    """
    email: EmailStr
    full_name: str = Field(..., min_length=2, max_length=100, description="Full name of the user")
    role: Optional[str] = Field(default="architect", description="User role in the system")

class UserCreate(UserBase):
    """
    Payload required for new user registration.
    """
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

class UserLogin(BaseModel):
    """
    Payload required for user authentication.
    """
    email: EmailStr
    password: str

class UserResponse(UserBase):
    """
    Safe User DTO returned by API endpoints.
    """
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    """
    Authentication token response DTO.
    """
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class TokenData(BaseModel):
    """
    Decoded JWT payload internal schema.
    """
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[str] = None
