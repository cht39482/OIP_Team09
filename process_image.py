import cv2 as cv
import numpy as np
from pathlib import Path
import os
import matplotlib.pyplot as plt
image_dir = "images_syringes"
file="C:\\Users\\cht47\\OneDrive - Singapore Institute Of Technology\\Lessons\\OIP\\othercomp\\OIP_Team09\\syringe0.jpeg"
im = cv.imread(file)
print(type(im))
# hsv = cv.cvtColor(im, cv.COLOR_BGR2HSV)
# cv.imwrite("images_syringes\syringe0grey.jpg",hsv)
def greyscale_flipped(filename):
	os_path=os.path.join("images_syringes",file)
	im = cv.imread(os_path)
	hsv = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
	filename=file[:-5]
	flipped=cv.flip(im, 0)
	blurred = cv.GaussianBlur(hsv, (5, 5), 0)
	alpha = 0.8 # Contrast control (1.0-3.0)
	beta = -40 # Brightness control (0-100)

	adjusted = cv.convertScaleAbs(im, alpha=alpha, beta=beta)
	# show the output image and edge map
	cv.imwrite("images_syringes\\"+filename+"greyscale.jpg",hsv)
	cv.imwrite("images_syringes\\"+filename+"flipped.jpg",flipped)
	cv.imwrite("images_syringes\\"+filename+"blurred.jpg",blurred)
	cv.imwrite("images_syringes\\"+filename+"dark.jpg",adjusted)

if(os.path.isdir(image_dir)):
	for file in os.listdir(image_dir):
		if file.endswith(".jpg") or file.endswith(".png") or file.endswith("jpeg"):
			greyscale_flipped(file)


else:
	print("File is not found")

