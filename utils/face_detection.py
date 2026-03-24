"""
Face Detection Module
Handles all face detection functionality using OpenCV
"""

import cv2
import numpy as np
import base64
from typing import Tuple, Optional

class FaceDetector:
    """Face detection class using OpenCV Haar cascades"""
    
    def __init__(self):
        """Initialize face detector with Haar cascade"""
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
        if self.face_cascade.empty():
            raise RuntimeError("Failed to load face cascade classifier")
    
    def decode_base64_frame(self, frame_data: str) -> Optional[np.ndarray]:
        """
        Decode base64 encoded frame to numpy array
        
        Args:
            frame_data: Base64 encoded image string
            
        Returns:
            Decoded image as numpy array or None if failed
        """
        try:
            # Remove data URL prefix if present
            if ',' in frame_data:
                frame_data = frame_data.split(',')[1]
            
            # Decode base64
            image_data = base64.b64decode(frame_data)
            nparr = np.frombuffer(image_data, np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            return frame
        except Exception as e:
            print(f"Frame decoding error: {e}")
            return None
    
    def detect_faces(self, frame: np.ndarray) -> Tuple[int, list]:
        """
        Detect faces in a frame
        
        Args:
            frame: Input image as numpy array
            
        Returns:
            Tuple of (face_count, face_rectangles)
        """
        try:
            if frame is None:
                return 0, []
            
            # Convert to grayscale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray, 
                scaleFactor=1.3, 
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            return len(faces), faces.tolist()
            
        except Exception as e:
            print(f"Face detection error: {e}")
            return 0, []
    
    def analyze_frame(self, frame_data: str) -> Tuple[int, str, Optional[list]]:
        """
        Complete frame analysis: decode and detect faces
        
        Args:
            frame_data: Base64 encoded frame
            
        Returns:
            Tuple of (face_count, status_message, face_rectangles)
        """
        # Decode frame
        frame = self.decode_base64_frame(frame_data)
        if frame is None:
            return 0, "Invalid frame", []
        
        # Detect faces
        face_count, faces = self.detect_faces(frame)
        
        # Determine status
        if face_count == 0:
            status = "No face detected"
        elif face_count == 1:
            status = "Face detected"
        else:
            status = f"Multiple faces detected ({face_count})"
        
        return face_count, status, faces

# Global face detector instance
face_detector = FaceDetector()

def detect_faces_in_frame(frame_data: str) -> Tuple[int, str]:
    """
    Convenience function to detect faces in base64 frame
    
    Args:
        frame_data: Base64 encoded image string
        
    Returns:
        Tuple of (face_count, status_message)
    """
    face_count, status, _ = face_detector.analyze_frame(frame_data)
    return face_count, status
