# GrabCut ile Görüntü Segmentasyonu

---

Bu projede, bilgisayarlı görüde sıkça kullanılan GrabCut algoritması ile bir görüntüdeki nesneyi arka plandan ayırma işlemi gerçekleştirilir. GrabCut, özellikle karmaşık arka planlara sahip görüntülerde, kullanıcıdan alınan minimum etkileşimle (örneğin sadece bir dikdörtgen çizimiyle) nesne segmentasyonu yapabilen, güçlü ve modern bir algoritmadır. Temel olarak, kullanıcının fareyle nesnenin etrafına çizdiği bir dikdörtgeni başlangıç noktası olarak alır ve bu alan içindeki nesneyi, arka plandan otomatik olarak ayırır. Bu işlem sırasında renk dağılımlarını modellemek için Gaussian Karışım Modelleri (GMM) ve pikseller arası ilişkiyi değerlendirmek için Markov Rastgele Alanları (MRF) kullanılır. Sonuç olarak, kullanıcıya hızlı ve etkili bir segmentasyon deneyimi sunar.

## GrabCut Nedir?
GrabCut algoritması, etkileşimli görüntü segmentasyonu için geliştirilmiş bir yöntemdir. Temel olarak, kullanıcıdan alınan bir dikdörtgen ile ön plan ve arka plan piksellerini ayırır. Markov Rastgele Alanları (MRF) ve Gaussian Karışım Modelleri (GMM) kullanarak, nesne ve arka planı yinelemeli olarak modelleyip en iyi ayrımı bulur. Özellikle arka planın karmaşık olduğu durumlarda başarılı sonuçlar verir.

---

### Kütüphanelerin Yüklenmesi
```python
import cv2
import numpy as np
```
- `cv2`: OpenCV kütüphanesi, görüntü işleme işlemleri için kullanılır.
- `numpy`: Sayısal işlemler ve matris işlemleri için kullanılır.

### Görüntünün Yüklenmesi ve Kopyalanması
```python
img = cv2.imread("bird.jpg")
img_copy = img.copy()
```
- `img`: Segmentasyon yapılacak ana görüntü.
- `img_copy`: Kullanıcı dikdörtgenini göstermek için kullanılan kopya görüntü.

### Maske ve Model Matrislerinin Oluşturulması
```python
mask = np.zeros(img.shape[:2], np.uint8)
bgModel = np.zeros((1, 65), np.float64)
fgModel = np.zeros((1, 65), np.float64)
```
- `mask`: Her pikselin ön plan/arka plan durumunu tutan matris.
- `bgModel` ve `fgModel`: Arka plan ve ön plan için GMM parametrelerini tutar.

### Mouse Callback Fonksiyonu
```python
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
```
- Kullanıcı, fare ile görüntü üzerinde bir dikdörtgen çizer. 
- **cv2.EVENT_LBUTTONDOWN**: Sol fare tuşuna basıldığında çizim başlar ve başlangıç koordinatları kaydedilir.
- **cv2.EVENT_MOUSEMOVE**: Fare hareket ettikçe, geçici olarak dikdörtgen ekranda gösterilir (kullanıcıya görsel geri bildirim sağlar).
- **cv2.EVENT_LBUTTONUP**: Sol tuş bırakıldığında çizim tamamlanır, dikdörtgenin koordinatları kaydedilir ve segmentasyon için hazır hale gelir.
- Bu yapı sayesinde kullanıcı, segmentasyon için nesnenin etrafını kolayca seçebilir ve algoritmanın çalışmasını başlatabilir.

### Pencere ve Mouse Callback Ayarları
```python
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", draw_rectangle)
```
- Görüntü penceresi oluşturulur ve mouse olayları için callback atanır.

### Ana Döngü ve Segmentasyon
```python
while True:
    cv2.imshow("Image", img_copy)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('g') and rect_or_drawn:
        cv2.grabCut(img, mask, rect, bgModel, fgModel, 5, cv2.GC_INIT_WITH_RECT)
        output_mask = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        segmented = img * output_mask[:, :, np.newaxis]
        cv2.imshow("Segmented", segmented)
    elif key == 27:
        break
cv2.destroyAllWindows()
```
- Kullanıcı 'g' tuşuna bastığında GrabCut algoritması çalışır ve segmentasyon sonucu ekranda gösterilir.
- ESC ile çıkılır ve tüm pencereler kapanır.

---

Her adımda kodun ne yaptığı yukarıda açıklanmıştır. Proje, GrabCut algoritmasının temel mantığını ve OpenCV ile etkileşimli segmentasyonun nasıl yapılacağını öğrenmek için iyi bir örnektir.


