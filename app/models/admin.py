from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from .base import PyObjectId

class AdminBase(BaseModel):
    username: str
    email: EmailStr
    is_active: bool = True

class AdminCreate(AdminBase):
    password: str

class AdminInDB(AdminBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class AdminOut(AdminBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
