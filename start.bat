@echo off
echo ===================================================
echo   Starting NutriTrack Services
echo ===================================================
echo.

echo Starting Node.js (Express) Backend on Port 5000...
start cmd /k "node server.js"

echo Starting Python (Flask) AI Backend on Port 5001...
start cmd /k "cd nutritrack_flask && python app.py"

echo Starting Frontend Web Server on Port 5500...
start cmd /k "npx serve . -p 5500"

echo.
echo All services are launching in separate windows!
echo Please wait a few seconds, then open your browser and go to:
echo http://localhost:5500
echo.
pause
