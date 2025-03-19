from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.detect import router as detector_router

# Init FastAPI
app = FastAPI(title="Person Detector API")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detector_router, prefix="/api/v1/detect", tags=["Person Detection"])

@app.get("/")
async def root():
    return {"status": "success", "message": "Welcome to the Person Detection API!", "data": None}
