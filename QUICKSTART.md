# 🚀 Quick Start Guide - Online Exam Proctor System

## Prerequisites Check
- ✅ Python 3.8+ installed
- ⚠️ MongoDB installed and running
- ✅ Dependencies installed (`flask-session`, `pyjwt`, etc.)

## How to Run

### Option 1: Automated Script (Easiest)

**Windows:**
```bash
run.bat
```

**Linux/Mac:**
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Steps

1. **Start MongoDB**
   ```bash
   # Check if MongoDB is running
   # Windows: Services panel or 'sc query MongoDB'
   # Linux/Mac: 'systemctl status mongod'
   
   # Start MongoDB
   net start MongoDB  # Windows
   sudo systemctl start mongod  # Linux/Mac
   ```

2. **Open Terminal in Project Directory**
   ```bash
   cd "c:\Users\AKSHIT GARG\OneDrive\Desktop\ONLINE EXAM PROCTOR SYSTEM"
   ```

3. **Run Application**
   ```bash
   python app.py
   ```

4. **Open Browser**
   ```
   http://localhost:5000
   ```

---

## Demo Login Credentials

### Student Account
```
Email: student@demo.com
Password: password123
```

### Admin Account
```
Email: admin@demo.com
Password: admin123
```

---

## Application URLs

| Page | URL | Access |
|------|-----|--------|
| Login | http://localhost:5000 | Public |
| Register |http://localhost:5000/register | Public |
| Exam | http://localhost:5000/exam | Students |
| Dashboard | http://localhost:5000/dashboard | Admins |

---

## Common Issues

### MongoDB Not Running
```
Error: MongoDB connection failed
Solution: Run 'net start MongoDB' (Windows) or 'sudo systemctl start mongod' (Linux/Mac)
```

### Port Already in Use
```
Error: Address already in use
Solution: Change port in app.py line 296: app.run(debug=True, port=5001)
```

### Module Not Found
```
Error: ModuleNotFoundError: No module named 'flask_session'
Solution: pip install -r requirements.txt
```

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
