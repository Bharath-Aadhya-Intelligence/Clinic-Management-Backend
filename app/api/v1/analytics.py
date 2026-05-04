from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from ...services.patient import patient_service
from ...api.deps import get_current_admin
from ...models.patient import PatientOut

router = APIRouter()

@router.get("/today")
async def get_today_stats(current_admin: dict = Depends(get_current_admin)):
    count = await patient_service.get_today_visit_count()
    return {
        "patient_count": count,
        "order_count": 0, # Placeholder or fetch from order service
        "reminder_count": 0 # Placeholder
    }

@router.get("/monthly")
async def get_monthly_stats(current_admin: dict = Depends(get_current_admin)):
    total = await patient_service.get_monthly_visit_count()
    breakdown = await patient_service.get_monthly_visit_breakdown()
    return {
        "monthly_visit_count": total,
        "daily_breakdown": breakdown
    }

@router.get("/reminders", response_model=Dict[str, Any])
async def get_appointment_reminders(current_admin: dict = Depends(get_current_admin)):
    reminders = await patient_service.get_reminders_for_tomorrow()
    return {"reminders": reminders}
