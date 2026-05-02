from .base import BaseService
from datetime import datetime

class MedicineService(BaseService):
    def __init__(self):
        super().__init__("medicines")

    async def get_active_medicines(self):
        return await self.get_all({"is_active": True})

    async def create_medicine(self, data: dict):
        data["created_at"] = datetime.utcnow()
        data["updated_at"] = datetime.utcnow()
        return await self.create(data)

    async def update_medicine(self, id: str, data: dict):
        data["updated_at"] = datetime.utcnow()
        return await self.update(id, data)

medicine_service = MedicineService()
