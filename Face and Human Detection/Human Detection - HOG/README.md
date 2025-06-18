# HOG (Histogram of Oriented Gradients) ile İnsan Tespiti
---
Bu proje, OpenCV kütüphanesi kullanılarak HOG (Histogram of Oriented Gradients) yöntemiyle insan tespiti yapan bir uygulamayı içerir. Projede hem fotoğraf hem de video üzerinde insan tespiti yapabilen iki farklı Python betiği bulunmaktadır.

## HOG (Histogram of Oriented Gradients) Algoritması Detaylı Açıklama

HOG, görüntüdeki nesneleri (özellikle insanları) tespit etmek için kullanılan bir özellik çıkarım yöntemidir. HOG'un temel amacı, bir görüntüdeki kenar, köşe ve doku gibi yapıları, yön bilgisiyle özetlemektir. HOG, özellikle yaya tespitinde endüstri standardı haline gelmiştir.

### HOG Nasıl Çalışır?

1. **Görüntü Ön İşleme**
   - Görüntü gri tonlamaya çevrilir ve gerekirse kontrast ayarı yapılır.

2. **Gradyan Hesaplama**
   - Her piksel için x ve y yönünde gradyanlar (kenar değişimleri) hesaplanır.
   - Bu, görüntüdeki ana yapısal değişiklikleri (kenarları) ortaya çıkarır.

3. **Hücrelere Bölme**
   - Görüntü, genellikle 8x8 piksellik küçük hücrelere ayrılır.

4. **Yön Histogramı Oluşturma**
   - Her hücredeki piksellerin gradyan yönleri, 0-180° arası belirli aralıklara (ör. 9 yön) bölünerek histogram haline getirilir.
   - Böylece her hücre, o bölgedeki kenarların hangi yönlerde yoğunlaştığını özetler.

5. **Blok Normalizasyonu**
   - Komşu hücreler bloklar halinde gruplanır (örn. 2x2 hücre).
   - Her bloktaki histogramlar normalize edilir. Bu, aydınlatma değişimlerine karşı dayanıklılık sağlar.

6. **Özellik Vektörü**
   - Tüm bloklardan elde edilen histogramlar birleştirilerek uzun bir özellik vektörü oluşturulur.

7. **Sınıflandırıcı Kullanımı**
   - Bu vektörler, genellikle bir SVM (Destek Vektör Makineleri) gibi bir makine öğrenmesi algoritmasına verilir.
   - OpenCV'de HOG + SVM kombinasyonu, insan tespiti için hazır olarak sunulur.

**Avantajları:**
- Kenar ve doku bilgisini yönlü olarak özetler.
- Aydınlatma ve poz değişimlerine karşı dayanıklıdır.
- Özellikle insan gibi dikey ve yatay kenarları bol nesnelerde çok etkilidir.

---

## Resimden ve Videodan İnsan Tespiti

Bu projede iki ana kullanım senaryosu vardır: bir görüntü (fotoğraf) üzerinden insan tespiti ve bir video (veya kamera akışı) üzerinden insan tespiti. Aşağıda her iki senaryonun kodu ve satır satır açıklamaları birlikte verilmiştir.

### 1. Resimden İnsan Tespiti

```python
import cv2

# HOG tanımlayıcıyı başlat ve SVM ile insan tespit modelini yükle
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Görüntüyü yükle ve yeniden boyutlandır
image = cv2.imread("people.jpg")
image = cv2.resize(image, (800, 500))

# Farklı tespit ayarlarını tanımla
ayarlar = [
    {"isim": "Hassas", "winStride": (2, 2), "padding": (16, 16)},
    {"isim": "Dengeli", "winStride": (8, 8), "padding": (8, 8)},
    {"isim": "Hizli", "winStride": (16, 16), "padding": (4, 4)}
]

# Her ayar için insan tespiti uygula ve sonucu göster
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
```

