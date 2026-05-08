from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.db import connect_to_mongo, close_mongo_connection
from app.core.config import settings
import os
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.rate_limit import limiter

app = FastAPI(
    title="Homeopathy Hospital Management System API",
    version="1.0.0",
    description="Backend API for Homeopathy Hospital Management System"
)

# Add SlowAPI state and middleware
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for medicine images
os.makedirs(settings.STATIC_DIR, exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to Homeopathy Hospital Management System API", "version": "1.0.0"}

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

from app.api.v1 import auth, medicines, orders, patients, analytics

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(medicines.router, prefix="/api/v1/medicines", tags=["Medicines"])
app.include_router(orders.router, prefix="/api/v1/orders", tags=["Orders"])
app.include_router(patients.router, prefix="/api/v1/patients", tags=["Patients"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
