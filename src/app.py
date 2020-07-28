#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  app.py

import requests,json

from imageHandling import ImageHandler

def runColonies(coordinates):
	
	well_idx=0
	#instr.reset_tipracks()
	for coord in coordinates:
		
		coord=coordinates[well_idx]
		print(coord)
		
		try:
			instr.pick_up_tip()
		except:
			print("Cant pick up new tips (Is there one attached?)")
		
		move_to_point(coord)
		instr.move_to(plate.wells()[well_idx].bottom(3))

		try:
			instr.drop_tip()
		except:
			print("Unable to drop tip (Is there one attached?)")

		
		well_idx=well_idx+1

def main(args):
	
	while True:
		
		cmd=input()
		
		if cmd=="q":
			break
			
		if cmd=="/openImage":
		
			r = requests.get('http://192.168.200.63:5000/getImageFilename')

			imageHandler=ImageHandler()

			showImage(r.text)
			
			continue
			
		jsonData = json.dumps({'cmd':cmd})
		r = requests.post('http://192.168.200.63:5000/addCommand', json=jsonData)
	
	return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
