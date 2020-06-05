#!/usr/bin/env python3

import cv2
from copy import deepcopy
import numpy as np

from .calib import locations

import argparse

SLOT=6
if SLOT == 6:
    front_left_deck = (270, 96)

front_left_screw=(31,578)
rear_left_screw=(31,70)
front_right_screw=(828,578)
rear_right_screw=(828,70)

colonies = locations.coloniesCache()
circlesList=[front_left_screw, rear_left_screw, front_right_screw, rear_right_screw]

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDBLCLK:

        cv2.circle(img,(x,y),100,(255,0,0),-1)
        mouseX,mouseY = x,y

def overlayCircles(img,circlesList):
    overlay=deepcopy(img)
    color=(0,0,255)
    radius=20
    fontScale=0.5
    fontFace=cv2.FONT_HERSHEY_PLAIN
    offset=3

    for i in range(len(circlesList)):
        point=circlesList[i]

        textPoint=(point[0]+offset,point[1]-offset)
        cv2.circle(overlay,point, radius, color)
        cv2.putText(overlay, str(i),textPoint , fontFace, fontScale, color)

    return overlay


def main():

    parser = argparse.ArgumentParser(description='Get coordinates list')
    parser.add_argument('--source',help='source image filename')

    args = parser.parse_args()

    colonies_img = cv2.imread(args.source)


    overlay = overlayCircles(colonies_img, circlesList)

    cv2.imshow("win", overlay)
    cv2.waitKey()

if __name__ == "__main__":
    main()