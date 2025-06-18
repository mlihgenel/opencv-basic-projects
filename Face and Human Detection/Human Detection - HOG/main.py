import cv2

# HOG tanımlayıcıyı başlat
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Görüntüyü yükle
image = cv2.imread("people.jpg")
image = cv2.resize(image, (800, 500)) 

# Farklı tarama ayarları
ayarlar = [
    {"isim": "Hassas", "winStride": (2, 2), "padding": (16, 16)},
    {"isim": "Dengeli", "winStride": (8, 8), "padding": (8, 8)},
    {"isim": "Hizli", "winStride": (16, 16), "padding": (4, 4)}
]

# Her ayar için ayrı pencere göster
for ayar in ayarlar:
    img_copy = image.copy()
    rects, _ = hog.detectMultiScale(
        img_copy,
        winStride=ayar["winStride"],
        padding=ayar["padding"],
        scale=1.05
    )
    for (x, y, w, h) in rects:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
    cv2.imshow(f"{ayar['isim']} Tespit", img_copy)

cv2.waitKey(0)
cv2.destroyAllWindows()
