import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import measure


def fixRotation(image):
	scratch = image.copy()
	gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
	gray = cv2.GaussianBlur(gray.copy(), (5, 5), 0)

	edged = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
	edged = 255-edged;
	edged =  cv2.morphologyEx(edged, cv2.MORPH_OPEN, np.ones((4,4)))


	# cv2.imshow("Here",scratch)
	# cv2.imshow("otherside",edged)

	blobs_labels, lent = measure.label(edged, background=0, return_num=1)
	props = measure.regionprops(blobs_labels)


	areas = []
	i = 0
	for p in props:
		areas.append([p.area, p.bbox, p.centroid ,i])
		i = i + 1

	areas.sort(reverse=True)

	x, y, x2, y2 = areas[2][1]
	b1 = image[x:x2, y:y2]

	x, y, x2, y2 = areas[3][1]
	b2 = image[x:x2, y:y2]

	# cv2.imshow('b1', b1)
	# cv2.imshow('b2', b2)

	height = np.size(image, 0)
	width = np.size(image, 1)
	
	row_of_name = areas[3][2][0]

	if(row_of_name > height/2):
		image=cv2.flip(image,0)
		image=cv2.flip(image,1)

	# cv2.imshow("final",image)
	return image
