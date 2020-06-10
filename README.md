# opentrons-colony-picker
A minimally invasive colony picker mod for the Opentrons OT2 liquid handling robot

### Concept

This mod adds three main features to the OT2. 

1) A camera next to the pipettes housing to capture live feed of one slot of the deck.
2) A custom labware holder with and LED strip to provide backlight illumination and increase contrast 
3) Simple image processing software to select a list of destination points in the labware.

### Implementation

Since I didn't want to reflash OT2's Raspberry Pi or add any additional hardware to it, I dismounted the deck camera and fixed it behind the pipettes housing.

In this basic implementation I am using the OT2's jupyter notebook server to run scritps in different codeblocks, such as:

* Initalize the robot and labware
* Move the pipettes housing so the camera is centered over the labware
* Take a picture 
* Prompt user to run a local script to detect coordinates
* Load colony coordinates
* Run the colony picking protocol

Plus, some additional blocks used for calibration purposes.

### Colonies coordinates detection

No image processing library is installed con the OT2 image, (and no jupyter notebook widgets, to capture the clicked position on an image), Without reflashing a custom OT2 image using buildroot, I can't use opencv
and since I didn't want to rebuild a OT2 image (which I could do using buildroot), I am running the colony detection script in a local machine

The detection program uses  OpenCV and its highgui to display an image an allow the user to click on the image to choose the colonies.

The programs runs the following procedures:

* Fetching the image remotely from the robot using ssh. (An ssh key must have been set up in the robot and a copy in the client)
* Click on the image to define the colony positions.
* Push the coordinates in a json format into the server, together with the processed image. 

### Hardware

Labware: Black 3D printed box with LED strips for back lighting.

Camera fixture: 3d printed holder attached to the 2020 aluminum rails on the pipette housing
