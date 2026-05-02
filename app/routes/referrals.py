from fastapi import APIRouter, HTTPException, Depends, status
from app.models.referral import Referral
from app.utils.db import get_database
from app.utils.deps import get_current_user
from typing import List, Any
from bson import ObjectId

router = APIRouter(prefix="/referrals", tags=["Referrals"])

@router.post("/", response_model=Referral, status_code=status.HTTP_201_CREATED)
async def create_referral(referral: Referral, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(referral.referrer_id) or not ObjectId.is_valid(referral.referred_patient_id):
        raise HTTPException(status_code=400, detail="Invalid referrer_id or referred_patient_id")
    
    ref_dict = {k: v for k, v in referral.model_dump(by_alias=True).items() if v is not None}
    new_ref = await db.referrals.insert_one(ref_dict)
    created_ref = await db.referrals.find_one({"_id": new_ref.inserted_id})
    return created_ref

@router.get("/", response_model=List[Referral])
async def list_referrals(db = Depends(get_database), current_user = Depends(get_current_user)):
    referrals = await db.referrals.find().to_list(100)
    return referrals

@router.get("/stats", response_model=Any)
async def get_referral_stats(db = Depends(get_database), current_user = Depends(get_current_user)):
    pipeline = [
        {"$group": {"_id": "$referrer_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    stats = await db.referrals.aggregate(pipeline).to_list(10)
    return stats
