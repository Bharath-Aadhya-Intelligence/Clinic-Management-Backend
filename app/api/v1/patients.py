from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Optional
from datetime import date
from ...services.patient import patient_service
from ...models.patient import PatientOut, PatientCreate, PatientUpdate, ReferralSource
from ...api.deps import get_current_admin
from ...core.rate_limit import limiter

router = APIRouter()

@router.get("/meta/referral-sources", response_model=List[str])
async def get_referral_sources():
    return [source.value for source in ReferralSource]

@router.get("/", response_model=List[PatientOut])
@limiter.limit("60/minute")
async def list_patients(request: Request, visit_date: Optional[date] = None, current_admin: dict = Depends(get_current_admin)):
    if visit_date:
        return await patient_service.get_patients_by_visit_date(visit_date)
    return await patient_service.get_all()

@router.get("/{id}", response_model=PatientOut)
@limiter.limit("60/minute")
async def get_patient(request: Request, id: str, current_admin: dict = Depends(get_current_admin)):
    patient = await patient_service.get_by_id(id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
async def create_patient(patient: PatientCreate):
    return await patient_service.create_patient(patient.dict())

@router.patch("/{id}", response_model=PatientOut)
async def update_patient(id: str, update: PatientUpdate, current_admin: dict = Depends(get_current_admin)):
    # Convert dates in appointments if present
    update_data = update.dict(exclude_unset=True)
    if "appointments" in update_data:
        # Pydantic handles date serialization/deserialization, but Motor needs datetime or date objects
        pass
        
    success = await patient_service.update_patient(id, update_data)
    if not success:
        raise HTTPException(status_code=400, detail="Update failed")
    return await patient_service.get_by_id(id)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(id: str, current_admin: dict = Depends(get_current_admin)):
    success = await patient_service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Patient not found")
    return None
