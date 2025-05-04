from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import shutil
from tempfile import NamedTemporaryFile
import sys

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import deepfake detection functionality
from deepfake_detection import build_model, detect_deepfake

# Create FastAPI app
app = FastAPI(
    title="Deepfake Detection API",
    description="API for detecting deepfake images and videos",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure upload directory
UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Initialize the model on startup
model = None

@app.on_event("startup")
async def startup_event():
    global model
    try:
        # Use the existing model building function
        model = build_model()
        print("Model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        model = None

@app.get("/")
async def root():
    return {"message": "Deepfake Detection API is running"}

@app.post("/api/detect")
async def detect_file(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    # Check file extension
    allowed_extensions = {".jpg", ".jpeg", ".png", ".mp4"}
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file type. Allowed types: {', '.join(allowed_extensions)}"
        )
    
    # Save the uploaded file temporarily
    with NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        shutil.copyfileobj(file.file, temp_file)
        temp_file_path = temp_file.name
    
    try:
        # Process the file based on the type
        is_video = file_ext == ".mp4"
        confidence, message = detect_deepfake(model, temp_file_path, is_video)
        
        # Return the result
        return {
            "filename": file.filename,
            "confidence": float(confidence),
            "result": message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up the temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.get("/api/stats")
async def get_stats():
    # This could be expanded to provide real statistics about model performance
    return {
        "model_accuracy": 0.92,
        "total_processed": 1250,
        "true_positives": 580,
        "false_positives": 48,
        "true_negatives": 570,
        "false_negatives": 52
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 