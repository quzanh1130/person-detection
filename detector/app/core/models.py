from pydantic import BaseModel
from typing import Any, Dict, Optional

class ResponseFormat(BaseModel):
    status: str
    message: str
    data: Optional[Dict[str, Any]] = None  # Allow data to be None