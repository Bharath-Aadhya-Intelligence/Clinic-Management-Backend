from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from ...services.patient import patient_service
from ...services.medicine import medicine_service
from ...services.order import order_service
from ...api.deps import get_current_admin

router = APIRouter()

@router.get("/today")
async def get_today_stats(current_admin: dict = Depends(get_current_admin)):
    visit_count = await patient_service.get_today_visit_count()
    med_count = await medicine_service.get_count()
    order_count = await order_service.get_count({"status": "Pending"})
    return {
        "today_visit_count": visit_count,
        "total_medicines": med_count,
        "pending_orders": order_count
    }

@router.get("/monthly")
async def get_monthly_stats(current_admin: dict = Depends(get_current_admin)):
    total = await patient_service.get_monthly_visit_count()
    breakdown = await patient_service.get_monthly_visit_breakdown()
    return {
        "monthly_visit_count": total,
        "daily_breakdown": breakdown
    }

@router.get("/reminders")
async def get_appointment_reminders(current_admin: dict = Depends(get_current_admin)):
    reminders = await patient_service.get_reminders_for_tomorrow()
    return reminders
