# Because my laptop is not have gpu, so I use ultralytics/ultralytics:latest-cpu
# If you have gpu, you can use ultralytics/ultralytics:latest
FROM ultralytics/ultralytics:latest-cpu

# Set working directory
WORKDIR /app

# Copy and install Python dependencies early for caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model
COPY app/ .
COPY app/model/yolo12s.onnx /app/yolo12s.onnx

# Expose FastAPI port
EXPOSE 6868

# Run FastAPI with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6868"]
