import cv2
import matplotlib.pyplot as plt
from numpy import block

# Üzerinde çalışacağımız resim rgb formatında olacak
img = cv2.imread("Histogram/gorilla.jpg")
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # hsv formatına döndürerek işimizi kolaylaştırıyoruz

h, s, v = cv2.split(hsv_img)

clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(10,10))

# CLAHE içine sadece v(value) yani parlaklığı veriyoruz. Bu sayede resimdeki renklere zarar vermemiş olacağız
v_clahe = clahe.apply(v)
hsv_clahe = cv2.merge((h, s, v_clahe))

clahe_img = cv2.cvtColor(hsv_clahe, cv2.COLOR_HSV2RGB)


clahe_img_hist = cv2.calcHist([clahe_img], channels=[2], mask=None, histSize=[256], ranges=[0,255])


# Eşitlenmiş histogramı çizdiriyoruz. 
plt.figure(2, figsize=(7,7))
plt.plot(clahe_img_hist)
plt.title("CLAHE Metodu ile\nHSV Resmin V Kanalına Uygulanmış Histogram Eşitlemesi")
plt.xlabel("Intensity")
plt.ylabel("# of Pixels")
plt.show(block=False)


plt.figure(3,figsize=(5,7))

plt.subplot(311)
plt.title("Original Resim")
plt.imshow(rgb_img)
plt.axis("off")
plt.show(block=False)


plt.subplot(312)
plt.title("HSV Formatındaki Resim")
plt.imshow(hsv_img)
plt.axis("off")
plt.show(block=False)


plt.subplot(313)
plt.title("CLAHE Metodu Uygulanmış Resim")
plt.imshow(clahe_img)
plt.axis("off")
plt.show()




