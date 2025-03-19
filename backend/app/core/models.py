from sqlalchemy import Column, Integer, String, DateTime
from app.database.db import Base
import datetime

class DetectionRecord(Base):
    __tablename__ = "detection_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    people_count = Column(Integer, nullable=False)
    result_image_url = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)