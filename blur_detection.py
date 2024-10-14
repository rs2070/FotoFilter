import cv2
import os

class BlurDetector:
    def __init__(self, threshold=12.0):  #sensitive threshold
        self.threshold = threshold

    def is_blurry(self, file_path):
        image = cv2.imread(file_path)
        if image is None:
            print(f"Failed to read image at {file_path}")
            return False

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3, 3), 0) #reduce Gaussian blur for more details during edge detection
        fm = cv2.Laplacian(gray, cv2.CV_64F).var() #calculate edges using Laplacian and variance
        print(f"Variance for {file_path}: {fm}")
        return fm < self.threshold  #blurry if under threshold

def process_blurry(files):
    detector = BlurDetector()
    flagged_images = []
    for file_path in files:
        if detector.is_blurry(file_path):
            flagged_images.append(os.path.basename(file_path))
            print(f"Blur detected in {os.path.basename(file_path)}")
        else:
            print(f"Not blurry: {os.path.basename(file_path)}")
    return flagged_images