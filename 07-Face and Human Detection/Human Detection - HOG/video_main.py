import cv2

# HOG tanımlayıcıyı başlat
hog = cv2.HOGDescriptor()

# OpenCV'nin önceden eğitilmiş insan tespit SVM'ini yükle
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Görüntüyü yükle
image = cv2.imread('people.jpg')
image = cv2.resize(image, (960, 600))

cap = cv2.VideoCapture('people_walking.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # İnsanları tespit et (çoklu ölçeklerde tarama)
    (rects, weights) = hog.detectMultiScale(frame, 
                                            winStride=(4, 4),
                                            padding=(4, 4), 
                                            scale=1.05)

    # Tespit edilen bölgeleri çiz
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('İnsan Tespit', frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break
    
cap.release()
cv2.destroyAllWindows()