**Açıklamalar:**
- `cv2.HOGDescriptor()` ve `setSVMDetector()`: HOG + SVM ile insan tespiti için gerekli nesneleri başlatır.
- `cv2.imread()` ve `cv2.resize()`: Görüntüyü okur ve işlem hızını artırmak için boyutlandırır.
- `winStride`: Pencere kaydırma adımı. Küçük değer = daha hassas, büyük değer = daha hızlı.
- `padding`: Kenarlardaki insanları daha iyi bulmak için pencere etrafında boşluk bırakır.
- `scale`: Farklı boyutlardaki insanları yakalamak için görüntü ölçeklendirme faktörü.

### 2. Videodan İnsan Tespiti

```python
import cv2

# HOG tanımlayıcıyı başlat ve SVM ile insan tespit modelini yükle
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# Video dosyasını aç
cap = cv2.VideoCapture('people_walking.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break
    rects, _ = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )
    for (x, y, w, h) in rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    cv2.imshow('İnsan Tespit', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
```

**Açıklamalar:**
- `cv2.VideoCapture()`: Video dosyasını veya kamerayı açar.
- Döngüde her karede insan tespiti yapılır ve ekrana çizilir.
- Parametreler (winStride, padding, scale) gerçek zamanlı performans ve doğruluk için ayarlanabilir.

---

## Performans İpuçları ve Parametrelerin Etkisi

Aşağıda, HOG ile insan tespitinde sıkça karşılaşılan parametrelerin neyi, neden etkilediği detaylıca anlatılmıştır:

1. **winStride (Pencere Adımı)**
   - **Düşük değer** (örn. (2,2)): Daha hassas, daha fazla insan tespiti. Ancak işlem süresi uzar.
   - **Yüksek değer** (örn. (16,16)): Daha hızlı, ancak bazı insanları atlayabilir.
   - **Kullanım önerisi**: Gerçek zamanlı uygulamalarda (8,8) veya (16,16), statik analizde (2,2) veya (4,4).

2. **padding (Doldurma)**
   - **Yüksek padding**: Kenarlardaki insanları daha iyi bulur, ama işlem yükü artar.
   - **Düşük padding**: Daha hızlı çalışır, fakat kenarlarda tespit düşer.
   - **Kullanım önerisi**: (8,8) genellikle iyi bir denge sunar.

3. **scale (Ölçek Faktörü)**
   - **Küçük değer** (örn. 1.01): Farklı boyutlardaki insanları daha iyi yakalar, ama yavaşlar.
   - **Büyük değer** (örn. 1.1): Daha hızlı, fakat küçük nesneleri kaçırabilir.
   - **Kullanım önerisi**: 1.03 veya 1.05 çoğu durumda idealdir.

4. **Görüntü Boyutu**
   - Büyük görüntülerde işlem süresi uzar. Önce yeniden boyutlandırma yapmak (örn. 800x500) performansı ciddi şekilde artırır.

5. **Gerçek Zamanlı Video için**
   - Kare boyutunu küçültmek, `winStride` ve `scale` değerlerini artırmak FPS'i yükseltir.
   - Çok fazla yanlış pozitif çıkıyorsa, `hitThreshold` değerini artırabilirsiniz.

6. **Aydınlatma ve Kontrast**
   - HOG, aydınlatma değişimlerine karşı dayanıklı olsa da, çok karanlık veya çok parlak görüntülerde ön işleme (örn. histogram eşitleme) faydalı olabilir.

---



## Performans İpuçları (Detaylı Açıklama)

Aşağıda HOG ile insan tespitinde en çok kullanılan parametrelerin performans ve doğruluk üzerindeki etkileri detaylı biçimde açıklanmıştır. Her bir ayarın avantajları, dezavantajları ve hangi senaryoda ne kullanılır örneklerle belirtilmiştir.

### 1. `winStride` (Tarama Penceresi Adımı)
- **Düşük Değerler (ör. (2,2), (4,4))**
  - Avantaj: Daha hassas tarama, küçük ve yakın nesneleri daha iyi bulur.
  - Dezavantaj: Çok daha yavaş çalışır, işlem süresi artar.
  - Kullanım: Statik görüntü analizi, yüksek doğruluk istenen durumlar.
