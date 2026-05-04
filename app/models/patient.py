from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List
from enum import Enum
from .base import PyObjectId

class ReferralSource(str, Enum):
    GOOGLE = "Google"
    INSTAGRAM = "Instagram"
    YOUTUBE = "YouTube"
    OLD_PATIENT = "Old Patient"
    OTHER = "Other"

class AppointmentStatus(str, Enum):
    SCHEDULED = "Scheduled"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"

class Appointment(BaseModel):
    appointment_number: int  # 1, 2, or 3
    date: Optional[datetime] = None
    time: Optional[str] = None
    status: AppointmentStatus = AppointmentStatus.SCHEDULED

class PatientBase(BaseModel):
    name: str
    age: int
    phone_number: str
    address: str
    visit_date: date = Field(default_factory=date.today)
    referral_source: ReferralSource = ReferralSource.OTHER

class PatientCreate(PatientBase):
    second_treatment_date: Optional[date] = None
    third_treatment_date: Optional[date] = None

class PatientUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    visit_date: Optional[date] = None
    referral_source: Optional[ReferralSource] = None
    appointments: Optional[List[Appointment]] = None

class PatientInDB(PatientBase):
    id: Optional[PyObjectId] = Field(alias="_id", serialization_alias="id", default=None)
    appointments: List[Appointment] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PatientOut(PatientInDB):
    pass
