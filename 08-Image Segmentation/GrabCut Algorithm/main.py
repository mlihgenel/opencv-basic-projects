import cv2
import numpy as np

drawing = False  
ix, iy = -1, -1 
rect = (0, 0, 1, 1)
rect_or_drawn = False  

img = cv2.imread("bird.jpg")
img_copy = img.copy()
mask = np.zeros(img.shape[:2], np.uint8)
bgModel = np.zeros((1, 65), np.float64)
fgModel = np.zeros((1, 65), np.float64)

def draw_rectangle(event, x, y, flags, param):
    global ix, iy, drawing, img_copy, rect, rect_or_drawn

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img_copy = img.copy()
            cv2.rectangle(img_copy, (ix, iy), (x, y), (0, 255, 0), 2)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
        rect_or_drawn = True
        cv2.rectangle(img_copy, (rect[0], rect[1]),
                      (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2)

cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)

print("Nesneyi seçmek için dikdörtgeni fareyle çiz. Bittiğinde 'g' tuşuna bas.")

while True:
    cv2.imshow("Image", img_copy)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('g') and rect_or_drawn:
        cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
        output_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        segmented = img * output_mask[:, :, np.newaxis]

        cv2.imshow("Segmented", segmented)
        print("Segmentasyon tamamlandı. Çıkmak için herhangi bir tuşa bas.")
    elif key == 27: 
        break

cv2.destroyAllWindows()
