from fastapi import APIRouter, Depends, HTTPException, status, Request
from typing import List, Optional
from ...services.order import order_service
from ...models.order import OrderOut, OrderCreate, OrderUpdate
from ...api.deps import get_current_admin
from ...core.rate_limit import limiter

router = APIRouter()

@router.post("/", response_model=OrderOut, status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def place_order(request: Request, order: OrderCreate):
    return await order_service.create_order(order.dict())

@router.get("/admin", response_model=List[OrderOut])
@limiter.limit("30/minute")
async def list_orders_admin(request: Request, current_admin: dict = Depends(get_current_admin)):
    return await order_service.get_all()

@router.delete("/admin/clear-all", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_orders_admin(current_admin: dict = Depends(get_current_admin)):
    await order_service.delete_all()
    return None

@router.get("/admin/{id}", response_model=OrderOut)
async def get_order_admin(id: str, current_admin: dict = Depends(get_current_admin)):
    order = await order_service.get_by_id(id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.patch("/admin/{id}", response_model=OrderOut)
async def update_order_status_admin(id: str, update: OrderUpdate, current_admin: dict = Depends(get_current_admin)):
    success = await order_service.update_status(id, update.status)
    if not success:
        raise HTTPException(status_code=400, detail="Update failed")
    return await order_service.get_by_id(id)

@router.delete("/admin/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_admin(id: str, current_admin: dict = Depends(get_current_admin)):
    success = await order_service.delete(id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return None
