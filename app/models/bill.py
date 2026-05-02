from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from app.models.common import PyObjectId

class BillItem(BaseModel):
    description: str
    quantity: int
    price: float
    total: float

class Bill(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    patient_id: str = Field(..., description="Ref: Patients._id")
    total_amount: float
    items: List[BillItem]
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
