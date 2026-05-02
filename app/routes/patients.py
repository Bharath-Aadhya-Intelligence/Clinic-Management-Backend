from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timezone
from app.models.patient import Patient
from app.utils.db import get_database
from app.utils.security import get_password_hash
from typing import List
from bson import ObjectId

from app.schemas.auth import PatientCreate

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.get("/", response_model=List[Patient], response_model_exclude={"password_hash"})
async def list_patients(db = Depends(get_database)):
    patients = await db.patients.find().to_list(100)
    return patients

@router.get("/{id}", response_model=Patient, response_model_exclude={"password_hash"})
async def get_patient(id: str, db = Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    patient = await db.patients.find_one({"_id": ObjectId(id)})
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{id}", response_model=Patient, response_model_exclude={"password_hash"})
async def update_patient(id: str, patient: Patient, db = Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = {k: v for k, v in patient.model_dump(by_alias=True).items() if k != "_id"}
    result = await db.patients.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
         raise HTTPException(status_code=404, detail="Patient not found or no changes made")
    updated_patient = await db.patients.find_one({"_id": ObjectId(id)})
    return updated_patient

@router.delete("/{id}")
async def delete_patient(id: str, db = Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    result = await db.patients.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {"message": "Patient deleted successfully"}
