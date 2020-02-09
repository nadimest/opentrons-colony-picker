import cv2
import numpy as np

class Camera():
    def __init__(self,source=0):
        self.cap = cv2.VideoCapture(source)

    def read(self):
        ret,img=self.cap.read()
        if ret:
            return img
        else:
            return None

    def stop(self):
        self.cap.release()

def encodePng(img):
    return cv2.imencode('.png', img)[1].tobytes()

def blankImage(width,height,color):
    img = np.full((height, width), color)
    return encodePng(img)

