import cv2
import numpy as np
from matplotlib import pyplot as plt
from skimage import measure

def getAnswers(im, i):
	label = measure.label(im, background=0)
	props = measure.regionprops(label)
	colord = plt.imshow(label, cmap='spectral')
	plt.axis('off')
	plt.tight_layout()
	plt.show()

	a, b = im.shape[:2]
	bound1 = b/4
	bound2 = bound1*2
	bound3 = bound1*3
	bound4 = b

	# print(b)
	# print(bound1, bound2, bound3, bound4)


	for p in props:
		x, y = p.centroid

		if y > 0 and y <= bound1:
			print(str(i), 'A')
		elif y > bound1 and y <= bound2:
			print(str(i), 'B')
		elif y > bound2 and y <= bound3:
			print(str(i), 'C')
		elif y > bound3 and y <= bound4:
			print(str(i), 'D')

		i = i+1

	return;



# start ---------------------------------------------------------------

img = cv2.imread("Sheet13.png")
img = 255-img
erode =  cv2.morphologyEx(img, cv2.MORPH_OPEN, np.ones((5,5)))
gray = cv2.cvtColor(erode, cv2.COLOR_BGR2GRAY)
r, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

# cv2.imshow('', erode)

blobs_labels = measure.label(thresh, background=0)
props = measure.regionprops(blobs_labels)
colord = plt.imshow(blobs_labels, cmap='spectral')
plt.axis('off')
plt.tight_layout()
# plt.show()

# for p in props:
# 	x, y = p.centroid
# 	if x > 400:
# 		print(p.centroid)

ans_p1 = props[3]
ans_p2 = props[4]

x, y, x2, y2 = ans_p1.bbox
ans_i1 = thresh[x+6:x2-6, y+6:y2-6]
getAnswers(ans_i1, 1)

x, y, x2, y2 = ans_p2.bbox
ans_i2 = thresh[x+6:x2-6, y+6:y2-6]
getAnswers(ans_i2, 16)


# cv2.imshow('left?', ans_i1)
# cv2.imshow('right?', ans_i2)

cv2.waitKey(0)
cv2.destroyAllWindows()