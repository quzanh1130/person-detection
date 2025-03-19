import cv2
import numpy as np
from fastapi import Request, APIRouter, UploadFile, File, Query
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from ultralytics import YOLO
from core.logger import setup_logger
from core.models import ResponseFormat
from core.detector import predict_and_detect
import torch

logger = setup_logger(__name__)
router = APIRouter()

# Load model (ensure correct path) with explicit CPU device
try:
    model = YOLO("yolo12s.onnx") 
    logger.info("YOLO model loaded successfully")
except Exception as e:
    logger.error(f"Error loading YOLO model: {e}")
    raise RuntimeError("Failed to load YOLO model")

@router.post("")
async def detect_objects(
    file: UploadFile = File(...),
    class_name: str = Query("person", min_length=1, max_length=50),
    conf: float = Query(0.5, ge=0.0, le=1.0)
):
    try:
        logger.info(f"Received file: {file.filename} | Class: {class_name} | Confidence: {conf}")

        # Read image as numpy array
        contents = await file.read()
        np_img = np.frombuffer(contents, np.uint8)

        if np_img.size == 0:
            logger.error(f"File {file.filename} is empty or not an image")
            return JSONResponse(
                content=ResponseFormat.format_response(
                    status="error",
                    message="Uploaded file is not a valid image",
                    data=None
                ).dict(),  # Convert to dictionary
                status_code=400
            )

        img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)

        if img is None:
            logger.error(f"Failed to decode image: {file.filename}")
            return JSONResponse(
                content=ResponseFormat(
                    status="error",
                    message="Could not decode image file",
                    data=None
                ).dict(),  # Convert to dictionary
                status_code=400
            )

        # Perform detection
        results = await predict_and_detect(model, img, class_name, conf)

        if not results:
            logger.warning(f"No detections found for {class_name} in {file.filename}")
            return JSONResponse(
                content=ResponseFormat(
                    status="success",
                    message="No objects detected",
                    data=None
                ).dict()  # Convert to dictionary
            )

        # Extract bounding box details
        detections = []
        for result in results:
            for box in result.boxes:
                detections.append({
                    "x_min": int(box.xyxy[0][0]),
                    "y_min": int(box.xyxy[0][1]),
                    "x_max": int(box.xyxy[0][2]),
                    "y_max": int(box.xyxy[0][3]),
                    "confidence": float(box.conf[0]),
                    "class_name": class_name
                })

        logger.info(f"Detection completed successfully for {file.filename}")
        return JSONResponse(
            content=ResponseFormat(
                status="success",
                message="Detection completed successfully",
                data={"detections": detections}  # Ensure `data` is a dictionary
            ).dict()  # Convert to dictionary
        )

    except cv2.error as cv_error:
        logger.error(f"OpenCV error processing {file.filename}: {cv_error}")
        return JSONResponse(
            content=ResponseFormat(
                status="error",
                message="Error processing image with OpenCV",
                data=None
            ).dict(),  # Convert to dictionary
            status_code=500
        )

    except ValueError as ve:
        logger.error(f"Value error while detecting objects in {file.filename}: {ve}")
        return JSONResponse(
            content=ResponseFormat(
                status="error",
                message="Invalid input or processing error",
                data=None
            ).dict(),  # Convert to dictionary
            status_code=400
        )

    except Exception as e:
        logger.exception(f"Unexpected error processing {file.filename}: {e}")
        return JSONResponse(
            content=ResponseFormat(
                status="error",
                message="An unexpected error occurred during detection",
                data=None
            ).dict(),  # Convert to dictionary
            status_code=500
        )
