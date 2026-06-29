from fastapi import FastAPI
from app.config import settings

app = FastAPI(title=settings.app_name)

@app.get("/")
def read_root():
    return {"message": f"Welcome to {settings.app_name} API"}