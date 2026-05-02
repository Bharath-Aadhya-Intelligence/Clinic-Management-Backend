from fastapi import FastAPI, Request, status, Response
from datetime import datetime, timezone
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from app.routes import patients, auth, appointments, referrals, medicines, bills, analytics
from app.utils.db import get_database
from app.utils.security import get_password_hash
from app.models.user import User

app = FastAPI(title="Clinic Management System API")

@app.on_event("startup")
async def startup_event():
    db = await get_database()
    # Check if specific admin exists
    admin_email = "admin@clinic.com"
    existing_admin = await db.admins.find_one({"email": admin_email})
    password = "admin123"
    hashed_password = get_password_hash(password)
    
    if not existing_admin:
        logger.info(f"Admin {admin_email} not found. Creating default admin...")
        admin_data = {
            "name": "Super Admin",
            "phone": "+1234567890",
            "email": admin_email,
            "role": "admin",
            "password_hash": hashed_password,
            "created_at": datetime.now(timezone.utc)
        }
        await db.admins.insert_one(admin_data)
        logger.info(f"Default admin created: {admin_email} / {password}")
    elif "password_hash" not in existing_admin:
        logger.info(f"Admin {admin_email} found but missing password. Updating...")
        await db.admins.update_one(
            {"email": admin_email},
            {"$set": {"password_hash": hashed_password}}
        )
        logger.info(f"Admin {admin_email} password updated to: {password}")
    else:
        logger.info(f"Admin {admin_email} already exists and is configured.")

app.include_router(auth.router)
app.include_router(patients.router)
app.include_router(appointments.router)
app.include_router(referrals.router)
app.include_router(medicines.router)
app.include_router(bills.router)
app.include_router(analytics.router)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = exc.errors()
    logger.error(f"Validation error: {error_details}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": error_details}),
    )


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.get("/")
async def root():
    return {"message": "Welcome to the Clinic Management System API"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
