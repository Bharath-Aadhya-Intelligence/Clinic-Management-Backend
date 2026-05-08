from fastapi import APIRouter, Depends, Response, Request
from typing import List, Dict, Any
from datetime import datetime
from ...services.patient import patient_service
from ...services.medicine import medicine_service
from ...services.order import order_service
from ...services.report import report_service
from ...api.deps import get_current_admin
from ...core.rate_limit import limiter
from ...models.patient import PatientOut

router = APIRouter()

@router.get("/today")
@limiter.limit("30/minute")
async def get_today_stats(request: Request, current_admin: dict = Depends(get_current_admin)):
    visit_count = await patient_service.get_today_visit_count()
    med_count = await medicine_service.get_count()
    order_count = await order_service.get_count({"status": "Pending"})
    reminders = await patient_service.get_reminders_for_tomorrow()
    return {
        "today_visit_count": visit_count,
        "total_medicines": med_count,
        "pending_orders": order_count,
        "reminder_count": len(reminders)
    }

@router.get("/monthly")
@limiter.limit("30/minute")
async def get_monthly_stats(request: Request, current_admin: dict = Depends(get_current_admin)):
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

@router.get("/reports/orders")
async def get_order_report(current_admin: dict = Depends(get_current_admin)):
    csv_data = await report_service.generate_orders_csv()
    return Response(
        content=csv_data,
        media_type="text/csv",
        headers={
            "Content-Disposition": f"attachment; filename=order_report_{datetime.now().strftime('%Y%m%d')}.csv"
        }
    )
