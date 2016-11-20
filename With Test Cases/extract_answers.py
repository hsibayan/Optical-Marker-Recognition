import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import measure

def getAnswers(im, i):

	r, thresh = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
	thresh = 255-thresh;
	thresh =  cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3,3)))

	a, b = im.shape[:2]
	bound1 = b/4
	bound2 = bound1*2
	bound3 = bound1*3
	bound4 = b

	height = a/15;
	width = b

	lowerbound = 1
	upperbound = height

	results = []
	for n in range(i, (i+15)):
		img = thresh[lowerbound:upperbound, 1:width]
		# cv2.imshow(str(n), img)

		label, count = measure.label(img, background=0, return_num=True)
		props = measure.regionprops(label)
		# colord = plt.imshow(label, cmap='spectral')
		# plt.axis('off')
		# plt.tight_layout()
		# plt.show()

		shaded = []
		for p in props:
			# print(p.area)
			if p.area > 700:
				shaded.append(p)

		shadeCount = len(shaded)

		if shadeCount > 1:
			results.append([n, 'Shade Error (more than 1 shade)'])
		elif shadeCount == 0:
			results.append([n, 'Shade Error (no shade)'])
		else:
			# results.append([n, 'Good Shade! Good job <3'])
			letter = None
			x, y = shaded[0].centroid
			if y >= 0 and y <= bound1:
				letter = 'A'
			elif y > bound1 and y <= bound2:
				letter = 'B'
			elif y > bound2 and y <= bound3:
				letter = 'C'
			elif y > bound3 and y <= bound4:
				letter = 'D'
			results.append([n, letter])

		lowerbound += height
		upperbound += height

	# for r in results:
	# 	print(r[0], r[1])

	return results


# start ---------------------------------------------------------------
def extract(final_output,filename):
	
	img = final_output
	img = cv2.medianBlur(img,5)

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	thresh = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)

	thresh = 255-thresh;
	thresh =  cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3,3)))
	# cv2.imshow('adap', thresh)
	# cv2.imshow('not adap', thresh2)

	blobs_labels, lent = measure.label(thresh, background=0, return_num=1)
	props = measure.regionprops(blobs_labels)
	colord = plt.imshow(blobs_labels, cmap='spectral')
	plt.axis('off')
	plt.tight_layout()
	# plt.show()

	areas = []
	i = 0
	for p in props:
		areas.append([p.area, p.bbox, p.centroid])
		i = i + 1

	areas.sort(reverse=True)

	x1, y1 = areas[0][2]

	h, width = img.shape[:2]
	midpoint = width/2

	if y1 < midpoint:
		left = areas[0][1]
		right = areas[1][1]
	else:
		left = areas[1][1]
		right = areas[0][1]

	x, y, x2, y2 = left
	ans_i1 = gray[x+12:x2-12, y+12:y2-12]
	results = getAnswers(ans_i1, 1)

	x, y, x2, y2 = right
	ans_i2 = gray[x+12:x2-12, y+12:y2-12]
	results_right = getAnswers(ans_i2, 16)

	results = results + results_right

	text_file = open('_Results/' + filename + '.txt', 'w')

	for r in results:
		# print(r[0], r[1])
		text_file.write(str(r[0]) + ' ' + r[1] + '\n')

	text_file.close()

	# cv2.imshow('left?', ans_i1)
	# cv2.imshow('right?', ans_i2)