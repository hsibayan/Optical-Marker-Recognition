import cv2
import numpy as np
import fourpoint as f
import rotate
import imutils

def normalize(filename):
	image = cv2.imread("_Test Photos/"+filename+".jpg")
	height = np.size(image, 0)
	width = np.size(image, 1)

	# if(height < width):
	# 	image = imutils.resize(image.copy(), height=1000)
	# else:
	# 	image = imutils.resize(image.copy(), width=1000)
	# cv2.imshow("original",image)
	# cv2.imshow("normal,",normal_image)

	scratch = image.copy()
	gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray.copy(), (5, 5), 0)
	edged = cv2.Canny(gray, 50, 200)
	#opening = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)

	im2, cnts, hier = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
	sorted_c = sorted(cnts, key = cv2.contourArea, reverse = True)


	for c in sorted_c:
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		if len(approx) == 4:
			paper = approx
			break



	cv2.drawContours(scratch, [paper], -1, (0,255,0), 3)
	warped = f.four_point_transform(image.copy(), paper.reshape(4, 2))
	warped = cv2.resize(warped, (1275, 1650)) 
	# cv2.imshow("Warped",warped)
	# cv2.imshow("Original",image)
	# cv2.imshow("Gray",gray)
	# cv2.imshow("Edges",edged)
	# cv2.imshow("Scratch",scratch)
	final = rotate.fixRotation(warped)

	return final