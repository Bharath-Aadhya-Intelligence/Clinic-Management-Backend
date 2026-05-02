from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, ConfigDict, GetJsonSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import core_schema
from bson import ObjectId
from app.models.common import PyObjectId

class Patient(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    phone: str
    age: Optional[int] = None
    address: Optional[str] = None
    notes: Optional[str] = None
    email: Optional[str] = None
    password_hash: Optional[str] = None
    lead_source: Optional[str] = Field(None, description="instagram | facebook | google | old_patient")
    referred_by: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
