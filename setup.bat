@echo off
echo Setting up Deepfake Detection Project...

:: Create upload directories
mkdir backend\uploads 2>nul
mkdir uploads 2>nul

:: Install backend dependencies
echo Installing backend dependencies...
pip install -r backend\requirements.txt

:: Install frontend dependencies
echo Installing frontend dependencies...
cd frontend
npm install
cd ..

echo Setup completed!
echo To start the application, run:
echo   start.bat 