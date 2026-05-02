from pydantic import BaseModel, EmailStr
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str
    role: str = "staff"

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PatientLogin(BaseModel):
    phone: str
    password: str

class PatientCreate(BaseModel):
    name: str
    phone: str
    password: str
