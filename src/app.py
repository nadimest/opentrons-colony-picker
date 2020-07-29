#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  app.py

import requests,json

from lib.imageHandling import ImageHandler
from lib.coordinatesManagement import CoordinatesManager
coordinates=CoordinatesManager(calibration_filename="calib/calibration.json")

def imageProcessing(img_filename):
	global coordinates

	img_window = ImageHandler(img_filename,coordinates)
	while True:
		img_window.showImage(circles=coordinates.getPoints())
		c=img_window.getPressedKey()
		if c == ord('q'):
			img_window.quit()
			break

		if c == ord('s'):
			coordinates.writeCoordinatesFile(filename="data/coordinates.json")

			img_window.saveImage("images/colonies_processed.jpg")

			for coord in coordinates.coord_transformed:
				print(coord)
		continue


def main(args):
	
	while True:
		
		cmd=input()
		
		if cmd=="quit":
			break
			
		if cmd=="process":
		
			r = requests.get('http://192.168.200.63:5000/getImageFilename')
			filename=r.text

			imageProcessing(filename)

		jsonData = json.dumps({'cmd':cmd})
		r = requests.post('http://192.168.200.63:5000/addCommand', json=jsonData)
	
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
