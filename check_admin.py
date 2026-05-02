import asyncio
import os
from app.utils.db import get_database

async def main():
    db = await get_database()
    count = await db.users.count_documents({})
    admin = await db.users.find_one({"email": "admin@clinic.com"})
    print(f"Total Users: {count}")
    if admin:
        print(f"Admin Found: {admin['email']}")
        print(f"Admin Role: {admin.get('role')}")
        print(f"Admin Hash: {admin.get('password_hash')}")
    else:
        print("Admin Not Found")

if __name__ == "__main__":
    asyncio.run(main())
