import cv2 as cv
import numpy



def func(x):
	
	print("")


cap = cv.VideoCapture(0)
track = cv.namedWindow("track")

cv.createTrackbar("U_H","track",110,180,func)
cv.createTrackbar("U_S","track",255, 255, func)
cv.createTrackbar("U_V","track",255, 255, func)
cv.createTrackbar("L_H","track",68,180, func)
cv.createTrackbar("L_S","track",55, 255, func)
cv.createTrackbar("L_V","track",54, 255, func)


while(True):
	cv.waitKey(1000)
	ret,inframe = cap.read()
	
	if(ret):
		break


while(True):
	ret,frame = cap.read()
	imghsv= cv.cvtColor(frame, cv.COLOR_BGR2HSV)

	
	U_H = cv.getTrackbarPos("U_H", "track")
	U_S = cv.getTrackbarPos("U_S", "track")
	U_V = cv.getTrackbarPos("U_V", "track")
	L_V = cv.getTrackbarPos("L_V","track")
	L_H = cv.getTrackbarPos("L_H","track")
	L_S = cv.getTrackbarPos("L_S","track")

	
	kernel = numpy.ones((3,3),numpy.uint8)

	upper = numpy.array([U_H,U_S,U_V])
	lower = numpy.array([L_H,L_S,L_V])

	mask = cv.inRange(imghsv, lower, upper)
	mask = cv.medianBlur(mask,3)
	mask_inv = 255-mask 
	mask = cv.dilate(mask,kernel,5)
	
	
	b = frame[:,:,0]
	g = frame[:,:,1]
	r = frame[:,:,2]
	b = cv.bitwise_and(mask_inv, b)
	g = cv.bitwise_and(mask_inv, g)
	r = cv.bitwise_and(mask_inv, r)
	frame_merge = cv.merge((b,g,r))

	b = inframe[:,:,0]
	g = inframe[:,:,1]
	r = inframe[:,:,2]
	b = cv.bitwise_and(b,mask)
	g = cv.bitwise_and(g,mask)
	r = cv.bitwise_and(r,mask)
	cloak = cv.merge((b,g,r))

	out = cv.bitwise_or(frame_merge, cloak)

	cv.imshow("Harry's cloak",out)

	if(cv.waitKey(2) == 27):
		break

cv.destroyAllWindows()
cap.release()