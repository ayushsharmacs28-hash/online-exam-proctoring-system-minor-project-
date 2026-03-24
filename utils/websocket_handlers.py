"""
WebSocket Event Handlers
Handles all WebSocket communication for real-time proctoring
"""

from flask import request, session
from flask_socketio import emit
from database.mongo import violations
from utils.face_detection import detect_faces_in_frame
import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_connect():
    """Handle client connection"""
    logger.info(f'Client connected: {request.sid}')
    emit('status', {'message': 'Connected to proctoring system'})

def handle_disconnect():
    """Handle client disconnection"""
    logger.info(f'Client disconnected: {request.sid}')

def handle_frame(data):
    """
    Handle incoming video frames for face detection
    
    Args:
        data: Dictionary containing 'frame' and optional 'timestamp'
    """
    try:
        # Validate session
        if 'user_id' not in session or 'exam_session_id' not in session:
            emit('error', {'message': 'Invalid session'})
            return
        
        # Get frame data
        frame_data = data.get('frame', '')
        if not frame_data:
            emit('error', {'message': 'No frame data provided'})
            return
        
        # Detect faces
        face_count, status = detect_faces_in_frame(frame_data)
        
        # Check for violations
        user_id = session['user_id']
        session_id = session['exam_session_id']
        user_email = session.get('user_email', '')
        
        if face_count == 0:
            # Log face missing violation
            violations.insert_one({
                "type": "Face Missing",
                "user_id": user_id,
                "user_email": user_email,
                "session_id": session_id,
                "time": datetime.datetime.now(),
                "detected_via": "websocket"
            })
            
            emit('violation', {
                'type': 'Face Missing',
                'message': 'No face detected in camera feed',
                'face_count': face_count,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            logger.warning(f"Face missing violation - User: {user_id}, Session: {session_id}")
            
        elif face_count > 1:
            # Log multiple faces violation
            violations.insert_one({
                "type": "Multiple Faces",
                "user_id": user_id,
                "user_email": user_email,
                "session_id": session_id,
                "time": datetime.datetime.now(),
                "detected_via": "websocket"
            })
            
            emit('violation', {
                'type': 'Multiple Faces',
                'message': f'Multiple faces detected: {face_count}',
                'face_count': face_count,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            logger.warning(f"Multiple faces violation - User: {user_id}, Faces: {face_count}, Session: {session_id}")
            
        else:
            # No violation - send status update
            emit('status', {
                'message': status,
                'face_count': face_count,
                'status': 'normal',
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            logger.info(f"Normal status - User: {user_id}, Faces: {face_count}")
            
    except Exception as e:
        logger.error(f'Frame processing error: {str(e)}')
        emit('error', {'message': 'Server error during frame processing'})

def handle_heartbeat():
    """Handle client heartbeat to keep connection alive"""
    emit('heartbeat_response', {'timestamp': datetime.datetime.now().isoformat()})
