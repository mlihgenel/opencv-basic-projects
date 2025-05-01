import numpy as np
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("input.jpg")
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

lower_mask = np.array([6, 100, 64])
upper_mask = np.array([42, 255, 255])

mask = cv2.inRange(img_hsv, lowerb=lower_mask, upperb=upper_mask)
result = cv2.bitwise_and(img_hsv, img_hsv, mask=mask)
result = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)


contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
external_contours = np.zeros_like(mask)

for i in range(len(contours)):
    
    if hierarchy[0][i][3] == -1:
        cv2.drawContours(external_contours, contours, i, 255, -1)
  
kernel = np.ones(shape=(3,3))      
erode = cv2.erode(external_contours, kernel, iterations=3)  
dilate = cv2.dilate(erode, kernel, iterations=1)

last_img = dilate.copy()

contours_final, _ = cv2.findContours(last_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

final_mask = np.zeros_like(last_img)

for cnt in contours_final:
    hull = cv2.convexHull(cnt)
    cv2.drawContours(final_mask, [hull], -1, 255, -1)

cv2.imshow("Last Image with more accurate", final_mask)
cv2.imshow("Mask Kivis", result)

cv2.waitKey()
cv2.destroyAllWindows()