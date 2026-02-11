@echo off
echo ================================================
echo  Online Exam Proctor System - Setup and Run
echo ================================================
echo.

echo [Step 1/4] Checking MongoDB status...
sc query MongoDB | find "RUNNING" >nul
if %errorlevel% neq 0 (
    echo MongoDB is not running. Attempting to start...
    net start MongoDB
    if %errorlevel% neq 0 (
        echo ERROR: MongoDB service not found or failed to start
        echo Please install MongoDB or start it manually
        pause
        exit /b 1
    )
) else (
    echo MongoDB is already running!
)

echo.
echo [Step 2/4] Setting up Python environment...
set PYTHONPATH=%CD%
echo PYTHONPATH set to: %PYTHONPATH%

echo.
echo [Step 3/4] Creating demo users...
python -c "import sys; sys.path.insert(0, '.'); exec(open('database/demo_user.py').read())"

echo.
echo [Step 4/4] Starting the application...
echo ================================================
echo.
echo  Application will start at: http://localhost:5000
echo.
echo  Demo Credentials:
echo  Student: student@demo.com / password123
echo  Admin:   admin@demo.com / admin123
echo.
echo ================================================
echo.
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
