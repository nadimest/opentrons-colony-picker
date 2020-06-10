#!/usr/bin/env python3

from lib.coordinatesCalibration import *
import subprocess

def main():

    fetchImage=subprocess.run("./server_scripts/fetchPicturefromServer.sh")

    global img
    img = cv2.imread("data/colonies.jpg")

    while True:
        overlay=overlayCircles(img,colonies.getCoordinates())
        cv2.imshow("image", overlay)

        c=cv2.waitKey(10)
        if c==ord('q'):
            break

        if c==ord('s'):
            coord_transformed = [transformCoordinates(item) for item in colonies.getCoordinates()]
            writeCoordinatesFile(coord_transformed,filename="data/coordinates.json")
            cv2.imwrite("data/colonies_processed.jpg",overlay)

            for coord in coord_transformed:
                print(coord)

            fetchImage=subprocess.run("./server_scripts/pushColoniesToServer.sh")
            break

if __name__ == "__main__":
    main()