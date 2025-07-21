import cv2
import numpy as np

lk_params = dict(
    winSize = (15,15),
    maxLevel = 2,
    criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03)
)

clicked_point = []

def mouse_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point.append([x, y])
        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
        cv2.imshow("Nokta Sec", frame)

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if not ret:
    print("Kamera açılamadı.")
    cap.release()
    exit()

cv2.imshow("Nokta Sec", frame)
cv2.setMouseCallback("Nokta Sec", mouse_click)
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(clicked_point) == 0:
    print("Nokta seçilmedi.")
    cap.release()
    exit()

p0 = np.array([clicked_point[0]], dtype=np.float32).reshape(-1, 1, 2)
old_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
mask = np.zeros_like(frame)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    p1, status, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    good_new = p1[status==1] # --> status == 1 başarılı, status == 0 başarısız
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

cap.release()
cv2.destroyAllWindows()
