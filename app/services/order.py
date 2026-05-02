from .base import BaseService
from datetime import datetime
from ..models.order import OrderStatus

class OrderService(BaseService):
    def __init__(self):
        super().__init__("orders")

    async def create_order(self, data: dict):
        data["order_date"] = datetime.utcnow()
        data["status"] = OrderStatus.PENDING
        return await self.create(data)

    async def update_status(self, id: str, status: str):
        return await self.update(id, {"status": status})

order_service = OrderService()