- **Yüksek Değerler (ör. (8,8), (16,16))**
  - Avantaj: Çok daha hızlı çalışır, gerçek zamanlı uygulamalar için uygundur.
  - Dezavantaj: Küçük veya kenardaki insanları atlayabilir.
  - Kullanım: Canlı video, webcam, düşük donanımda hızlı sonuç istenen durumlar.

### 2. `padding` (Doldurma)
- **Düşük Değerler (ör. (4,4))**
  - Avantaj: Daha hızlı çalışır, işlem yükü azalır.
  - Dezavantaj: Görüntü kenarındaki insanları kaçırma ihtimali artar.
- **Yüksek Değerler (ör. (16,16))**
  - Avantaj: Kenarlardaki insanları daha iyi tespit eder.
  - Dezavantaj: Hesaplama maliyeti artar, hız düşer.
  - Kullanım: Kalabalık ve kenarları dolu görüntülerde önerilir.

### 3. `scale` (Görüntü Piramidi Ölçek Faktörü)
- **Küçük Değerler (örn. 1.01, 1.03)**
  - Avantaj: Farklı boyutlardaki insanları daha iyi yakalar (ör. hem yakın hem uzak).
  - Dezavantaj: Çok yavaş çalışır, özellikle videoda FPS düşer.
  - Kullanım: Yüksek doğruluk gerektiren, hızın önemli olmadığı durumlar.
- **Büyük Değerler (örn. 1.08, 1.1)**
  - Avantaj: Çok daha hızlı çalışır.
  - Dezavantaj: Küçük veya uzaktaki insanları kaçırabilir.
  - Kullanım: Gerçek zamanlı video, düşük çözünürlüklü görüntüler.
### 4. `hitThreshold` (Eşik Değeri)
- **Varsayılan (0)**
  - Çoğu durumda yeterli.
- **Yüksek Değerler (örn. 1, 2)**
  - Avantaj: Yanlış pozitifleri azaltır (insan olmayan şeylerin insan olarak algılanmasını önler).
  - Dezavantaj: Gerçek insanları da kaçırabilir.
  - Kullanım: Çok fazla yanlış tespit varsa artırılabilir.

### 5. Görüntü Boyutu
- **Büyük Görüntüler**
  - Avantaj: Detay kaybı olmaz.
  - Dezavantaj: İşlem süresi çok uzar.
- **Küçük/Orta Boyutlu Görüntüler (örn. 800x500)**
  - Avantaj: Çok daha hızlı sonuç.
  - Dezavantaj: Çok küçük insanlar kaybolabilir.
  - Kullanım: Video ve gerçek zamanlı uygulamalarda mutlaka yeniden boyutlandırma önerilir.


### 6. Kare Boyutu (Video için)
- **Küçük Kareler**
  - Avantaj: FPS ciddi şekilde artar.
  - Dezavantaj: Küçük detaylar kaybolabilir.
- **Büyük Kareler**
  - Avantaj: Daha detaylı tespit.
  - Dezavantaj: FPS düşer.

### 7. Aydınlatma ve Kontrast
- **Kötü Aydınlatma**
  - Histogram eşitleme veya kontrast artırıcı ön işlemler, HOG'un başarısını artırır.

---

#### Özet Tablo
| Amaç                 | winStride | padding | scale | Kare Boyutu | hitThreshold |
|----------------------|-----------|---------|-------|-------------|--------------|
| Maksimum Hız         | (16,16)   | (4,4)   | 1.08  | Küçük       | 0            |
| Maksimum Doğruluk   | (2,2)     | (16,16) | 1.01  | Orta/Büyük  | 0 veya <1    |
| Dengeli (Genel)      | (8,8)     | (8,8)   | 1.05  | Orta        | 0            |

Her zaman, kendi veri setiniz ve donanımınızda bu parametrelerle denemeler yaparak en iyi sonucu bulmanız önerilir.
#