import cv2
import numpy as np
import glob 

CHESSBOARD = (6,9)

criteria = (cv2.TERM_CRITERIA_MAX_ITER + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.001)

objPoints = [] # --> gerçek dünyadaki koordinatlar için
imgPoints = [] # --> resimdeki koordinatlar için

# 1, 9*6, 3 --> 1,54,3 olmalı 
# köşe noktalarının koordinatlarını tutar 3D
objp = np.zeros((CHESSBOARD[0]*CHESSBOARD[1], 3), dtype=np.float32) 
# köşe noktalarının 2D gerçek dünyadaki yerlerini temsil eder. 
objp[:, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2) 


images = glob.glob('images/*.jpg') 

for fnames in images:
    img = cv2.imread(fnames)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD, None)
    
    if ret:
        objPoints.append(objp)
        corners2 = cv2.cornerSubPix(image=gray, corners=corners, winSize=(11,11), zeroZone=(-1,-1), criteria=criteria)
        imgPoints.append(corners2.copy())
        
        cv2.drawChessboardCorners(image=img, patternSize=CHESSBOARD, corners=corners2, patternWasFound=ret)
    
    cv2.imshow('img', img)
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints, imgPoints, gray.shape[::-1], None, None)

"""
ret   --> (reprojection error) kalibrasyonadaki ortalama hata değeri 
mtx   --> (intrinsic matrix) kamera matrisi - odak uzaklıkları (fx, fy) ve optik merkez (cx, cy) içerir.
dist  --> (distortion coefficients) lens bozulma katsayıları 
rvecs --> (rotation vectors) 3D dönüş vektörü - kameranın nesneye göre dönüşünü söyler 
tvecs --> (translation vectors) 3D konum vektörü - kameranın nesneye göre konumu söyler 
"""
print("Reprojection Error: ", ret)
print("\nIntrinsic Matrix: \n", mtx)
print("\nDistortion Coefficients : ", dist)

