import cv2
import numpy as np

video_path = 'videos/video2.mp4'
cap = cv2.VideoCapture(video_path)

ret, frame1 = cap.read()

prevImg = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

hsv_mask = np.zeros_like(frame1)
hsv_mask[:,:,1] = 255

while True:

    ret, frame2 = cap.read()
    nextImg = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

    flow = cv2.calcOpticalFlowFarneback(prevImg, nextImg, None, 0.5, 4, 15, 3, 5, 1.2, 0)

    mag, ang = cv2.cartToPolar(flow[:,:,0], flow[:,:,1], angleInDegrees = True)

    hsv_mask[:,:,0] = ang/2
    hsv_mask[:,:,2] = cv2.normalize(mag, None, 0,255, cv2.NORM_MINMAX)

    bgr = cv2.cvtColor(hsv_mask, cv2.COLOR_HSV2BGR)
    cv2.imshow('frame', bgr)

    k = cv2.waitKey(30) & 0xFF
    if k == ord('q'):
        break

    prevImg = nextImg

cv2.destroyAllWindows()
cap.release()