# 🎓 AI Online Exam Proctoring System

A comprehensive Python-based AI-powered online examination proctoring system that prevents cheating through real-time monitoring, face detection, and behavior analysis.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-4.0+-brightgreen.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 🔐 Authentication System
- **User Registration & Login** with encrypted passwords (bcrypt)
- **Session Management** with Flask-Session
- **Role-Based Access Control** (Student/Admin)

### 📹 Real-Time Proctoring
- **Live Webcam Monitoring** with video feed display
- **Face Detection** using OpenCV and face-recognition library
- **Tab Switch Detection** with automatic violation logging
- **Multiple Face Detection** to prevent impersonation
- **Violation Counter** with real-time updates

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

- **Backend**: Python 3.8+, Flask 2.0+
- **Database**: MongoDB 4.0+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Computer Vision**: OpenCV, face-recognition
- **Authentication**: bcrypt, PyJWT
- **Session Management**: Flask-Session

## 📋 Prerequisites

Before running the application, ensure you have:

1. **Python 3.8 or higher** installed
2. **MongoDB** installed and running
3. **Webcam** for proctoring features
4. **Modern web browser** (Chrome, Firefox, Edge)

## 🚀 Installation & Setup

### Step 1: Clone or Navigate to Project Directory

```bash
cd "C:\Users\AKSHIT GARG\OneDrive\Desktop\ONLINE EXAM PROCTOR SYSTEM"
```

### Step 2: Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installing `face-recognition` may take a few minutes as it includes dlib and other dependencies.

### Step 3: Start MongoDB

**Windows:**
```bash
# Start MongoDB service
net start MongoDB

# OR run mongod directly
mongod
```

**Linux/Mac:**
```bash
sudo systemctl start mongod
```

### Step 4: Create Demo Users

```bash
python database/demo_user.py
```

This creates:
- **Student Account**: `student@demo.com` / `password123`
- **Admin Account**: `admin@demo.com` / `admin123`

### Step 5: Run the Application

```bash
python app.py
```

The application will start on **http://localhost:5000**

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
├── face_auth.py               # Face verification module
├── proctor.py                 # Standalone face detection script
├── suspicious_score.py        # Violation scoring system
├── requirements.txt           # Python dependencies
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
│   ├── webcam.js             # Webcam & violation monitoring
│   └── exam.js               # Exam timer & submission
│
└── uploads/                  # User uploaded images (created automatically)
```

## 🔧 Configuration

Edit `config.py` to customize:

- **EXAM_DURATION**: Exam time limit (default: 30 minutes)
- **VIOLATION_THRESHOLD**: Suspicious score threshold (default: 50 points)
- **FACE_DETECTION_INTERVAL**: Face check frequency (default: 5 seconds)
- **Violation Penalties**: Points for each violation type

## 🎯 Sample Exam Questions

The system includes 5 sample MCQ questions covering:
- Data Structures & Algorithms
- Programming Languages
- Web Technologies

To add more questions, edit the `EXAM_QUESTIONS` list in `app.py`.

## 📊 Violation Scoring System

| Violation Type | Points | Triggered When |
|---------------|--------|----------------|
| Tab Switch | 7 | User switches browser tabs or windows |
| Face Missing | 5 | No face detected in webcam |
| Multiple Faces | 10 | More than one person detected |

**Threshold**: Sessions with 50+ suspicious points are flagged for review.

## 🐛 Troubleshooting

### MongoDB Connection Failed
- **Windows**: Start MongoDB service with `net start MongoDB`
- **Linux/Mac**: Run `sudo systemctl start mongod`
- Check if MongoDB is running on port 27017

### Webcam Not Working
- Grant camera permissions to your browser
- Check if antivirus/firewall is blocking camera access
- Ensure no other application is using the webcam

### Face Recognition Installation Issues
- On Windows: Install Visual C++ Build Tools
- On Mac: Install cmake with `brew install cmake`
- Use Python 3.8-3.10 for best compatibility

### Port Already in Use
- Change the port in `app.py`: `app.run(debug=True, port=5001)`

## 🔒 Security Features

- ✅ Password encryption with bcrypt
- ✅ Session-based authentication
- ✅ SQL injection prevention (MongoDB)
- ✅ Right-click disabled during exam
- ✅ Developer tools blocked
- ✅ Tab switch detection
- ✅ Back button prevention during exam

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

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- face-recognition library by Adam Geitgey
- Flask framework for web development
- MongoDB for flexible data storage

---

**⚠️ Important Note**: This system is designed for educational purposes. For production use, additional security measures and compliance with examination regulations should be implemented.

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review MongoDB and Python logs
3. Ensure all dependencies are installed correctly

---

Made with ❤️ for secure online examinations
