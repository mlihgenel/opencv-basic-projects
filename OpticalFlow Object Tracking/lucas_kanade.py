from corner_detect import * 
import cv2
import numpy as np 

lk_params = dict(
    winSize = (7,7),
    maxLevel = 2,
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)
video_path = 'videos/video2.mp4'
cap = cv2.VideoCapture(video_path)
ret, old_frame = cap.read()

width = old_frame.shape[0]
height = old_frame.shape[1]

mask = np.zeros_like(old_frame)
old_gray = first_gray

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    if p0 is not None:
        
        p1, status, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
        good_new = p1[status==1]
        good_old = p0[status==1]
        
        if len(good_new) > 0:
            a,b = good_new[0].ravel()
            c,d = good_old[0].ravel()
            
            mask = cv2.line(mask, (int(a), int(b)), (int(c), int(d)),  (0,255,0), 3)
            frame = cv2.circle(frame, (int(a), int(b)), 5,(0,0,255), -1)
            
            img = cv2.add(frame, mask)
            cv2.imshow('frame', img)
            
            old_gray = frame_gray.copy()
            p0 = good_new.reshape(-1,1,2)
        
        else:
            p0 = None 
               
    k = cv2.waitKey(25) & 0xFF
    if k == ord('q'):
        break
      
cv2.destroyAllWindows()
cap.release()
    
