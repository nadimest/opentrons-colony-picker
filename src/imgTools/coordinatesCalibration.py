#!/usr/bin/env python3

import cv2
from copy import deepcopy
import numpy as np

import locations

import argparse

SLOT=6
if SLOT == 6:
    front_left_deck = (270, 96)

front_left_screw_px=(31,578)
rear_left_screw_px=(31,70)
front_right_screw_px=(828,578)
rear_right_screw_px=(828,70)

front_left_screw_mm=[270, 96]
rear_left_screw_mm=[270, 171]
front_right_screw_mm=[387, 96]
rear_right_screw_mm=[387, 171]

SCALE=0.147

screws=[front_left_screw_px, rear_left_screw_px, front_right_screw_px, rear_right_screw_px]

colonies = locations.coloniesCache()

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        colonies.add((x,y))

img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)


def transformCoordinates(coord):
    """ See the pixelToDeck_factor_Calculation readme file for the source of these transformation formulas"""
    X_new = SCALE * (coord[0] - front_left_screw_px[0]) + front_left_screw_mm[0]
    Y_new = SCALE * (front_left_screw_px[1] - coord[1]) + front_left_screw_mm[1]

    return (X_new, Y_new)


def overlayCircles(img,circlesList):

    overlay=deepcopy(img)
    color=(0,0,255)
    radius=5
    thickness=-1
    fontScale=0.7
    fontFace=cv2.FONT_HERSHEY_PLAIN
    offset=3

    for i in range(len(circlesList)):
        point=circlesList[i]
        textPoint=(point[0]+offset,point[1]-offset)
        cv2.circle(overlay,point, radius, color,thickness)
        cv2.putText(overlay, str(i),textPoint , fontFace, fontScale, color)

    return overlay


def main():

    parser = argparse.ArgumentParser(description='Get coordinates list')
    parser.add_argument('--source',help='source image filename')
    args = parser.parse_args()

    global img
    img = cv2.imread(args.source)
    # img = overlayCircles(img, screws)

    while True:
        overlay=overlayCircles(img,colonies.getCoordinates())
        cv2.imshow("image", overlay)

        c=cv2.waitKey(10)
        if c==ord('q'):
            break

        if c==ord('s'):
            for coord in colonies.getCoordinates():
                print(transformCoordinates(coord))


if __name__ == "__main__":
    main()