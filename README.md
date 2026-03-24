# 🎓 AI Online Exam Proctoring System

A comprehensive Python-based AI-powered online examination proctoring system that prevents cheating through real-time monitoring, face detection, and behavior analysis.


## ✨ Features

### 🔐 Authentication System
- **User Registration & Login** with encrypted passwords (bcrypt)
- **Session Management** with Flask-Session
- **Role-Based Access Control** (Student/Admin)

### 📹 Real-Time Proctoring
- **Live Webcam Monitoring** with video feed display
- **WebSocket-based Face Detection** using OpenCV
- **Tab Switch Detection** with automatic violation logging
- **Multiple Face Detection** to prevent impersonation
- **Real-time Violation Counter** with instant feedback

### 📝 Exam Management
- **Interactive MCQ Interface** with radio button selections
- **30-Minute Timer** with auto-submission
- **Automatic Grading** with instant results
- **Session Tracking** linking violations to specific exam attempts

### 📊 Admin Dashboard
- **Real-Time Statistics** (total users, exams, violations)
- **Violation Breakdown** by type
- **Exam Results Table** with scores and suspicious activity
- **Detailed Violation Logs** with timestamps
- **Auto-Refresh** every 30 seconds

### 🎯 Suspicious Activity Scoring
- **Tab Switch**: 7 points
- **Face Missing**: 5 points
- **Multiple Faces**: 10 points
- **Automatic Calculation** per session and user

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask 3.0+
- **Database**: MongoDB (Cloud-based)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Real-time Communication**: WebSocket (Socket.IO)
- **Computer Vision**: OpenCV, NumPy
- **Authentication**: bcrypt, PyJWT
- **Package Manager**: uv (modern Python package manager)

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8 or higher** installed
2. **uv** package manager installed (`pip install uv`)
3. **Webcam** for proctoring features
4. **Modern web browser** (Chrome, Firefox, Edge)
5. **MongoDB Atlas** cloud database (URI configured in `.env`)

## 📖 How to Use

### For Students

1. **Register/Login**
   - Navigate to http://localhost:5000
   - Login with demo credentials or register a new account
   - Email: `student@demo.com`, Password: `password123`

2. **Take Exam**
   - Allow webcam access when prompted (required for proctoring)
   - Read all questions carefully
   - Select your answers using radio buttons
   - Keep your face visible throughout the exam
   - Avoid switching tabs or opening other windows
   - Click "Submit Exam" when finished

3. **View Results**
   - Exam score (% correct answers)
   - Suspicious activity score
   - Violation breakdown

### For Administrators

1. **Login**
   - Email: `admin@demo.com`, Password: `admin123`

2. **Monitor Dashboard**
   - View total statistics
   - Check violation breakdown by type
   - Review recent exam results
   - Analyze detailed violation logs
   - Dashboard auto-refreshes every 30 seconds

## 📁 Project Structure

```
ONLINE EXAM PROCTOR SYSTEM/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── pyproject.toml              # uv project configuration
├── .env                       # Environment variables (MongoDB URI)
├── suspicious_score.py          # Violation scoring system
│
├── utils/                     # Modular utilities
│   ├── face_detection.py       # Face detection logic
│   ├── websocket_handlers.py    # WebSocket event handlers
│   └── data.py               # Exam questions data
│
├── database/
│   ├── mongo.py              # MongoDB connection & collections
│   └── demo_user.py          # Demo user creation script
│
├── templates/
│   ├── login.html            # Login page
│   ├── register.html         # Registration page
│   ├── exam.html             # Exam interface
│   └── dashboard.html        # Admin dashboard
│
├── static/
│   ├── style.css             # Complete stylesheet
│   ├── webcam.js             # Webcam & WebSocket client
│   └── exam.js               # Exam timer & submission
│
└── uploads/                  # User uploaded images (created automatically)
```

## 🔧 Configuration

### Environment Variables (.env)
```
MONGO_URI=mongodb+srv://your-username:your-password@cluster.mongodb.net/your-database
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### Application Settings (config.py)
- **EXAM_DURATION**: Exam time limit (default: 30 minutes)
- **VIOLATION_THRESHOLD**: Suspicious score threshold (default: 50 points)
- **FACE_DETECTION_INTERVAL**: Face check frequency (default: 5 seconds)
- **Violation Penalties**: Points for each violation type

## 🎯 Sample Exam Questions

The system includes 5 sample MCQ questions covering:
- Data Structures & Algorithms
- Programming Languages
- Web Technologies

To add more questions, edit `EXAM_QUESTIONS` list in `utils/data.py`.

## 📊 Violation Scoring System

| Violation Type | Points | Triggered When |
|---------------|--------|----------------|
| Tab Switch | 7 | User switches browser tabs or windows |
| Face Missing | 5 | No face detected in webcam |
| Multiple Faces | 10 | More than one person detected |

**Threshold**: Sessions with 50+ suspicious points are flagged for review.


## 🔒 Security Features

- ✅ Password encryption with bcrypt
- ✅ Session-based authentication
- ✅ MongoDB injection prevention
- ✅ WebSocket-based real-time monitoring
- ✅ Right-click disabled during exam
- ✅ Developer tools blocked
- ✅ Tab switch detection
- ✅ Back button prevention during exam
- ✅ Modular codebase with separation of concerns

## 🚀 Future Enhancements

- [ ] Eye tracking for attention monitoring
- [ ] Audio monitoring for suspicious sounds
- [ ] Mobile device detection
- [ ] Screenshot capture and storage
- [ ] Email notifications for violations
- [ ] PDF report generation
- [ ] Multi-language support
- [ ] Question bank management

## 📝 Demo Credentials

### Student Account
- **Email**: student@demo.com
- **Password**: password123

### Admin Account
- **Email**: admin@demo.com
- **Password**: admin123

## 👨‍💻 Author

**Akshit Garg**
- Email: akshit.garg.cs29@iilm.edu

**Shaurya Srivastava**
- Email: shaurya.srivastava.cs29@iilm.edu

**Ajay Kumar**
- Email: ajay.kumar.cs28@iilm.edu

**Nayan pandey**
- Email: nayan.pandey.cs28@iilm.edu

**Ayush Sharma**
- Email: ayush.sharma.cs28@iilm.edu


## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- Flask-SocketIO for real-time communication
- MongoDB Atlas for cloud database hosting
- uv for modern Python package management

---

**⚠️ Important Note**: This system is designed for educational purposes. For production use, additional security measures and compliance with examination regulations should be implemented.

---

Made with ❤️ for secure online examinations
