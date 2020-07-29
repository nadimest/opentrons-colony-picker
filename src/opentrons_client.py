import os, time, requests
from opentrons.execute import get_protocol_api
from opentrons import types

import json, sys

TIPRACK_SLOT = 5
PLATE_SLOT = 3
SAFE_Z_HEIGHT = 150
MIN_Z_HEIGHT = 72
BOX_CORNER_HEIGHT = 72  # 125 without the tip
camera_center_slot6 = [310, 75, SAFE_Z_HEIGHT]


class Robot():

    def __init__(self):
        self.protocol = get_protocol_api('2.0')

        # Custom labware assignation
        custom_labware_folder = "custom_labware"
        labwareFilename = custom_labware_folder + "/Petri 1 Reservoir 50000 µL.json"

        with open(labwareFilename) as labware_file:
            labware_def = json.load(labware_file)
            colonies1 = self.protocol.load_labware_from_definition(labware_def, 6)

        tiprack = self.protocol.load_labware('opentrons_96_tiprack_300ul', TIPRACK_SLOT)
        self.plate = self.protocol.load_labware('corning_96_wellplate_360ul_flat', PLATE_SLOT)

        # Pipette assignation
        self.instr = self.protocol.load_instrument('p50_single_v1.3', 'right', tip_racks=[tiprack])
        self.well_idx = 0

    def home(self):
        self.instr.home()
        self.protocol.home()

    def move_to_point(self, coordinates):
        point = types.Point(*coordinates)
        self.instr.move_to(location=types.Location(point=point, labware=None), minimum_z_height=SAFE_Z_HEIGHT)

    def pickColony(self, coord):

        try:
            self.instr.pick_up_tip()
        except:
            print("Cant pick up new tips (Is there one attached?)")

        self.move_to_point(coord)
        self.instr.move_to(self.plate.wells()[self.well_idx].bottom(3))

        try:
            self.instr.drop_tip()
        except:
            print("Unable to drop tip (Is there one attached?)")

        self.well_idx = self.well_idx + 1

    def turnOnLights(self):
        self.protocol.set_rail_lights(True)

    def turnOffLights(self):
        self.protocol.set_rail_lights(False)


def take_picture():
    filename = '/data/colonies.jpg'
    cmd = 'ffmpeg -f video4linux2 -input_format mjpeg -s 1920x1080   -i /dev/video0  -frames 1 -vf crop=862:638:530:220 -y ' + filename
    #    cmd = 'ffmpeg -f video4linux2 -input_format mjpeg -s 1920x1080   -i /dev/video0  -frames 1 -vf eq=brightness=0.06:saturation=2 crop=862:638:530:220 -y '+filename

    stream = os.popen(cmd)
    time.sleep(2)

    return filename


def checkCoordinates(coord_str):
    coord = [int(x) for x in coord_str.split(',')]
    print(coord)
    if len(coord) == 3:
        if coord[2] >= MIN_Z_HEIGHT:
            return coord
    else:
        return 0


cmd = ""
while cmd != "quit":
    time.sleep(0.5)
    r = requests.get('http://192.168.200.63:5000/get')
    content = r.json()
    cmd = content['cmd']
    params = content['params']

    if cmd == "/init":
        robot = Robot()

    if cmd == "/home":
        try:
            robot.home()
        except:
            print("Could not home. Did you run /init ?")

    if cmd == "/slot6":
        try:
            robot.move_to_point(camera_center_slot6)
        except:
            print("Could not move. Did you run /init and /home?")

    if cmd == "/move" and params:

        coord = checkCoordinates(params)
        if coord:
            try:
                robot.move_to_point(coord)
            except:
                print("Could not move. Did you run /init and /home?")
        else:
            print("could not check Coordinates. Are they in the form of [int, int, int]?")

    if cmd == "/takePicture":
        imageFilename = take_picture()

        with open(imageFilename, 'rb') as f:
            requests.post('http://192.168.200.63:5000/uploadPicture', data=f)

    if cmd == "/lightsOn":
        robot.turnOnLights()

    if cmd == "/lightsOff":
        robot.turnOffLights()

    if cmd:
        print(cmd, params)