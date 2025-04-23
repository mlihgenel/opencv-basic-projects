import cv2 
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("input.jpg")
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(imgGray, 190, 240, cv2.THRESH_BINARY)
kernel = np.ones((3,3))
thresh = cv2.erode(thresh, kernel, iterations=2)


cv2.imshow("img", thresh)    
cv2.waitKey(0)
cv2.destroyAllWindows()