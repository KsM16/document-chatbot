# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings

# 1. Initialize the FastAPI app using the central config
app = FastAPI(title=settings.APP_NAME)

# 2. Configure CORS
# Parse the comma-separated string from .env into a clean list of origins
origins = [origin.strip() for origin in settings.ALLOWED_ORIGINS.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Health Check Endpoint
@app.get("/health")
def health_check():
    """
    Simple endpoint to verify the API is running and responsive.
    Used by Railway (hosting) and load balancers to check service health.
    """
    return {"status": "ok"}

# Optional: A root endpoint to confirm the app name
@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.APP_NAME}"}