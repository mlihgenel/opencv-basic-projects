#  Kamera Kalibrasyonu (Camera Calibration)
---
Bu proje, OpenCV kullanarak bir kameranın kalibrasyonunu gerçekleştirmeyi amaçlar. Kalibrasyon işlemi, kameranın lensinden kaynaklı bozulmaları (distortion) matematiksel olarak modelleyip düzeltmemizi sağlar. Aşağıda teorik bilgiler ve proje içeriği detaylıca açıklanmıştır.

---

##  Kamera Kalibrasyonu Nedir?

Gerçek dünyadaki 3D noktaların kamera ile elde edilen 2D görüntüde nasıl göründüğü, kameranın **iç parametreleri** (intrinsic) ve **dış parametreleri** (extrinsic) ile tanımlanır.

Kamera kalibrasyonu:
- Kameranın iç parametrelerini (odak uzaklığı, optik merkez) bulur.
- Lens kaynaklı bozulma katsayılarını hesaplar.
- 3D–2D eşleşmeler yardımıyla bu parametreleri optimize eder.

### Pinhole Kamera Modeli
Pinhole (iğne deliği) modeli, kameranın ışığı sonsuz küçüklükteki bir delikten geçirerek görüntü düzlemine düşürdüğünü varsayar. Bu modelde **K** intrinsik matrisi aşağıdaki gibi tanımlanır:

```
K = | f_x  0    c_x |
    | 0    f_y  c_y |
    | 0    0     1  |
```

Burada:
* **f<sub>x</sub>, f<sub>y</sub>**: Odak uzaklıkları (piksel cinsinden)
* **c<sub>x</sub>, c<sub>y</sub>**: Optik merkezin piksel koordinatları

Bu matris, 3D bir noktanın kamera koordinat sisteminden 2D piksel koordinatlarına nasıl projeleneceğini belirler.

### Distortion (Bozulma) Türleri
Gerçek lensler ideal değildir ve çeşitli bozulmalara yol açar:
* **Radial Distortion** (`k1, k2, k3`): Görüntünün merkezine yaklaştıkça artan varil veya yastık bozulması.
* **Tangential Distortion** (`p1, p2`): Lensin sensöre tam hizalanmaması sonucu oluşur.
* **Prism / Thin-Prism**: Karmaşık lens sistemlerinde görülen ek sapmalar.

### Extrinsic Parametreler
Extrinsic parametreler kameranın dünyanın geri kalanına göre konumunu tanımlar:
* **R** (3×3 dönüş matrisi): Kameranın eksenlerini dünya eksenlerine göre döndürür.
* **t** (3×1 öteleme vektörü): Kameranın optik merkezinin dünya koordinatlarındaki konumunu gösterir.

Bu parametreler sayesinde bir noktanın dünya koordinatlarından kamera koordinatlarına dönüşümü yapılabilir.

---

##  Neden Kalibrasyon Gerekli?

-  Gerçek dünya ölçümleri yapmak için
-  Görüntüdeki perspektif ve bozulmaları düzeltmek için
-  Robotik, artırılmış gerçeklik, stereo vision gibi uygulamalarda doğru sonuçlar almak için

Kalibrasyonun doğruluğu genellikle **yeniden projeksiyon hatası** (reprojection error) ile ölçülür. Tipik olarak 0.3-0.5 pikselden küçük değerler iyi kabul edilir. Düşük hata değerleri, 3D yeniden yapılandırma, doğrusal ölçüm veya hassas robot kinematiği gibi görevlerde kritik öneme sahiptir.

Ayrıca kalibre edilmiş bir kamera ile:
* **İndustrial Metrology**: Milimetre altı hassasiyetle ölçüm yapılabilir.
* **Augmented Reality**: Sanal nesneler gerçek ortamla doğru hizada yerleştirilebilir.
* **Multi-Camera Sistemleri**: Stereo veya çoklu kamera kalibrasyonunda tutarlı bir referans sistemi oluşturulur.

---


##  Kod Açıklaması

```python
import cv2
import numpy as np
import glob
```
Bu kütüphaneler; OpenCV ile görüntü işlemleri, NumPy ile matris işlemleri, glob ile dosya arama için kullanılır.

```python
CHESSBOARD = (6, 9)  # iç köşe sayısı
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
```
`CHESSBOARD` kalıbın boyutunu, `criteria` ise köşe iyileştirme için durma şartlarını belirtir.

```python
objPoints = []  # 3D gerçek dünya noktaları
imgPoints = []  # 2D görüntüdeki köşe noktaları

objp = np.zeros((CHESSBOARD[0]*CHESSBOARD[1], 3), dtype=np.float32)
objp[:, :2] = np.mgrid[0:CHESSBOARD[0], 0:CHESSBOARD[1]].T.reshape(-1, 2)
```
`objp` sabit satranç tahtası koordinatlarını tutar ve her görüntü için `objPoints` listesine kopyalanır.

```python
images = glob.glob('images/*.jpg')

for fname in images:
    img = cv2.imread(fname)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD, None)
    if ret:
        objPoints.append(objp.copy())
        corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
        imgPoints.append(corners2)
        cv2.drawChessboardCorners(img, CHESSBOARD, corners2, ret)
        cv2.imshow('Corners', img)
        cv2.waitKey(500)
cv2.destroyAllWindows()
```
Bu döngü her görüntüde köşeleri bulur, `cv2.cornerSubPix` ile hassaslaştırır ve görselleştirir.

```python
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
    objPoints, imgPoints, gray.shape[::-1], None, None)
```
`calibrateCamera` fonksiyonu intrinsic matrisi **(mtx)**, ortalamalı yeniden projeksiyon hatası **(ret)**, bozulma katsayılarını **(dist)**, dönüş vektörlerini **(rvecs)** ve öteleme vektörlerini **(tvecs)** hesaplar. 



