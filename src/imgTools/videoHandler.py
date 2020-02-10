import cv2
import numpy as np
from copy import deepcopy

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

def overlayCircles(img,circlesList):
    overlay=deepcopy(img)
    color=(0,255,255)
    radius=5
    fontScale=0.8
    fontFace=cv2.FONT_HERSHEY_PLAIN
    offset=(10,-10)


    for i in range(len(circlesList)):
        point=circlesList[i]
        textPoint=(point[0]+5,point[1]-5)
        cv2.circle(overlay,point, radius, color)
        cv2.putText(overlay, str(i),textPoint , fontFace, fontScale, color)

    return overlay

