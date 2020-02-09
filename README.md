# opentrons-colony-picker
A colony picker mod for the Opentrons OT2 liquid handling robot

### Concept

This mod adds two main features to the OT2. 

1) A camera next to the pipettes housing to capture live feed of one slot of the deck.
2) A custom labware holder with and LED strip to provide backlight illumination and increase contrast 
3) Simple image processing software to select a list of destination points in the labware.

### Implementation
Since I didn't want to reflash OT2's Raspberry Pi or add any hardware to it, I attached a second Raspberry Pi (Colony-PI) on the housing and used the official V2 camera module.

A remote connection to Colony-PI enables the user to run a GUI, move the camera around, calibrate the colonies's labware height and choose the positions of the colonies to be picked.



