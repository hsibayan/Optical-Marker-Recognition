import extract_answers as e
import normalize as n
import cv2 as c
import imutils

test = range(4, 37)
defective = [8,15,16,17,19,20,26]



for i in test:
	if not i in defective:
		print("Doing this image: "+str(i))
		final = n.normalize(str(i))
		c.imshow("Image i"+str(i),imutils.resize(final.copy(), height=500))
		e.extract(final,str(i))

c.waitKey(0)
c.destroyAllWindows()