import cv2, datetime
from database.mongo import violations

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) == 0:
        violations.insert_one({"type":"Face Missing","time":datetime.datetime.now()})

    if len(faces) > 1:
        violations.insert_one({"type":"Multiple Faces","time":datetime.datetime.now()})

    cv2.imshow("AI Proctor", frame)
    if cv2.waitKey(1) == 27:
        break

cam.release()
cv2.destroyAllWindows()
