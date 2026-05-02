from fastapi import APIRouter, HTTPException, Depends, status, Response
from app.models.bill import Bill
from app.utils.db import get_database
from app.utils.deps import get_current_user
from typing import List
from bson import ObjectId

router = APIRouter(prefix="/bills", tags=["Bills"])

@router.post("/", response_model=Bill, status_code=status.HTTP_201_CREATED)
async def create_bill(bill: Bill, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(bill.patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient_id")
        
    bill_dict = {k: v for k, v in bill.model_dump(by_alias=True).items() if v is not None}
    new_bill = await db.bills.insert_one(bill_dict)
    created_bill = await db.bills.find_one({"_id": new_bill.inserted_id})
    return created_bill

@router.get("/{patient_id}", response_model=List[Bill])
async def get_patient_bills(patient_id: str, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(patient_id):
        raise HTTPException(status_code=400, detail="Invalid patient_id")
    bills = await db.bills.find({"patient_id": patient_id}).to_list(100)
    return bills

@router.get("/{id}/pdf")
async def generate_bill_pdf(id: str, db = Depends(get_database), current_user = Depends(get_current_user)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail="Invalid ID")
    bill = await db.bills.find_one({"_id": ObjectId(id)})
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
        
    # STUB: In a real app, generate PDF using reportlab or similar library
    # Here we just return a mock response for now
    pdf_content = b"%PDF-1.4\n%Stub PDF Document\n"
    return Response(content=pdf_content, media_type="application/pdf")
