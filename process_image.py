import cv2 as cv
import numpy as np
from pathlib import Path
import os

image_dir = "images_syringes"
if(os.path.isdir(image_dir)):
	for file in os.listdir(image_dir):
		if file.endswith(".jpg") or file.endswith(".png") or file.endswith("jpeg"):
			im = cv.imread(file)
			hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
			# define range of blue color in HSV
    		lower_blue = np.array([110,50,50])
    		upper_blue = np.array([130,255,255])
    		# Threshold the HSV image to get only blue colors
    		mask = cv.inRange(hsv, lower_blue, upper_blue)
			# Bitwise-AND mask and original image
    		res = cv.bitwise_and(im,im, mask= mask)
else:
	print("File is not found")
