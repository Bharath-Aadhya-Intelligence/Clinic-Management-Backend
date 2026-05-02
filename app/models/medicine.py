from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.common import PyObjectId

class Medicine(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    name: str
    price: float
    quantity: int
    category: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )
