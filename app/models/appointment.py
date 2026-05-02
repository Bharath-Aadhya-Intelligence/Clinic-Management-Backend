from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.common import PyObjectId

class Appointment(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    patient_id: str = Field(..., description="Ref: Patients._id")
    date: datetime
    reminder_sent_patient: bool = False
    reminder_sent_admin: bool = False
    status: str = Field(default="scheduled", description="scheduled | completed | cancelled")

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
