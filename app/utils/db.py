import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME", "clinic_management")

client = AsyncIOMotorClient(MONGO_URL)
db = client[DATABASE_NAME]

async def get_database():
    return db
