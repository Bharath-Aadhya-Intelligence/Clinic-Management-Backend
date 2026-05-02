from fastapi import APIRouter, HTTPException, Depends, status
from app.models.appointment import Appointment
from app.utils.db import get_database
from app.utils.deps import get_current_user
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: Appointment, db = Depends(get_database), current_user = Depends(get_current_user)):
    # Validate patient_id
    if not ObjectId.is_valid(appointment.patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient_id")
    patient = await db.patients.find_one({"_id": ObjectId(appointment.patient_id)})
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    app_dict = {k: v for k, v in appointment.model_dump(by_alias=True).items() if v is not None}
    new_app = await db.appointments.insert_one(app_dict)
    created_app = await db.appointments.find_one({"_id": new_app.inserted_id})
    return created_app

@router.get("/", response_model=List[Appointment])
async def list_appointments(db = Depends(get_database), current_user = Depends(get_current_user)):
    apps = await db.appointments.find().to_list(100)
    return apps

@router.get("/{patient_id}", response_model=List[Appointment])
async def get_patient_appointments(patient_id: str, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient ID")
    apps = await db.appointments.find({"patient_id": patient_id}).to_list(100)
    return apps

@router.put("/{id}", response_model=Appointment)
async def update_appointment(id: str, appointment: Appointment, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    update_data = {k: v for k, v in appointment.model_dump(by_alias=True).items() if k != "_id"}
    result = await db.appointments.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.modified_count == 0:
         raise HTTPException(status_code=404, detail="Appointment not found or no changes made")
    updated_app = await db.appointments.find_one({"_id": ObjectId(id)})
    return updated_app
