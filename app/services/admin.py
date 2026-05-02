from .base import BaseService
from ..models.admin import AdminInDB
from ..core.security import get_password_hash

class AdminService(BaseService):
    def __init__(self):
        super().__init__("admins")

    async def get_by_username(self, username: str):
        return await self.collection.find_one({"username": username})

    async def get_by_email(self, email: str):
        return await self.collection.find_one({"email": email})

    async def create_admin(self, admin_data: dict):
        admin_data["hashed_password"] = get_password_hash(admin_data.pop("password"))
        return await self.create(admin_data)

admin_service = AdminService()
