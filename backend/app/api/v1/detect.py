import os
import json
import shutil
import uuid
import datetime
import base64
import cv2
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from app.core.logger import setup_logger
from app.core.detector import detect_person
from app.core.models import DetectionRecord
from app.database.schema import DetectionResponse
from app.database.db import get_db

logger = setup_logger(__name__)
detect_router = APIRouter()

@detect_router.post("/", response_model=DetectionResponse)
async def detect_people(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create unique filename
    file_id = str(uuid.uuid4())
    original_filename = file.filename
    extension = original_filename.split(".")[-1]
    upload_path = f"uploads/{file_id}.{extension}"
    result_path = f"results/{file_id}.{extension}"
    
    # Save uploaded file
    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Run person detection
    try:
        detection_response = detect_person(upload_path)
        if not isinstance(detection_response, dict) or "data" not in detection_response or "detections" not in detection_response["data"]:
            raise HTTPException(status_code=500, detail="Invalid detection result format")
        detect_results = detection_response["data"]["detections"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Detection failed: {str(e)}")
    
    # Process detections and save cropped images
    try:
        # Read the image using OpenCV
        img = cv2.imread(upload_path)
        if img is None:
            raise HTTPException(status_code=500, detail="Failed to read the image")
        
        for idx, detection in enumerate(detect_results):
            try:
                x_min, y_min, x_max, y_max = map(int, [
                    detection["x_min"], detection["y_min"], detection["x_max"], detection["y_max"]
                ])
            except KeyError as e:
                raise HTTPException(status_code=500, detail=f"Invalid detection result format: {str(e)}")
            
            # Draw bounding box on the image
            label = f"Person {idx+1}"
            cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            cv2.putText(img, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            # cv2.rectangle(img, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)
            
            # Crop the detected region
            cropped_img = img[y_min:y_max, x_min:x_max]
            cropped_path = f"results/{file_id}_crop_{idx}.{extension}"
            
            # Save the cropped image
            cv2.imwrite(cropped_path, cropped_img)

        # Save the final image with bounding boxes
        cv2.imwrite(result_path, img)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing images: {str(e)}")
    
    # Create database record
    db_record = DetectionRecord(
        timestamp=datetime.datetime.now(),
        people_count=len(detect_results),
        result_image_url=result_path,
        original_filename=original_filename,
    )
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    
    # Return response
    return {
        "id": db_record.id,
        "timestamp": db_record.timestamp,
        "people_count": len(detect_results),
        "result_image_url": f"/images/{file_id}.{extension}",
        "original_filename": original_filename
    }

@detect_router.get("/images/{filename}")
async def get_image(filename: str):
    """
    Serve image files from the results directory by filename
    """
    # Build the file path
    file_path = f"results/{filename}"
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"Image '{filename}' not found")
    
    # Return the file with the appropriate media type
    return FileResponse(
        file_path, 
        media_type=f"image/{filename.split('.')[-1]}"
    )