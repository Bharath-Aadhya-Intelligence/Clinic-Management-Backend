from fastapi import APIRouter, Depends, HTTPException, status, Form
from datetime import timedelta
from ...core.security import verify_password, create_access_token, create_refresh_token, decode_token
from ...core.config import settings
from ...services.admin import admin_service
from ...models.admin import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login_for_access_token(
    email: str = Form(...),
    password: str = Form(...)
):
    admin = await admin_service.get_by_email(email)
    if not admin or not verify_password(password, admin["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": admin["username"]})
    refresh_token = create_refresh_token(data={"sub": admin["username"]})
    
    return {
        "access_token": access_token, 
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_access_token(refresh_token: str = Form(...)):
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )
    
    username = payload.get("sub")
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload",
        )
        
    new_access_token = create_access_token(data={"sub": username})
    new_refresh_token = create_refresh_token(data={"sub": username})
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
