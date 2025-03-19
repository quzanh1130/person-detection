import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1 import detect_router, history_router
from app.database.db import init_db
from app.core.logger import setup_logger

logger = setup_logger(__name__)

# Init FastAPI
app = FastAPI(title="Backend Person Detection System")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads and results directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("results", exist_ok=True)

# Mount static files
app.mount("/images", StaticFiles(directory="results"), name="images")

# Initialize the database on startup
@app.on_event("startup")
async def startup_db_client():
    logger.info("Initializing database...")
    init_db()
    logger.info("Database initialized successfully!")

# Include routers
app.include_router(detect_router, prefix="/api/v1/detect", tags=["detection"])
app.include_router(history_router, prefix="/api/v1/history", tags=["history"])

@app.get("/")
async def root():
    return {"status": "200","success": True, "message": "Welcome to the Backend Person Detection API!", "data": None}
