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

img = cv2.imread("m1.png")
# img = 255-img
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.blur(gray,(7,7));
r, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
thresh = 255-thresh;
thresh =  cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((4,4)))
# thresh = 255-thresh;
# thresh =  cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, np.ones((3,3)))
# thresh =  cv2.dilate(thresh, np.ones((4,4)))

# cv2.imshow('', thresh)

blobs_labels = measure.label(thresh, background=0)
props = measure.regionprops(blobs_labels)
colord = plt.imshow(blobs_labels, cmap='spectral')
plt.axis('off')
plt.tight_layout()
# plt.show()

# cv2.imshow('', ans_i1)

# for p in props:
# 	print(p.area)



ans_p1 = props[4]
ans_p2 = props[3]

x, y, x2, y2 = ans_p1.bbox
ans_i1 = thresh[x+10:x2-12, y+12:y2-12]
# ans_i1 = thresh[x:x2, y:y2]
getAnswers(ans_i1, 1)

x, y, x2, y2 = ans_p2.bbox
ans_i2 = thresh[x+10:x2-12, y+12:y2-12]
# ans_i2 = thresh[x:x2, y:y2]
getAnswers(ans_i2, 16)


# cv2.imshow('left?', ans_i1)
# cv2.imshow('right?', ans_i2)

cv2.waitKey(0)
cv2.destroyAllWindows()