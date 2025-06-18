# Haar Cascade ile Yüz Tespiti
---
Bu proje, OpenCV kütüphanesi kullanılarak Haar Cascade yöntemiyle yüz tespiti yapan bir uygulamayı içerir. Projede video üzerinde gerçek zamanlı yüz tespiti yapan bir Python betiği ve gerekli model dosyaları bulunmaktadır.

## Haar Cascade Algoritması 

Haar Cascade, Viola-Jones algoritması olarak da bilinen ve özellikle yüz tespitinde uzun yıllardır kullanılan, hızlı ve pratik bir görüntü işleme tekniğidir. Temel olarak, görüntüdeki belirli desenleri (göz, burun, ağız gibi) hızlıca kontrol eden, çok sayıda basit sınıflandırıcıyı zincirleme olarak kullanan bir yapıdır.

**Temel Mantık:**
- Görüntü gri tona çevrilir.
- Farklı boyut ve konumlardaki bölgelerde, Haar özellikleri ile yüz olasılığı hesaplanır.
- Cascade (basamaklı) yapı sayesinde, yüz olmayan bölgeler hızlıca elenir, kalan bölgelerde detaylı analiz yapılır.
- Sonuç olarak, yüz olarak tespit edilen bölgeler işaretlenir.

**Avantajları:**
- Gerçek zamanlı ve çok hızlı çalışır.
- Düşük donanımda bile rahatlıkla kullanılabilir.
- Eğitimli modellerle farklı nesneler de tespit edilebilir.

**Dezavantajları:**
- Kötü ışık, açı ve karmaşık arka planda başarı oranı düşer.
- Modern derin öğrenme yöntemlerine göre daha fazla yanlış pozitif/negatif üretebilir.

**Pratik Notlar:**
- Yüz tespiti için genellikle cepheden bakışa uygun modeller kullanılır.
- Küçük yüzler ve farklı açılar için özel modeller gerekebilir.
- İyi aydınlatılmış, net görüntülerde en iyi sonucu verir.

---


https://github.com/user-attachments/assets/0e7cd32f-d712-47d8-9247-1633386c5158


---

## Yüz Tespiti Uygulaması

Aşağıda, projedeki ana Python betiği ve satır satır açıklamaları yer almaktadır.

```python
import cv2

# Haar Cascade modelini yükle
face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt2.xml')

# Video dosyasını aç
cap = cv2.VideoCapture('sample_video.mp4')

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Görüntüyü gri tona çevir
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Yüzleri tespit et
    face_rects = face_cascade.detectMultiScale(
        gray, 
        scaleFactor=1.2, 
        minNeighbors=5
    )

    # Tespit edilen yüzlerin etrafına dikdörtgen çiz
    for (x, y, w, h) in face_rects:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Kamera", frame)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
```

**Açıklamalar:**
- `cv2.CascadeClassifier()`: Haar Cascade modelini yükler. Model dosyasının yolu doğrudan verilmiştir.
- `cv2.VideoCapture()`: Video dosyasını veya kamerayı açar.
- `cv2.cvtColor()`: Renkli görüntüyü gri tona çevirir (Haar Cascade gri tonlu görüntüyle çalışır).
- `detectMultiScale()`: Görüntüdeki yüzleri tespit eder.
  - `scaleFactor`: Her tespit adımında görüntünün ne kadar küçültüleceğini belirler. Küçük değerler daha hassas, büyük değerler daha hızlıdır.
  - `minNeighbors`: Bir bölgenin yüz olarak kabul edilmesi için gerekli minimum komşu dikdörtgen sayısı. Yüksek değer yanlış pozitifleri azaltır.
- Döngüde her karede yüzler tespit edilip ekrana çizilir. `q` tuşuna basınca uygulama kapanır.

---

## Performans ve Parametre İpuçları (Detaylı)

### 1. `scaleFactor`
- **Küçük Değerler (örn. 1.05, 1.1):**
  - Avantaj: Daha hassas, küçük yüzleri de bulur.
  - Dezavantaj: Daha yavaş çalışır.
  - Kullanım: Yüksek doğruluk istenen, hızın çok önemli olmadığı durumlar.
- **Büyük Değerler (örn. 1.2, 1.3):**
  - Avantaj: Daha hızlı çalışır.
  - Dezavantaj: Küçük yüzleri atlayabilir.
  - Kullanım: Gerçek zamanlı video, hızlı sonuç gereken durumlar.

### 2. `minNeighbors`
- **Düşük Değerler (örn. 3):**
  - Avantaj: Daha fazla yüz tespiti (bazı yanlış pozitifler dahil).
  - Dezavantaj: Yanlış pozitif (yüz olmayan bölgeler) artar.
- **Yüksek Değerler (örn. 6, 7):**
  - Avantaj: Yanlış pozitifler azalır.
  - Dezavantaj: Gerçek yüzlerin bazılarını kaçırabilir.
  - Kullanım: Arka planı karmaşık görüntülerde artırmak faydalı olabilir.

### 3. Görüntü Boyutu
- **Küçük boyutlar:** Daha hızlı işlem, düşük doğruluk.
- **Büyük boyutlar:** Daha hassas tespit, yavaş işlem.

### 4. Aydınlatma ve Kontrast
- Yüz tespitinde başarı için iyi aydınlatılmış ve net görüntüler önerilir.
- Gerekirse histogram eşitleme gibi ön işlemler uygulanabilir.

#### Özet Tablo

| Amaç                 | scaleFactor | minNeighbors | Kare Boyutu |
|----------------------|-------------|-------------|-------------|
| Maksimum Hız         | 1.3         | 3           | Küçük       |
| Maksimum Doğruluk    | 1.05        | 6           | Orta/Büyük  |
| Dengeli (Genel)      | 1.2         | 5           | Orta        |

---

## Sonuç

Bu proje, Haar Cascade tabanlı yüz tespitinin temelini ve parametrelerin performansa etkisini uygulamalı olarak göstermektedir. Farklı parametrelerle denemeler yaparak kendi veri setiniz ve donanımınız için en iyi ayarları bulabilirsiniz. Daha gelişmiş ve karmaşık senaryolar için derin öğrenme tabanlı yöntemler de değerlendirilebilir.
