import cv2
import numpy as np
from matplotlib import cm

img = cv2.imread("landscape.jpg")
land_copy = img.copy()

marker_img = np.zeros(img.shape[:2], dtype=np.int32)

segments = np.zeros(img.shape, dtype=np.uint8)

def create_rgb(i):
    return tuple(np.array(cm.tab10(i)[:3])*255)

colors = []
for i in range(10):
    colors.append(create_rgb(i))

n_markers = 10 # 0-9 
# RENK SEÇİMİ
current_marker = 1
# WATERSHED İLE MARKER GÜNCELLEMESİNİ TUTMAK İÇİN 
marks_updated = False

def mouse_callback(event,x,y,flags,params):
    global marks_updated

    if event == cv2.EVENT_LBUTTONDOWN:
        # WATERSHED ALGORİTMASINA GEÇİLECEK OLAN MARKERLAR
        cv2.circle(marker_img, (x,y), 10, current_marker, -1)

        # KULLANICININ RESİMDE GÖRDÜĞÜ
        cv2.circle(land_copy, (x,y),10, colors[current_marker], -1)

        marks_updated = True
        

cv2.namedWindow('Road Image')
cv2.setMouseCallback('Road Image', mouse_callback)

while True:

    cv2.imshow('Watershed Segments', segments)
    cv2.imshow('Road Image', land_copy)

    k = cv2.waitKey(0)

    if k == 27:
        break

    # EKRANI TEMİZLEMEK İÇİN 
    elif k == ord('c'):
        road_copy = img.copy()
        marker_img = np.zeros(img.shape[:2], dtype=np.int32)
        segments = np.zeros(img.shape, dtype=np.uint8)

    # RENK SEÇİMİNİ GÜNCELLEME 
    elif k > 0 and chr(k).isdigit():
        current_marker = int(chr(k))

    # MARKERLARI GÜNCELLEME 
    if marks_updated:

        marker_img_copy = marker_img.copy()
        cv2.watershed(img, marker_img_copy)

        segments = np.zeros(img.shape, dtype=np.uint8)

        for color_ind in range(n_markers):
            segments[marker_img_copy==(color_ind)] = colors[color_ind]


cv2.destroyAllWindows()
        
        

        
        