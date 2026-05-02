import asyncio
from app.core.db import connect_to_mongo, close_mongo_connection
from app.services.admin import admin_service
from app.core.config import settings

async def seed_admin():
    await connect_to_mongo()
    
    # Check if admin already exists
    existing = await admin_service.get_by_username("admin")
    if existing:
        print("Admin user already exists.")
    else:
        admin_data = {
            "username": "admin",
            "email": "admin@hospital.com",
            "password": "adminpassword123", # User should change this
            "is_active": True
        }
        await admin_service.create_admin(admin_data)
        print("Admin user created: admin / adminpassword123")
    
    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(seed_admin())
