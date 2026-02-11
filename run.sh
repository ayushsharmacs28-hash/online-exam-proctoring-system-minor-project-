#!/bin/bash

echo "================================================"
echo " Online Exam Proctor System - Setup and Run"
echo "================================================"
echo

echo "[Step 1/4] Checking MongoDB status..."
if systemctl is-active --quiet mongod; then
    echo "✓ MongoDB is running!"
else
    echo "MongoDB is not running. Attempting to start..."
    sudo systemctl start mongod
    if [ $? -eq 0 ]; then
        echo "✓ MongoDB started successfully!"
    else
        echo "✗ ERROR: Failed to start MongoDB"
        echo "Please start MongoDB manually: sudo systemctl start mongod"
        exit 1
    fi
fi

echo
echo "[Step 2/4] Setting up Python environment..."
export PYTHONPATH=$(pwd)
echo "PYTHONPATH set to: $PYTHONPATH"

echo
echo "[Step 3/4] Creating demo users..."
python3 -c "import sys; sys.path.insert(0, '.'); exec(open('database/demo_user.py').read())"

echo
echo "[Step 4/4] Starting the application..."
echo "================================================"
echo
echo "  Application will start at: http://localhost:5000"
echo
echo "  Demo Credentials:"
echo "  Student: student@demo.com / password123"
echo "  Admin:   admin@demo.com / admin123"
echo
echo "================================================"
echo
echo "Press Ctrl+C to stop the server"
echo

python3 app.py
