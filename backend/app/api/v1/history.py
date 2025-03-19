import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.core.logger import setup_logger
from app.core.models import DetectionRecord
from app.database.schema import DetectionHistory
from app.database.db import get_db

logger = setup_logger(__name__)
history_router = APIRouter()

@history_router.get("", response_model=dict)
def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    min_people: Optional[int] = Query(None, ge=0),
    max_people: Optional[int] = Query(None, ge=0),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(DetectionRecord)
        logger.info(f"Retrieving history records: skip={skip}, limit={limit}, min_people={min_people}, max_people={max_people}, date_from={date_from}, date_to={date_to}")

        # Apply filters
        if min_people is not None:
            query = query.filter(DetectionRecord.people_count >= min_people)
        if max_people is not None:
            query = query.filter(DetectionRecord.people_count <= max_people)
        if date_from is not None:
            query = query.filter(DetectionRecord.timestamp >= date_from)
        if date_to is not None:
            query = query.filter(DetectionRecord.timestamp <= date_to)

        # Apply pagination
        records = query.order_by(DetectionRecord.timestamp.desc()).offset(skip).limit(limit).all()
        logger.info(f"Retrieved {len(records)} history records")
        
        # Convert ORM objects to serializable dictionaries
        serialized_records = [
            {
                "id": record.id,
                "timestamp": record.timestamp,
                "people_count": record.people_count,
                "result_image_url": record.result_image_url,
                "original_filename": record.original_filename
            }
            for record in records
        ]
        
        return {
            "status": "success",
            "message": "History records retrieved successfully",
            "data": serialized_records
        }
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}",
            "data": None
        }

@history_router.get("/count")
def get_history_count(
    min_people: Optional[int] = Query(None, ge=0),
    max_people: Optional[int] = Query(None, ge=0),
    date_from: Optional[str] = Query(None),
    date_to: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(DetectionRecord)
        logger.info(f"Retrieving history record count: min_people={min_people}, max_people={max_people}, date_from={date_from}, date_to={date_to}")
        
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
        logger.info(f"Retrieved total history record count: {total_count}")
        
        return {
            "status": "success",
            "message": "Count retrieved successfully.",
            "data": {"count": total_count}
        }
    
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        return {
            "status": "error",
            "message": f"An error occurred: {str(e)}",
            "data": None
        }

@history_router.get("/{record_id}")
def get_history_item(record_id: int, db: Session = Depends(get_db)):
    record = db.query(DetectionRecord).filter(DetectionRecord.id == record_id).first()
    logger.info(f"Retrieving history record with ID: {record_id}")
    if not record:
        logger.error(f"Record not found: {record}")
        raise HTTPException(
            status_code=404,
            detail={
                "status": "error",
                "message": "Record not found",
                "data": None
            }
        )
    
    logger.info(f"History record retrieved successfully: {record_id}")
    return {
        "status": "success",
        "message": "History record retrieved successfully",
        "data": {
            "id": record.id,
            "timestamp": record.timestamp,
            "people_count": record.people_count,
            "result_image_url": record.result_image_url,
            "original_filename": record.original_filename
        }
    }