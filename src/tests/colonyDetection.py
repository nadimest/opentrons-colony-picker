#!/usr/bin/env python
# -*- coding: utf-8 -*-


import cv2
from copy import deepcopy
import numpy as np

SOURCE="picture.jpg"
BACKGROUND_SOURCE="emptyplate.jpg"

def trackbarCallback(val):
    return val

cv2.namedWindow("win")
cv2.createTrackbar("th", "win" , 149, 255, trackbarCallback)


img=cv2.imread(SOURCE)
bg=cv2.imread(BACKGROUND_SOURCE)


displayImg=img

def getForeground(img,bg):
    
    diff= cv2.subtract(img,bg)
    
    return diff

def preprocessing(img):
    
    gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    kernelSize=(3,3)
    # ~ gray=cv2.blur(gray,kernelSize)
    # ~ gray=cv2.medianBlur(gray, 5)
    # ~ clahe = cv2.createCLAHE(clipLimit=14.0, tileGridSize=(8,8))
    # ~ gray = clahe.apply(gray)
    ret,bit = cv2.threshold(gray,cv2.getTrackbarPos("th", "win"),255,cv2.THRESH_BINARY)
    
    th1=20
    th2=200
    # ~ edges=cv2.Canny(gray,th1,th2)
    
    
    bit = cv2.erode(bit, kernelSize, iterations=2)
    bit = cv2.dilate(bit, kernelSize, iterations=2)

    # ~ closing = cv2.morphologyEx(bit, cv2.MORPH_OPEN, kernelSize)
    
    return bit


def circlesDetect(img):
    
    cImage=deepcopy(img)
    
    img2=preprocessing(img)
    
    circles = cv2.HoughCircles(img2,cv2.HOUGH_GRADIENT,0.1,5,
                                param1=2100,param2=10,minRadius=1,maxRadius=10)
    
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(cImage,(i[0],i[1]),i[2],(0,255,0),1)

    
    return cImage

def circlesDetectCountours(img):
    
    
    cImage=deepcopy(img)
        
    img=preprocessing(img)
    


    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]


    array = np.empty([1,2])

    for c in contours:
        (x,y),r = cv2.minEnclosingCircle(c)
        center = (int(x),int(y))
        r = int(r)
        if r >= 2 and r<=4:
            cv2.circle(cImage,center,r,(0,255,0),2)
            newPoint=[int(x),int(y)]
            array=np.append(array,[[int(x),int(y)]],axis=0) 
            
    
    print(array.shape)
    return cImage

L_BUTTON_DOWN=False
R_BUTTON_DOWN=False

def click_and_change(event, x, y, flags, param):
    
    global L_BUTTON_DOWN, R_BUTTON_DOWN
    
    if event == cv2.EVENT_LBUTTONDOWN:
        L_BUTTON_DOWN=True
        
    elif event == cv2.EVENT_LBUTTONUP:
        L_BUTTON_DOWN=False
        
    if event == cv2.EVENT_RBUTTONDOWN:
        R_BUTTON_DOWN=True
        
    elif event == cv2.EVENT_RBUTTONUP:
        R_BUTTON_DOWN=False
        
cv2.setMouseCallback("win", click_and_change)


def main():
    
    c=0
    toggle=3
    

    while True:
        
        diff=getForeground(img,bg)
    
        img2=preprocessing(diff)

        img_circles= circlesDetectCountours(diff)


        if c==ord('1') or toggle==1:
            toggle=1
            result=img2
        
        if c==ord('2') or toggle==2:
            toggle=2
            result=img_circles
        
        if c==ord('3') or toggle==3:
            toggle=3
            result=img
        
    
        cv2.imshow("win",result)
        c=cv2.waitKey(1)
        
        if c==ord('q'):
            break
        
        
if __name__ == "__main__":
    main()
