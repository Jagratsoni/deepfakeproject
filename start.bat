@echo off
echo Starting Deepfake Detection Application...

:: Start backend server
start cmd /k "cd backend && python main.py"

:: Wait for backend to start
timeout /t 5

:: Start frontend development server
start cmd /k "cd frontend && npm start"

echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000 