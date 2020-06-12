#!/usr/bin/env python3

import cv2
from copy import deepcopy
import numpy as np
import json

import lib.locations as locations

import argparse


calibration_filename = "calib/calibration.json"

with open(calibration_filename) as calibration_file:
    calibration=json.load(calibration_file)

scale=calibration['SCALE']
chosenSlot=str(calibration['CHOSEN_SLOT'])
calibration_points=calibration['SLOTS'][chosenSlot]

def transformCoordinates(coord):
    """ See the pixelToDeck_factor_Calculation readme file for the source of these transformation formulas"""
    X_new = scale * (coord[0] - calibration_points['front_left_screw_px'][0]) + calibration_points['front_left_screw_mm'][0]
    Y_new = scale * (calibration_points['front_left_screw_px'][1] - coord[1]) + calibration_points['front_left_screw_mm'][1]

    return (X_new, Y_new)

def writeCoordinatesFile(coordinates,filename="coordinates.json"):

    coord= {'coordinates': coordinates}

    with open(filename,'w') as coordinates_file:
        json.dump(coord,coordinates_file)


from lib.coordinatesManagement import CoordinatesManager

coordinates=CoordinatesManager(calibration_filename="calib/calibration.json")

colonies = locations.coloniesCache()

def draw_circle(event,x,y,flags,param):
    global mouseX,mouseY
    if event == cv2.EVENT_LBUTTONDOWN:
        colonies.add((x,y))
        coordinates.add((x,y))

img = np.zeros((512,512,3), np.uint8)
cv2.namedWindow('image')
cv2.setMouseCallback('image', draw_circle)

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

    while True:
        # overlay=overlayCircles(img,colonies.getCoordinates())
        overlay=overlayCircles(img,coordinates.getPoints())
        cv2.imshow("image", overlay)

        c=cv2.waitKey(10)
        if c==ord('q'):
            break

        if c==ord('s'):
            coordinates.writeCoordinatesFile()

            # coord_transformed = [transformCoordinates(item) for item in colonies.getCoordinates()]
            # writeCoordinatesFile(coord_transformed)
            cv2.imwrite("colonies_processed.jpg",overlay)
            for coord in coord_transformed:
                print(coord)

if __name__ == "__main__":
    main()