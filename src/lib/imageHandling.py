#!/usr/bin/env python3

import cv2
from copy import deepcopy
import numpy as np

class ImageHandler():
    def __init__(self,img_filename, coordinates, winName="image"):
        self.img = np.zeros((512, 512, 3), np.uint8)
        self.winName=winName
        self.coordinates=coordinates
        cv2.namedWindow(self.winName)
        cv2.setMouseCallback(self.winName, self.draw_circle)
        self.img = cv2.imread(img_filename)

    def draw_circle(self,event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            self.coordinates.add((x, y))

    def overlayCircles(self,circlesList):
        self.overlay=deepcopy(self.img)
        color=(0,0,255)
        radius=5
        thickness=-1
        fontScale=0.7
        fontFace=cv2.FONT_HERSHEY_PLAIN
        offset=3
        if circlesList:
            for i in range(len(circlesList)):
                point=circlesList[i]
                textPoint=(point[0]+offset,point[1]-offset)
                cv2.circle(self.overlay,point, radius, color,thickness)
                cv2.putText(self.overlay, str(i),textPoint , fontFace, fontScale, color)

    def showImage(self,circles=None):
        self.overlayCircles(circles)
        cv2.imshow(self.winName,self.overlay)
        self.cmd=cv2.waitKey(10)

    def getPressedKey(self):
        return self.cmd

    def saveImage(self,filename):
        cv2.imwrite(filename,self.overlay)