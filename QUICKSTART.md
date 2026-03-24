# 🚀 Quick Start Guide - Online Exam Proctor System

## Prerequisites Check

- ✅ Python 3.8+ installed
- ✅ uv package manager installed (`pip install uv`)
- ✅ MongoDB Atlas cloud database (URI configured in `.env`)
- ✅ Webcam for proctoring features
- ✅ Modern web browser (Chrome, Firefox, Edge)

## How to Run

### 1. Install uv Package Manager (if not already installed)

```bash
# Install uv using pip
pip install uv

# Verify installation
uv --version
```

### 2. Set Up Project Environment

```bash
# Clone or navigate to project directory
cd ONLINE-EXAM-PROCTOR-SYSTEM

# Create virtual environment with uv
uv venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
# Install all dependencies using uv
uv sync

# Or install specific packages
uv add flask flask-socketio python-socketio opencv-python numpy pymongo bcrypt pyjwt flask-session flask-cors
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URI=mongodb+srv://your-username:your-password@cluster.mongodb.net/your-database
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 5. Run the Application

```bash
# Start the Flask application with SocketIO
python app.py
```

The application will be available at: http://localhost:5000


---
## Application URLs
| Page | URL | Access |
|------|-----|--------|
| Login | <http://localhost:5000> | Public |
| Register |<http://localhost:5000/register> | Public |
| Exam | <http://localhost:5000/exam> | Students |
| Dashboard | <http://localhost:5000/dashboard> | Admins |
---
## Testing the Application
1. **Register a new student** → Creates account
2. **Login with student account** → Redirects to exam
3. **Allow webcam access** → Required for proctoring
4. **Take the exam** → Answer 5 MCQ questions
5. **Try switching tabs** → Violation detected
6. **Submit exam** → See results
7. **Login as admin** → View dashboard
8. **Check violations** → Review all activity
---

## Demo Credentials

### Student Account
- **Email**: student@demo.com
- **Password**: password123

### Admin Account
- **Email**: admin@demo.com
- **Password**: admin123

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure virtual environment is activated
2. **MongoDB Connection Error**: Check `.env` file for correct URI
3. **Webcam Not Working**: Check browser permissions and camera access
4. **WebSocket Connection Failed**: Ensure flask-socketio is installed

### Development Tips

- Use `uv sync` to keep dependencies up to date
- Check browser console for WebSocket connection status
- Monitor server logs for face detection errors
- Test with different browsers for compatibility

## Project is Ready! ✅
All features implemented:
- ✅ Authentication & Sessions
- ✅ Exam Interface with timer
- ✅ Webcam Monitoring
- ✅ Violation Detection
- ✅ Admin Dashboard
- ✅ Modern UI Design
- ✅ Complete Documentation
**Just start MongoDB and run the application!**

## Architecture Overview

```
Frontend (Browser) ←→ WebSocket ←→ Face Detection ←→ MongoDB Atlas
     ↓                              ↓
   Exam UI                    Violation Logging
     ↓                              ↓
   Results ←→ Flask Routes ←→ Admin Dashboard
```

**🎯 Ready to go! Your AI-powered exam proctoring system is now running with modern WebSocket-based face detection and cloud database storage.**
