from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .base import PyObjectId

class MedicineBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None
    is_active: bool = True

class MedicineCreate(MedicineBase):
    pass

class MedicineUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class MedicineInDB(MedicineBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    image_path: Optional[str] = None
    image_filename: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class MedicineOut(MedicineBase):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
