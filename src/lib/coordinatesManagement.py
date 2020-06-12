#!/usr/bin/env python3

from .pointsManagement import pointsManager
import json

class CoordinatesManager(pointsManager):

    def __init__(self, calibration_filename):
        super().__init__()

        with open(calibration_filename) as calibration_file:
            calibration=json.load(calibration_file)

        self.scale=calibration['SCALE']
        self.chosenSlot=str(calibration['CHOSEN_SLOT'])
        self.calibration_points=calibration['SLOTS'][self.chosenSlot]

    def transformCoordinates(self,coord):
        """ See the pixelToDeck_factor_Calculation readme file for the source of these transformation formulas"""
        X_new = self.scale * (coord[0] - self.calibration_points['front_left_screw_px'][0]) + self.calibration_points['front_left_screw_mm'][0]
        Y_new = self.scale * (self.calibration_points['front_left_screw_px'][1] - coord[1]) + self.calibration_points['front_left_screw_mm'][1]

        return (X_new, Y_new)

    def writeCoordinatesFile(self,filename="coordinates.json"):

        self.coord_transformed = [self.transformCoordinates(item) for item in self.elements]
        coord_json= {'coordinates': self.coord_transformed}

        with open(filename,'w') as coordinates_file:
            json.dump(coord_json,coordinates_file)