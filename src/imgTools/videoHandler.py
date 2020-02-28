import cv2
import numpy as np
from copy import deepcopy

offsetY=240
offsetX=180
width=800
height=600

class Camera():
    def __init__(self,source=0,RotateFlag=False):
        self.cap = cv2.VideoCapture(source)
        self.rotateFlag=RotateFlag
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT,960)
        self.cap.set(cv2.CAP_PROP_FPS, 15)

    def read(self):
        ret,img=self.cap.read()
        img=img[offsetY:offsetY+height,offsetX:+offsetX+width,:]
        if self.rotateFlag:
            img=cv2.rotate(img,rotateCode=1)

        if ret:
            return img
        else:
            return None
    def takePicture(self,filename):
        img=self.read()
        cv2.imwrite(filename,img)
        return 

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
    radius=4
    fontScale=0.5
    fontFace=cv2.FONT_HERSHEY_PLAIN
    offset=3


    for i in range(len(circlesList)):
        point=circlesList[i]
        textPoint=(point[0]+offset,point[1]-offset)
        cv2.circle(overlay,point, radius, color)
        cv2.putText(overlay, str(i),textPoint , fontFace, fontScale, color)

    return overlay

