#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import cv2
from copy import deepcopy
import numpy as np

SOURCE="colonies_test.jpg"
BACKGROUND_SOURCE="emptyplate.jpg"

def trackbarCallback(val):
    return val

cv2.namedWindow("win")
cv2.createTrackbar("th", "win" , 130, 255, trackbarCallback)


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

def getCircleROI(img,center=(0,0),radius=100):
    
    mask=np.zeros_like(img)
    cv2.circle(mask, center,radius, (255,255,255),-1)  #white filled circle
    
    img=cv2.bitwise_and(img, mask)
    
    return img

def getCiclesfromContours(img):
    minContourPoints=6
    contours = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
    circlesArray = np.empty([1,3],dtype=np.int)

    for c in contours:
        if len(c) > minContourPoints:
            (x,y),r = cv2.minEnclosingCircle(c)   
            center = (int(x),int(y))
            r = int(r)
            
            circlesArray=np.append(circlesArray,[[int(x),int(y),int(r)]],axis=0)
    
    return circlesArray

def filterCirclesByRadius(circlesArray,minRadius=2,maxRadius=4):
    circlesArray=circlesArray[(circlesArray[:,2]>=minRadius) & (circlesArray[:,2]<=maxRadius)]
    return circlesArray

def drawCirclesFromArray(img, circlesArray):
    
    cImage=deepcopy(img)
    
    for circle in circlesArray:
            
        x=circle[0]
        y=circle[1]
        r=circle[2]
        if r>3:
            circleColor=(255,255,0)
        else:
            circleColor=(0,255,0)
            r=r+1
        
        cv2.circle(cImage,(x,y),r,circleColor,1)
        # ~ cv2.circle(cImage,center,r+2,(0,0,255),1)
        # ~ print(center,r,cv2.contourArea(c))
        # ~ cv2.imshow("win",cImage)
        # ~ cv2.waitKey()

    return cImage
    
"""Circle detection from contours
1.- Does the contour have more than 6 points?  Less than 6 points it is probably not a circle
2.- Convert contour into circle, by finding the center and radius of an circle that circunscribes the contour
3.- Filter circles with a radius outside the range of interest
4.- Keep isolated circle. An isolated circle means that there is no artifact (circle or non circle) in an extended radius 
    of a few pixels.   (Artifact detection in the binary image and linked to the intensity threshold filter)
"""

def circlesDetectCountours(img,minRadius=2,maxRadius=3):
    

    circlesArray=getCiclesfromContours(img)
    print("Total number circles detected: ", circlesArray.shape)
    smallCirclesArray=filterCirclesByRadius(circlesArray,minRadius=2,maxRadius=3) 
    print("Circles with radius between 2 and 3: ",smallCirclesArray.shape)
    blobsArray=filterCirclesByRadius(circlesArray,minRadius=4,maxRadius=15) 
    print("Blobs detected as circles  with radius between 4 and 15: ",blobsArray.shape)
    
    return smallCirclesArray
    
    # ~ input()
    
    
   
                
                # ~ if center not in array:
                    # ~ array+=[center]
                # ~ array=np.append(array,[[int(x),int(y)]],axis=0) 
                # ~ if newPoint not in array:
                    # ~ array+=[[int(x),int(y)]]
    # ~ print(len(array),array)
    
    # ~ print(lineContours) 
    # ~ return cImage

def main():
    
    c=0
    toggle=3
    

    img=cv2.imread(SOURCE)
    bg=cv2.imread(BACKGROUND_SOURCE)
    diff=getForeground(img,bg)

    diff=getCircleROI(diff,center= (399, 305),radius=235)
    
    while True:
        
        img2=preprocessing(diff)
        circlesArray= circlesDetectCountours(img2,minRadius=2,maxRadius=20)
        img_circles=drawCirclesFromArray(img,circlesArray)
        
        if c==ord('1') or toggle==1:
            toggle=1
            result=img2
        
        if c==ord('2') or toggle==2:
            toggle=2
            result=img_circles
        
        if c==ord('3') or toggle==3:
            toggle=3
            result=img
        
        if c==ord('4') or toggle==4:
            toggle=4
            result=bg
            
        cv2.imshow("win",result)
        c=cv2.waitKey(1)
        
        if c==ord('q'):
            break
        
        
if __name__ == "__main__":
    main()
