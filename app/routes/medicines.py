from fastapi import APIRouter, HTTPException, Depends, status
from app.models.medicine import Medicine
from app.utils.db import get_database
from app.utils.deps import get_current_user
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/medicines", tags=["Medicines"])

@router.post("/", response_model=Medicine, status_code=status.HTTP_201_CREATED)
async def create_medicine(medicine: Medicine, db = Depends(get_database), current_user = Depends(get_current_user)):
    med_dict = {k: v for k, v in medicine.model_dump(by_alias=True).items() if v is not None}
    new_med = await db.medicines.insert_one(med_dict)
    created_med = await db.medicines.find_one({"_id": new_med.inserted_id})
    return created_med

@router.get("/", response_model=List[Medicine])
async def list_medicines(db = Depends(get_database), current_user = Depends(get_current_user)):
    medicines = await db.medicines.find().to_list(100)
    return medicines

@router.get("/{id}", response_model=Medicine)
async def get_medicine(id: str, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    medicine = await db.medicines.find_one({"_id": ObjectId(id)})
    if medicine is None:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.put("/{id}", response_model=Medicine)
async def update_medicine(id: str, medicine: Medicine, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = {k: v for k, v in medicine.model_dump(by_alias=True).items() if k != "_id"}
    result = await db.medicines.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
         raise HTTPException(status_code=404, detail="Medicine not found or no changes made")
    updated_med = await db.medicines.find_one({"_id": ObjectId(id)})
    return updated_med

@router.delete("/{id}")
async def delete_medicine(id: str, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = await db.medicines.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return {"message": "Medicine deleted successfully"}
