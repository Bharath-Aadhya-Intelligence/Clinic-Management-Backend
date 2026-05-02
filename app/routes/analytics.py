from fastapi import APIRouter, Depends
from app.utils.db import get_database
from app.utils.deps import get_current_user
from typing import Any

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/overview", response_model=Any)
async def get_overview(db = Depends(get_database), current_user = Depends(get_current_user)):
    patients_count = await db.patients.count_documents({})
    appointments_count = await db.appointments.count_documents({})
    pipeline = [{"$group": {"_id": None, "total_revenue": {"$sum": "$total_amount"}}}]
    revenue_result = await db.bills.aggregate(pipeline).to_list(1)
    total_revenue = revenue_result[0]["total_revenue"] if revenue_result else 0
    
    return {
        "total_patients": patients_count,
        "total_appointments": appointments_count,
        "total_revenue": total_revenue
    }

@router.get("/lead-sources", response_model=Any)
async def get_lead_sources(db = Depends(get_database), current_user = Depends(get_current_user)):
    pipeline = [
        {"$group": {"_id": "$lead_source", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    stats = await db.patients.aggregate(pipeline).to_list(None)
    return stats

@router.get("/growth", response_model=Any)
async def get_growth(db = Depends(get_database), current_user = Depends(get_current_user)):
    # Basic stub for growth analytics - count by month or similar.
    # We will just return the total count as a placeholder.
    return {"status": "Not completely implemented, stub for growth data"}

@router.get("/revenue", response_model=Any)
async def get_revenue_trends(db = Depends(get_database), current_user = Depends(get_current_user)):
    # Basic stub for revenue trends
    return {"status": "Not completely implemented, stub for revenue trends"}
