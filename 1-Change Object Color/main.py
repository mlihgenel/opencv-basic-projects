import cv2
import numpy as np

image = cv2.imread("input.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])
# hsv uzayında kırmızı için üst ve alt değerler.

mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = cv2.bitwise_or(mask1, mask2)
# maskeleme işlemi 

mask = cv2.dilate(mask, np.ones((9,9), np.uint8), iterations=1)
mask = cv2.GaussianBlur(mask, (3,3), 0)

background = np.zeros(shape=image.shape)  
object_only = cv2.bitwise_and(image, image, mask=mask)  


hsv_object = cv2.cvtColor(object_only, cv2.COLOR_BGR2HSV) 
hsv_object[:, :, 0][mask > 50] = 150 
final_object = cv2.cvtColor(hsv_object, cv2.COLOR_HSV2BGR)  



cv2.imshow("Purple Image", final_object)  
cv2.waitKey(0)
cv2.destroyAllWindows()
