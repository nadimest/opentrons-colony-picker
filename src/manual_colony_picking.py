#!/usr/bin/env python3

import subprocess

from lib.coordinatesManagement import CoordinatesManager
from lib.imageHandling import ImageHandler

coordinates=CoordinatesManager(calibration_filename="calib/calibration.json")

def main():

    fetchImage=subprocess.run("./server_scripts/fetchPicturefromServer.sh")

    image=ImageHandler("data/colonies.jpg",coordinates)

    while True:
        image.showImage(circles=coordinates.getPoints())
        c=image.getPressedKey()

        if c==ord('q'):
            break

        if c==ord('s'):
            coordinates.writeCoordinatesFile(filename="data/coordinates.json")

            image.saveImage("data/colonies_processed.jpg")

            for coord in coordinates.coord_transformed:
                print(coord)

            fetchImage=subprocess.run("./server_scripts/pushColoniesToServer.sh")
            break

if __name__ == "__main__":
    main()