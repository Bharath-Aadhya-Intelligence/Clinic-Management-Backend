from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.common import PyObjectId

class Referral(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    referrer_id: str = Field(..., description="Ref: Patients._id")
    referred_patient_id: str = Field(..., description="Ref: Patients._id")
    thankyou_sent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
