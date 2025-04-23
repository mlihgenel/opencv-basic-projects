import cv2 
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("Find_Shape_with_Contours/input.jpg")
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

_, thresh = cv2.threshold(imgGray, 190, 255, cv2.THRESH_BINARY)
kernel = np.ones((3,3))
thresh = cv2.erode(thresh, kernel, iterations=2) # thresh işlemimizin sonucu daha iyi hale getirmek için

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

count = 0
for i in range(len(contours)):
    
    if hierarchy[0][i][3] == 46: # dış conturlar için. 46 olduğunu hierarchy dizisinin içinden bulduk. 
        cnt = contours[i]
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00']) # obje merkezinin x kordinatı
        cy = int(M['m01']/M['m00']) # obje merkezinin y kordinatı
        count += 1
        
        cv2.drawContours(img, contours, i, (0,255,0), 3)
        cv2.putText(img, str(count), (cx-10, cy+10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,0), 3)

cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
cv2.waitKey(0)
cv2.destroyAllWindows()