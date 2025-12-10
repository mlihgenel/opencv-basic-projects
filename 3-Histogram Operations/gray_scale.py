import cv2
import matplotlib.pyplot as plt

# Üzerinde çalışacağımız resim grayscale olacak
img = cv2.imread("Histogram_Operations/input.png")
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Burada orijinal resmimizin histogramını hesaplıyoruz 
gray_img_hist = cv2.calcHist([img_gray], channels=[0], mask=None, histSize=[256], ranges=[0,255])
plt.figure(figsize=(6,6))
plt.title("RAW Image Histogram")
plt.plot(gray_img_hist)
plt.xlabel("Intensity")
plt.ylabel("# of Pixels")
plt.show(block=False)

# Geleneksel olan histogram eşitleme metodunu kullanıyoruz. 
equalize_img = cv2.equalizeHist(img_gray)
plt.figure(2, figsize=(6,6))
plt.subplot(211)
plt.title("EqualizeHist Metodu ile")
plt.imshow(equalize_img, cmap="gray")
plt.axis("off")
plt.show(block=False)

# Histogram eşitlemesi yaptığımız resmin tekrardan histogramını çizdiriyoruz. 
equalize_img_hist = cv2.calcHist([equalize_img], channels=[0], mask=None, histSize=[256], ranges=[0,255])
plt.subplot(212)
plt.title("Equalize Image Histogramı")
plt.plot(equalize_img_hist)
plt.show(block=False)

# -- CLAHE Yöntemi ile Histogram İşlemleri --

# CLAHE metodu ile histogram eşitlemesi yapıyoruz. 
clahe = cv2.createCLAHE(clipLimit=5, tileGridSize=(12,12))
clahe_img = clahe.apply(img_gray)
plt.figure(figsize=(6,6))
plt.subplot(211)
plt.imshow(clahe_img, cmap="gray")
plt.axis("off")
plt.title("CLAHE Metodu ile Eşitlenmiş Resim")
plt.show(block=False)


# Şimdi de eşitlenmiş resmin histogramını çizdireceğiz 
clahe_img_hist = cv2.calcHist([clahe_img], channels=[0], mask=None, histSize=[256], ranges=[0,255])
plt.subplot(212)
plt.plot(clahe_img_hist)
plt.title("CLAHE Metodu Histogramı")
plt.xlabel("Intensity")
plt.ylabel("# of Pixels")
plt.show(block=False)

plt.figure()
plt.title("CLAHE Metodu ile Eşitlenmiş Resim")
plt.imshow(clahe_img, cmap="gray")
plt.axis("off")
plt.show()


