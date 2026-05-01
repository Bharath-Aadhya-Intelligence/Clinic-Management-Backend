from fastapi import APIRouter, HTTPException, Depends, status
from app.models.patient import Patient
from app.utils.db import get_database
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=Patient, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: Patient, db = Depends(get_database)):
    patient_dict = {k: v for k, v in patient.model_dump(by_alias=True).items() if v is not None}
    new_patient = await db.patients.insert_one(patient_dict)
    created_patient = await db.patients.find_one({"_id": new_patient.inserted_id})
    return created_patient

@router.get("/", response_model=List[Patient])
async def list_patients(db = Depends(get_database)):
    patients = await db.patients.find().to_list(100)
    return patients

@router.get("/{id}", response_model=Patient)
async def get_patient(id: str, db = Depends(get_database)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    patient = await db.patients.find_one({"_id": ObjectId(id)})
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.put("/{id}", response_model=Patient)
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
