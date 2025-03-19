import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.core.logger import setup_logger
from app.core.models import DetectionRecord
from app.database.schema import DetectionHistory
from app.database.db import SessionLocal, engine

logger = setup_logger(__name__)
history_router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@history_router.get("", response_model=List[DetectionHistory])
def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_people: Optional[int] = Query(None, ge=0),
    max_people: Optional[int] = Query(None, ge=0),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(DetectionRecord)
    
    # Apply filters
    if min_people is not None:
        query = query.filter(DetectionRecord.people_count >= min_people)
    if max_people is not None:
        query = query.filter(DetectionRecord.people_count <= max_people)
    if date_from is not None:
        query = query.filter(DetectionRecord.timestamp >= date_from)
    if date_to is not None:
        query = query.filter(DetectionRecord.timestamp <= date_to)
    
    # Get total count for pagination
    total_count = query.count()
    
    # Apply pagination
    records = query.order_by(DetectionRecord.timestamp.desc()).offset(skip).limit(limit).all()
    
    # Format results
    results = []
    for record in records:
        # file_path = os.path.basename()
        results.append({
            "id": record.id,
            "timestamp": record.timestamp,
            "people_count": record.people_count,
            "result_image_url": record.result_image_url,
            "original_filename": record.original_filename
        })
    
    return results

@history_router.get("/count")
def get_history_count(
    min_people: Optional[int] = Query(None, ge=0),
    max_people: Optional[int] = Query(None, ge=0),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(DetectionRecord)
    
    # Apply filters
    if min_people is not None:
        query = query.filter(DetectionRecord.people_count >= min_people)
    if max_people is not None:
        query = query.filter(DetectionRecord.people_count <= max_people)
    if date_from is not None:
        query = query.filter(DetectionRecord.timestamp >= date_from)
    if date_to is not None:
        query = query.filter(DetectionRecord.timestamp <= date_to)
    
    total_count = query.count()
    return {"count": total_count}

@history_router.get("/{record_id}", response_model=DetectionHistory)
def get_history_item(record_id: int, db: Session = Depends(get_db)):
    record = db.query(DetectionRecord).filter(DetectionRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return {
        "id": record.id,
        "timestamp": record.timestamp,
        "people_count": record.people_count,
        "result_image_url": record.result_image_path,
        "original_filename": record.original_filename
    }