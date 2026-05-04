from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from enum import Enum
from .base import PyObjectId, MongoBaseModel

class OrderStatus(str, Enum):
    PENDING = "Pending"
    CONTACTED = "Contacted"
    COMPLETED = "Completed"

class OrderBase(MongoBaseModel):
    customer_name: str
    phone_number: str
    address: str
    medicine_id: str
    medicine_name: str
    medicine_price: float

class OrderCreate(OrderBase):
    pass

class OrderInDB(OrderBase):
    id: Optional[PyObjectId] = Field(alias="_id", serialization_alias="id", default=None)
    order_date: datetime = Field(default_factory=datetime.utcnow)
    status: OrderStatus = OrderStatus.PENDING

class OrderOut(OrderInDB):
    pass
    
class OrderUpdate(BaseModel):
    status: OrderStatus
