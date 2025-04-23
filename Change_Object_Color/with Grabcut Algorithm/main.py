import cv2
import numpy as np


img = cv2.imread('Change-Color/with Grabcut Algorithm/input.jpg')

height, width = img.shape[:2]

mask = np.zeros(img.shape[:2], np.uint8)

fgModel = np.zeros((1, 65), np.float64)
bgModel = np.zeros((1, 65), np.float64)

rect = (150, 110, 770, 500)

cv2.grabCut(img, mask, rect, bgModel, fgModel, 4, cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
grabcut_result = img * mask2[:, :, np.newaxis]

kernel = np.ones((5,5), np.uint8)
cleaned_mask = cv2.morphologyEx(mask2, cv2.MORPH_OPEN, kernel)

lower_red1 = np.array([0, 50, 50])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 50, 50])
upper_red2 = np.array([180, 255, 255])

hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

mask_for_red = cv2.inRange(hsv, lower_red1, upper_red1)
mask_for_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

mask_all = cv2.bitwise_or(mask_for_red, mask_for_red2)

mask_all = cv2.dilate(mask, np.ones((9,9), np.uint8), iterations=5)
mask_all = cv2.GaussianBlur(mask, (3,3), 0)

hsv[:, :, 0][mask_all > 0] = 160

purple_rose = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
purple_rose = purple_rose * cleaned_mask[:, :, np.newaxis]


while True:
    
    cv2.imshow('Final', purple_rose)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
cv2.destroyAllWindows()
