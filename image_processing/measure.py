from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
	
image = cv2.imread('test.png')
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if imutils.is_cv2() else cnts[1]

(cnts, _) = contours.sort_contours(cnts)
object=1
# loop over the contours individually
for c in cnts:
	if cv2.contourArea(c) < 100:
		continue

	orig = image.copy()
	cv2.drawContours(orig, c, -1, (0, 255, 0), 2)
 
 	print "Object", object, ": ", cv2.contourArea(c)
 	object+=1

	cv2.imshow("Image", orig)
	cv2.waitKey(0)
	
