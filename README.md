# Deepfake Detection Project

This project provides a web application for detecting deepfake images and videos using deep learning techniques.

## Project Structure

```
project/
├── backend/              # FastAPI backend
│   ├── main.py           # FastAPI application
│   ├── requirements.txt  # Backend dependencies
│   └── uploads/          # Temporary upload directory
├── frontend/             # React.js frontend
│   ├── public/           # Static assets
│   ├── src/              # React source code
│   │   ├── components/   # Reusable UI components
│   │   ├── pages/        # Page components
│   │   └── services/     # API communication
│   └── package.json      # Frontend dependencies
├── deepfake_detection.py # Deepfake detection functionality
├── train_model.py        # Model training script
└── requirements.txt      # Python dependencies for the ML model
```

## Tech Stack

- **Frontend**: React.js with Material-UI
- **Backend**: FastAPI (Python)
- **Machine Learning**: TensorFlow, PyTorch, OpenCV, MTCNN

## Getting Started

### Backend Setup

1. Install the required dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Start the backend server:
   ```bash
   cd backend
   python main.py
   ```
   The server will be running at http://localhost:8000

### Frontend Setup

1. Install the required dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Start the development server:
   ```bash
   cd frontend
   npm start
   ```
   The application will be running at http://localhost:3000

## Usage

1. Navigate to http://localhost:3000 in your web browser
2. Upload an image or video for analysis
3. View the detection results, which include a confidence score indicating the likelihood of the media being a deepfake

## Features

- Upload and analyze images (JPG, PNG) and videos (MP4)
- Real-time deepfake detection using a pre-trained model
- User-friendly interface with a clean, modern design
- Detailed results with confidence scoring and visualization

## Model Information

The deepfake detection model uses an Xception architecture pre-trained on ImageNet and fine-tuned on deepfake datasets. The model analyzes visual content to identify inconsistencies that may indicate manipulation.

## License

This project is intended for educational and research purposes only. 