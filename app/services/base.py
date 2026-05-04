from typing import List, Optional, Any, Dict
from bson import ObjectId
from ..core.db import get_database

class BaseService:
    def __init__(self, collection_name: str):
        self.collection_name = collection_name

    @property
    def collection(self):
        db = get_database()
        return db[self.collection_name]

    async def get_all(self, query: Dict = {}) -> List[Dict]:
        cursor = self.collection.find(query)
        return await cursor.to_list(length=1000)

    async def get_count(self, query: Dict = {}) -> int:
        return await self.collection.count_documents(query)

    async def get_by_id(self, id: str) -> Optional[Dict]:
        if not ObjectId.is_valid(id):
            return None
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def create(self, data: Dict) -> Dict:
        result = await self.collection.insert_one(data)
        data["_id"] = result.inserted_id
        return data

    async def update(self, id: str, data: Dict) -> bool:
        if not ObjectId.is_valid(id):
            return False
        result = await self.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return result.modified_count > 0

    async def delete(self, id: str) -> bool:
        if not ObjectId.is_valid(id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(id)})
        return result.deleted_count > 0
