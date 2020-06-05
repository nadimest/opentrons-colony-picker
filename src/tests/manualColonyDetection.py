#!/usr/bin/env python3

import cv2
from copy import deepcopy
import numpy as np

SOURCE="colonies_test.jpg"


colonies_img= cv2.imread(SOURCE)

cv2.imshow("win",colonies_img)
cv2.waitKey()

