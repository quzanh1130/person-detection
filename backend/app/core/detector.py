import os
import requests
from .logger import setup_logger

logger = setup_logger(__name__)

DETECT_URL = os.getenv("DETECT_URL", "http://localhost:6868/api/v1/detect/")
CONFIDENT_THRESHOLD = os.getenv("CONFIDENT_THRESHOLD", 0.5)

def call_detect_objects_api_sync(file_path: str, class_name: str = "person", conf: float = 0.5, api_url: str = "http://localhost:6868/api/v1/detect/"):
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file, "image/jpeg")}
        params = {"class_name": class_name, "conf": conf}
        
        logger.info(f"Sending request to {api_url} with params: {params}")
        response = requests.post(api_url, files=files, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error: {response.status_code}, Message: {response.text}")
            logger.error(f"Request params: {params}")
            logger.error(f"Request headers: {response.request.headers}")
            return None
        
def detect_person(file_path: str):
    try:
        class_name = "person"
        result = call_detect_objects_api_sync(file_path=file_path, class_name=class_name, conf=CONFIDENT_THRESHOLD, api_url=DETECT_URL)
        return result
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return None