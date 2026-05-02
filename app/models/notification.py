from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.common import PyObjectId

class Notification(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    recipient_id: str = Field(..., description="User or Patient ID")
    type: str = Field(..., description="reminder | referral | admin_alert")
    message: str
    status: str = Field(default="pending", description="pending | sent | failed")
    sent_at: Optional[datetime] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
