import cv2
import numpy as np

video_path = 'videos/video2.mp4'
cap = cv2.VideoCapture(video_path)
ret, frame = cap.read()

roi = cv2.selectROI("ROI Secimi", frame, fromCenter=False, showCrosshair=False) 

x, y, w, h = roi
x_min = x
y_min = y
x_max = x + w
y_max = y + h

feature_params = dict(
    maxCorners = 20,
    qualityLevel = 0.3,
    minDistance = 7,
    blockSize = 7
)

first_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

points = cv2.goodFeaturesToTrack(image=first_gray,
                                 mask = None,
                                 **feature_params)

selected_point = None 

for point in points:
    x,y = point.ravel()
    if y_min <= y <= y_max and x_min <= x <= x_max:
        selected_point = point 
        break # --> sadece tek bir noktayı almış olduk 
    
if selected_point is not None:
    print("Köşe noktası bulundu.")
    p0 = np.array([selected_point], dtype=np.float32)
else:
    print("Köşe noktası bulunamadı.")
    
