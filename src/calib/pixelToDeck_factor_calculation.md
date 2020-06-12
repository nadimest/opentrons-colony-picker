
We have now two set of coordinates for the screws:

Deck Coordinates (in mm, they are given to the robot to move to a certain position)

(Example for Slot 6)
front_left=[270, 96]
rear_left=[270, 171]
front_right=[387, 96]
rear_right=[387, 171]

Image coordinates (in px, they are the output of the colonies selection process)

front_left_screw=(31,578)
rear_left_screw=(31,70)
front_right_screw=(828,578)
rear_right_screw=(828,70)

We need a function that transform an image coordinate into a deck coordinate.
 
The assumptions are that the image is always taken in the same deck position.
 (For slot 6 this is camera_center_slot6=[310, 75])

So a univocal relationship can be obtained.

If we don't assume that pixel width and height are the same, then we need two scale factors, one per axis

X_scale [mm/px]=  [387-270]/[828-31]  = 0.1468
Y_scale [mm/px]=  [171-96] /[578-70] = 0.1476

With a 0.5% discrepancy, we can consider one scale equal to 

SCALE=0.147

(These numbers can be refined after calibration)

Lets define a new coordinates origin at the front left screw.

Notice that the pixel Y axis and deck Y axis are inverted. This can be confusing, lets take care of this before we run the coordinates transformation

(px*,py*)  ->  (px, IMAGE_HEIGHT - py)

Now lets define the new origin at the front-left screw (px_FL, py_FL)

(px**,py**) ->  (px - px_FL, (IMAGE_HEIGHT-py)-(IMAGE_HEIGHT-py_FL) )
(px**,py**) ->  (px - px_FL, py_FL-py)

Now I need to convert the new pixel into mm and add the offset for the front left screw (X_FL,Y_FL)=([270 mm, 96mm ])

X*= SCALE* px**  + X_FL
Y*= SCALE* py**  + Y_FL

And using the original coordinates:

X_new =  SCALE * (px-px_FL) + X_FL
Y_new =  SCALE * (py_FL-py) + Y_FL

------------------


 
# coordinates=[
#     [339,132],
#     [349,142],
#     [309,115]
# ]

