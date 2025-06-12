# Watershed ile Görüntü Segmentasyonu

---

Bu projede, Watershed algoritması ile bir görüntü üzerinde kullanıcı tarafından işaretlenen bölgeler segmentlere ayrılır. Kullanıcı, farklı bölgeleri işaretleyerek segmentasyon işlemini interaktif olarak gerçekleştirir. Sonuçlar anlık olarak görselleştirilir.

## Watershed Nedir?
Watershed algoritması, görüntü segmentasyonu için kullanılan bir yöntemdir. Temel olarak, bir görüntüyü "topografik bir harita" gibi düşünür ve işaretlenen bölgelerden (marker) başlayarak, suyun yükselmesiyle farklı havzaların oluşmasını simüle eder. Her havza, farklı bir segmenti temsil eder ve sınırları otomatik olarak belirler. Bu yöntem, özellikle nesnelerin sınırlarının belirgin olmadığı durumlarda oldukça etkilidir.

---

### Kütüphanelerin Yüklenmesi
```python
import cv2
import numpy as np
from matplotlib import cm
```
- `cv2`: OpenCV kütüphanesi, görüntü işleme işlemleri için kullanılır.
- `numpy`: Sayısal işlemler ve matris işlemleri için kullanılır.
- `matplotlib.cm`: Renk haritaları (colormap) için kullanılır.

### Görüntünün Yüklenmesi ve Kopyalanması
```python
img = cv2.imread("landscape.jpg")
road_copy = img.copy()
```
- `img`: Segmentasyon yapılacak ana görüntü.
- `road_copy`: Kullanıcı işaretlemelerini göstermek için kullanılan kopya görüntü.

###  Marker ve Segment Matrislerinin Oluşturulması
```python
marker_img = np.zeros(img.shape[:2], dtype=np.int32)
segments = np.zeros(img.shape, dtype=np.uint8)
```
- `marker_img`: Her pikselin hangi marker'a ait olduğunu tutan matris.
- `segments`: Son segmentasyon sonucunu renkli olarak tutan matris.

###  Renklerin Oluşturulması
```python
def create_rgb(i):
    return tuple(np.array(cm.tab10(i)[:3])*255)

colors = []
for i in range(10):
    colors.append(create_rgb(i))
```
- `create_rgb(i)`: Her marker için farklı bir renk üretir.
- `colors`: 10 farklı marker için renklerin tutulduğu liste.

### Marker ve Kontrol Değişkenleri
```python
n_markers = 10 # 0-9 
current_marker = 1
marks_updated = False
```
- `n_markers`: Toplam marker (işaretleyici) sayısı.
- `current_marker`: Şu an seçili olan marker (kullanıcı tuşla değiştirir).
- `marks_updated`: Markerların güncellenip güncellenmediğini kontrol eder.

### Mouse Callback Fonksiyonu
```python
def mouse_callback(event,x,y,flags,params):
    global marks_updated

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(marker_img, (x,y), 10, current_marker, -1)
        cv2.circle(road_copy, (x,y),10, colors[current_marker], -1)
        marks_updated = True
```
- Kullanıcı görsel üzerinde tıkladığında, ilgili marker ve renk ile hem `marker_img` hem de `road_copy` üzerine daire çizilir.
- `marks_updated` True yapılır, böylece segmentasyonun güncellenmesi gerektiği anlaşılır.

### Pencere ve Mouse Callback Ayarları
```python
cv2.namedWindow('Road Image')
cv2.setMouseCallback('Road Image', mouse_callback)
```
- Görüntü penceresi oluşturulur ve mouse olayları için callback atanır.

### Ana Döngü 
```python
while True:
    # Segmentasyon ve işaretli görseli göster
    cv2.imshow('Watershed Segments', segments)
    cv2.imshow('Road Image', road_copy)

    # Kullanıcıdan tuş girişi bekle
    k = cv2.waitKey(0)

    # ESC tuşu ile çıkış
    if k == 27:
        break

    # 'c' tuşu ile ekranı temizle
    elif k == ord('c'):
        road_copy = img.copy()
        marker_img = np.zeros(img.shape[:2], dtype=np.int32)
        segments = np.zeros(img.shape, dtype=np.uint8)

    # 0-9 arası tuşlarla marker (renk) seçimi
    elif k > 0 and chr(k).isdigit():
        current_marker = int(chr(k))

    # Markerlar güncellendiyse segmentasyonu uygula
    if marks_updated:
        marker_img_copy = marker_img.copy()
        cv2.watershed(img, marker_img_copy)
        segments = np.zeros(img.shape, dtype=np.uint8)
        for color_ind in range(n_markers):
            segments[marker_img_copy==(color_ind)] = colors[color_ind]
```

- Döngü sürekli olarak iki pencereyi (segmentasyon sonucu ve işaretli görsel) ekranda tutar.
- Kullanıcıdan tuş girişi beklenir:
  - **ESC** ile çıkılır ve program sonlanır.
  - **'c'** ile tüm işaretlemeler ve segmentler sıfırlanır, kullanıcı yeni bir segmentasyon başlatabilir.
  - **0-9 arası tuşlarla** farklı marker (renk) seçilir, böylece farklı bölgeler farklı renklerle işaretlenebilir.
- Eğer kullanıcı yeni bir işaretleme yaptıysa (`marks_updated` True olduysa):
  - `marker_img`'in bir kopyası alınır ve Watershed algoritması bu kopya üzerinde çalıştırılır. Bu, orijinal marker bilgisinin korunmasını sağlar.
  - Watershed algoritması, işaretlenen bölgelerden başlayarak görüntüyü segmentlere ayırır. Her segment, kullanıcı tarafından atanmış marker numarasına göre renklendirilir.
  - Sonuçta, `segments` matrisinde her bölge farklı bir renkle gösterilir ve bu görsel anlık olarak ekranda güncellenir.
- Bu yapı sayesinde kullanıcı, segmentasyon işlemini adım adım ve görsel olarak takip edebilir, istediği zaman işaretlemeleri sıfırlayabilir veya farklı bölgeleri farklı renklerle işaretleyerek segmentasyonun doğruluğunu artırabilir.
- Döngü, kullanıcı çıkış yapana kadar (ESC) devam eder ve sonunda tüm pencereler kapatılır.

```python
cv2.destroyAllWindows()
```
- Tüm pencereler kapatılır ve program sonlanır.

---

Her adımda kodun ne yaptığı yukarıda açıklanmıştır. Proje, Watershed algoritmasının temel mantığını ve OpenCV ile interaktif segmentasyonun nasıl yapılacağını öğrenmek için iyi bir örnektir.

## Notebook Dosyası

Ayrıca bu klasörde, Watershed algoritmasının adım adım uygulanışını ve görselleştirilmesini sağlayan bir Jupyter Notebook dosyası da bulunmaktadır. Detaylı ve interaktif inceleme yapmak isteyenler aşağıdaki dosyaya göz atabilir:

[wateshed-custom.ipynb dosyasını görüntüle](./watershed-custom.ipynb)

---
