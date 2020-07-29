#!/usr/bin/env python3

import cv2, time
from copy import deepcopy
import numpy as np

DISTANCE_LIMIT= 5
RADIUS=3

class ImageHandler():
    def __init__(self,img_filename, coordinates, winName="image"):
        self.img = np.zeros((512, 512, 3), np.uint8)
        self.winName=winName
        self.coordinates=coordinates
        cv2.namedWindow(self.winName)
        time.sleep(0.1)
        cv2.setMouseCallback(self.winName, self.draw_circle)
        self.img = cv2.imread(img_filename)

    def draw_circle(self,event, x, y, flags, param):
        global mouseX, mouseY
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.coordinates.removeNearPoint((x,y),DISTANCE_LIMIT):
                self.coordinates.add((x, y))

    def overlayCircles(self,circlesList):
        self.overlay=deepcopy(self.img)
        color=(0,0,255)
        thickness=1
        fontScale=0.5
        textcolor = (0, 255, 255)
        fontFace=cv2.FONT_HERSHEY_PLAIN
        offset=3
        if circlesList:
            for i in range(len(circlesList)):
                point=circlesList[i]
                textPoint=(point[0]+offset,point[1]-offset)
                cv2.circle(self.overlay,point, RADIUS, color,thickness)
                cv2.putText(self.overlay, str(i),textPoint , fontFace, fontScale, textcolor)

    def showImage(self,circles=None):
        self.overlayCircles(circles)
        cv2.imshow(self.winName,self.overlay)
        self.cmd=cv2.waitKey(10)

    def getPressedKey(self):
        return self.cmd

    def saveImage(self,filename):
        cv2.imwrite(filename,self.overlay)

    def quit(self):
        cv2.destroyAllWindows()