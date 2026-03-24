from flask import Flask, render_template, request, jsonify, redirect, session, flash, url_for
from flask_socketio import SocketIO, emit

import base64
import io
import cv2
import numpy as np
from database.mongo import users, violations, exam_sessions, exam_results
from database.demo_user import create_demo_users
from suspicious_score import get_session_score, get_violation_breakdown
from utils.data import EXAM_QUESTIONS
import bcrypt
import datetime
from functools import wraps
from bson import ObjectId
import os

app = Flask(__name__)
app.config.from_object('config.Config')
socketio = SocketIO(app)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# Admin decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'error')
            return redirect(url_for('login'))
        user = users.find_one({"_id": ObjectId(session['user_id'])})
        if not user or user.get('role') != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('exam'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def root():
    if 'user_id' in session:
        return redirect(url_for('exam'))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            name = request.form.get("name", "").strip()
            
            # Validation
            if not email or not password or not name:
                flash("All fields are required", "error")
                return redirect(url_for('register'))
            
            if len(password) < 6:
                flash("Password must be at least 6 characters", "error")
                return redirect(url_for('register'))
            
            # Check if user already exists
            if users.find_one({"email": email}):
                flash("Email already registered", "error")
                return redirect(url_for('register'))
            
            # Hash password
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            
            # Insert user
            users.insert_one({
                "email": email,
                "password": hashed,
                "name": name,
                "role": "student",
                "created_at": datetime.datetime.now()
            })
            
            flash("Registration successful! Please login.", "success")
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f"Registration failed: {str(e)}", "error")
            return redirect(url_for('register'))
    
    return render_template("register.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        try:
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            
            if not email or not password:
                flash("Email and password are required", "error")
                return redirect(url_for('login'))
            
            user = users.find_one({"email": email})
            
            if user and bcrypt.checkpw(password.encode(), user["password"]):
                session['user_id'] = str(user['_id'])
                session['user_email'] = user['email']
                session['user_name'] = user.get('name', 'Student')
                session['user_role'] = user.get('role', 'student')
                
                # Redirect based on role
                if user.get('role') == 'admin':
                    return redirect(url_for('dashboard'))
                return redirect(url_for('exam'))
            
            flash("Invalid email or password", "error")
            return redirect(url_for('login'))
            
        except Exception as e:
            flash(f"Login failed: {str(e)}", "error")
            return redirect(url_for('login'))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully", "success")
    return redirect(url_for('login'))

@app.route("/exam")
@login_required
def exam():
    # Create new exam session
    session_data = {
        "user_id": session['user_id'],
        "user_email": session['user_email'],
        "start_time": datetime.datetime.now(),
        "status": "in_progress"
    }
    result = exam_sessions.insert_one(session_data)
    session['exam_session_id'] = str(result.inserted_id)
    
    return render_template("exam.html", 
                          questions=EXAM_QUESTIONS,
                          user_name=session.get('user_name'))

@app.post("/violation")
@login_required
def violation():
    try:
        data = request.json
        violation_data = {
            "type": data["type"],
            "user_id": session['user_id'],
            "user_email": session['user_email'],
            "session_id": session.get('exam_session_id'),
            "time": datetime.datetime.now()
        }
        violations.insert_one(violation_data)
        
        # Get current score for this session
        score = get_session_score(session.get('exam_session_id'))
        
        return jsonify({
            "status": "logged",
            "current_score": score
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.post("/submit_exam")
@login_required
def submit_exam():
    try:
        data = request.json
        answers = data.get("answers", {})
        
        # Calculate score
        correct_count = 0
        for question in EXAM_QUESTIONS:
            qid = str(question["id"])
            if qid in answers and int(answers[qid]) == question["correct"]:
                correct_count += 1
        
        exam_score = (correct_count / len(EXAM_QUESTIONS)) * 100
        
        # Get suspicious score
        session_id = session.get('exam_session_id')
        suspicious_score = get_session_score(session_id)
        violation_breakdown = get_violation_breakdown(session_id=session_id)
        
        # Save results
        result_data = {
            "user_id": session['user_id'],
            "user_email": session['user_email'],
            "session_id": session_id,
            "exam_score": exam_score,
            "correct_answers": correct_count,
            "total_questions": len(EXAM_QUESTIONS),
            "suspicious_score": suspicious_score,
            "violations": violation_breakdown,
            "submitted_at": datetime.datetime.now()
        }
        exam_results.insert_one(result_data)
        
        # Update session status
        exam_sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {
                "status": "completed",
                "end_time": datetime.datetime.now()
            }}
        )
        
        return jsonify({
            "status": "success",
            "exam_score": exam_score,
            "suspicious_score": suspicious_score,
            "violations": violation_breakdown
        }), 200
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/dashboard")
@admin_required
def dashboard():
    # Get all violations with user info
    all_violations = list(violations.find().sort("time", -1).limit(100))
    
    # Get statistics
    total_violations = violations.count_documents({})
    
    # Violations by type
    violation_types = {}
    for v in violations.find():
        vtype = v.get("type", "Unknown")
        violation_types[vtype] = violation_types.get(vtype, 0) + 1
    
    # Recent exam results
    recent_results = list(exam_results.find().sort("submitted_at", -1).limit(10))
    
    stats = {
        "total_violations": total_violations,
        "violation_types": violation_types,
        "total_exams": exam_results.count_documents({}),
        "total_users": users.count_documents({})
    }
    
    return render_template("dashboard.html", 
                          violations=all_violations,
                          stats=stats,
                          recent_results=recent_results)

@app.get("/api/get_questions")
@login_required
def get_questions():
    return jsonify({"questions": EXAM_QUESTIONS})

# Face detection helper function
def detect_faces_in_frame(frame_data):
    """Detect faces in base64 encoded frame"""
    try:
        # Decode base64 image
        image_data = base64.b64decode(frame_data.split(',')[1])
        nparr = np.frombuffer(image_data, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return 0, "Invalid frame"
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Load face cascade
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        
        # Detect faces
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        
        return len(faces), None
        
    except Exception as e:
        return 0, str(e)

# WebSocket event handlers
@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')
    emit('status', {'message': 'Connected to proctoring system'})

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

@socketio.on('frame')
def handle_frame(data):
    """Process video frame for face detection"""
    try:
        # Validate session
        if 'user_id' not in session or 'exam_session_id' not in session:
            emit('error', {'message': 'Invalid session'})
            return
        
        # Detect faces
        face_count, error = detect_faces_in_frame(data.get('frame', ''))
        
        if error:
            emit('error', {'message': f'Frame processing error: {error}'})
            return
        
        # Check for violations
        user_id = session['user_id']
        session_id = session['exam_session_id']
        
        if face_count == 0:
            # Log face missing violation
            violations.insert_one({
                "type": "Face Missing",
                "user_id": user_id,
                "user_email": session.get('user_email', ''),
                "session_id": session_id,
                "time": datetime.datetime.now(),
                "detected_via": "websocket"
            })
            emit('violation', {
                'type': 'Face Missing',
                'message': 'No face detected in camera feed',
                'face_count': face_count
            })
            
        elif face_count > 1:
            # Log multiple faces violation
            violations.insert_one({
                "type": "Multiple Faces",
                "user_id": user_id,
                "user_email": session.get('user_email', ''),
                "session_id": session_id,
                "time": datetime.datetime.now(),
                "detected_via": "websocket"
            })
            emit('violation', {
                'type': 'Multiple Faces',
                'message': f'Multiple faces detected: {face_count}',
                'face_count': face_count
            })
        else:
            # No violation - send status update
            emit('status', {
                'message': 'Face detected',
                'face_count': face_count,
                'status': 'normal'
            })
            
    except Exception as e:
        app.logger.error(f'Frame processing error: {str(e)}')
        emit('error', {'message': 'Server error during frame processing'})

if __name__ == "__main__":
    # Ensure upload folder exists
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    
    create_demo_users()
    
    print("\n" + "="*50)
    print("*** Online Exam Proctor System ***")
    print("="*50)
    print(f"Server running at: http://localhost:5000")
    print(f"Demo Login: student@demo.com / password123")
    print(f"Admin Login: admin@demo.com / admin123")
    print("="*50 + "\n")
    # create_demo_users()
    
    socketio.run(app, debug=True, port=5000)
