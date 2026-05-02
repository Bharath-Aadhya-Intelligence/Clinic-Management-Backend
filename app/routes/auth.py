from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.db import get_database
from app.models.user import User
from app.models.patient import Patient
from app.schemas.auth import UserCreate, Token, PatientLogin, PatientCreate, UserLogin
from app.utils.security import get_password_hash, verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta, datetime, timezone
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/patient/register", response_model=Patient, status_code=status.HTTP_201_CREATED, response_model_exclude={"password_hash"})
async def patient_register(patient_in: PatientCreate, db = Depends(get_database)):
    logger.info(f"Patient registration attempt for phone: {patient_in.phone}")
    
    # Check in patients_auth (the registration folder)
    existing_auth = await db.patients_auth.find_one({"phone": patient_in.phone})
    if existing_auth:
        logger.warning(f"Registration failed: Phone {patient_in.phone} already exists")
        raise HTTPException(status_code=400, detail="Phone number already registered")
        
    # Prepare auth data (for patients_auth folder)
    auth_dict = {
        "phone": patient_in.phone,
        "password_hash": get_password_hash(patient_in.password),
        "created_at": datetime.now(timezone.utc)
    }
    
    # Prepare profile data (for patients folder)
    profile_dict = {
        "name": patient_in.name,
        "phone": patient_in.phone,
        "created_at": datetime.now(timezone.utc),
        "updated_at": datetime.now(timezone.utc)
    }
    
    # Insert into both collections with the same ID
    new_auth = await db.patients_auth.insert_one(auth_dict)
    patient_id = new_auth.inserted_id
    
    profile_dict["_id"] = patient_id
    await db.patients.insert_one(profile_dict)
    
    # Return the profile
    created_patient = await db.patients.find_one({"_id": patient_id})
    logger.info(f"Patient registered successfully in separate folders: {patient_in.phone}")
    return created_patient

@router.post("/login", response_model=Token)
async def login(login_data: UserLogin, db = Depends(get_database)):
    logger.info(f"Admin login attempt for: {login_data.email}")
    
    # Search in admins folder
    user = await db.admins.find_one({"email": login_data.email})
    
    if not user:
        logger.warning(f"Admin not found: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    if not verify_password(login_data.password, user["password_hash"]):
        logger.warning(f"Invalid password for admin: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
        
    logger.info(f"Admin login successful: {login_data.email}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user["_id"]), "email": user.get("email"), "role": user.get("role")}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/patient/login", response_model=Token)
async def patient_login(login_data: PatientLogin, db = Depends(get_database)):
    logger.info(f"Patient login attempt for phone: {login_data.phone}")
    
    # Search in patients_auth folder
    patient_auth = await db.patients_auth.find_one({"phone": login_data.phone})
    
    if not patient_auth:
        logger.warning(f"Patient credentials not found: {login_data.phone}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
        )
        
    if not verify_password(login_data.password, patient_auth["password_hash"]):
        logger.warning(f"Invalid password for patient: {login_data.phone}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect phone or password",
        )
        
    logger.info(f"Patient login successful: {login_data.phone}")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(patient_auth["_id"]), "phone": patient_auth["phone"], "role": "patient"}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
