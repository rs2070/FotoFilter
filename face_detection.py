import cv2
import os

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        if self.face_cascade.empty() or self.eye_cascade.empty():
            print("Failed to load cascades.")
            raise Exception("Failed to load cascades. Check the path to the XML files.")

    def detect_faces_and_eyes(self, file_path):
        image = cv2.imread(file_path)
        if image is None:
            print(f"Failed to read image at {file_path}")
            return False, None
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(50, 50))
        face_detected = False
        
        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            eyes = self.eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20))
            
            if len(eyes) >= 1: #allow detect with one eye visible
                face_detected = True
                cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)  #face rectangle

        if face_detected:
            processed_file_path = os.path.join('processed_images', os.path.basename(file_path))
            cv2.imwrite(processed_file_path, image)
            print(f"Faces detected in {file_path}")
            return True, processed_file_path
        
        print(f"No face detected in {file_path}")
        return False, None