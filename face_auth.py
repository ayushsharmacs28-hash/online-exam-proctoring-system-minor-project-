import face_recognition
import cv2

def verify_face(registered_path):
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        print("Camera not accessible")
        return False

    ret, frame = cam.read()
    cam.release()

    if not ret:
        print("Failed to capture image")
        return False

    cv2.imwrite("live.jpg", frame)

    # Load images
    reg_img = face_recognition.load_image_file(registered_path)
    live_img = face_recognition.load_image_file("live.jpg")

    # Get encodings safely
    reg_encodings = face_recognition.face_encodings(reg_img)
    live_encodings = face_recognition.face_encodings(live_img)

    if len(reg_encodings) == 0:
        print("No face found in registered image")
        return False

    if len(live_encodings) == 0:
        print("No face found in live image")
        return False

    reg_enc = reg_encodings[0]
    live_enc = live_encodings[0]

    # Compare faces
    result = face_recognition.compare_faces(
        [reg_enc], live_enc, tolerance=0.5
    )

    return result[0]
