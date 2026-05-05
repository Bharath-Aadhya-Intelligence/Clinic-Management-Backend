from fastapi import APIRouter, Depends, HTTPException, status, File, UploadFile, Form
from typing import List, Optional
from ...services.medicine import medicine_service
from ...models.medicine import MedicineOut, MedicineCreate, MedicineUpdate
from ...api.deps import get_current_admin
from ...utils.image_handler import compress_image, delete_image, get_image_base64
import json

router = APIRouter()

@router.get("/", response_model=List[MedicineOut])
async def list_medicines():
    medicines = await medicine_service.get_active_medicines()
    # Add full image URL if needed, but for now we just return the filename
    # Frontend can prepend the static URL
    return medicines

@router.get("/{id}", response_model=MedicineOut)
async def get_medicine(id: str):
    medicine = await medicine_service.get_by_id(id)
    if not medicine:
        raise HTTPException(status_code=404, detail="Medicine not found")
    return medicine

@router.post("/admin", response_model=MedicineOut, status_code=status.HTTP_201_CREATED)
async def create_medicine_admin(
    name: str = Form(...),
    price: float = Form(...),
    description: Optional[str] = Form(None),
    image: UploadFile = File(...),
    current_admin: dict = Depends(get_current_admin)
):
    # Compress and save image (local file)
    image_filename = compress_image(image, image.filename)
    # Get base64 for persistence
    image_data = get_image_base64(image)
    
    medicine_data = {
        "name": name,
        "price": price,
        "description": description,
        "image_filename": image_filename,
        "image_path": f"static/medicines/{image_filename}",
        "image_data": image_data,
        "is_active": True
    }
    
    new_medicine = await medicine_service.create_medicine(medicine_data)
    return new_medicine

@router.put("/admin/{id}", response_model=MedicineOut)
async def update_medicine_admin(
    id: str,
    name: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    description: Optional[str] = Form(None),
    is_active: Optional[bool] = Form(None),
    image: Optional[UploadFile] = File(None),
    current_admin: dict = Depends(get_current_admin)
):
    existing = await medicine_service.get_by_id(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    update_data = {}
    if name is not None: update_data["name"] = name
    if price is not None: update_data["price"] = price
    if description is not None: update_data["description"] = description
    if is_active is not None: update_data["is_active"] = is_active
    
    if image:
        # Delete old image if it exists
        if existing.get("image_filename"):
            delete_image(existing["image_filename"])
        # Save new image (local file)
        image_filename = compress_image(image, image.filename)
        # Get base64 for persistence
        image_data = get_image_base64(image)
        
        update_data["image_filename"] = image_filename
        update_data["image_path"] = f"static/medicines/{image_filename}"
        update_data["image_data"] = image_data
        
    success = await medicine_service.update_medicine(id, update_data)
    if not success:
        raise HTTPException(status_code=400, detail="Update failed")
        
    return await medicine_service.get_by_id(id)

@router.delete("/admin/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicine_admin(id: str, current_admin: dict = Depends(get_current_admin)):
    existing = await medicine_service.get_by_id(id)
    if not existing:
        raise HTTPException(status_code=404, detail="Medicine not found")
    
    # Delete image file
    if existing.get("image_filename"):
        delete_image(existing["image_filename"])
        
    await medicine_service.delete(id)
    return None
