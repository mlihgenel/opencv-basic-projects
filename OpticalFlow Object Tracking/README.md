# Optik Akış ile Nesne Takibi (Optical Flow Object Tracking)

Bu klasörde, **optik akış** (optical flow) kavramını kullanarak nesne takibi yapmak için hazırlanmış örnek Python betikleri yer almaktadır. Dosyalar, optik akışın hem **seyrek (sparse)** hem de **yoğun (dense)** yaklaşımlarını içerecek şekilde düzenlenmiştir. Ayrıca köşe (corner) tespiti adımı da dâhil edilerek Lucas–Kanade metoduyla nokta takibi gerçekleştirilmektedir.

> 📚 **Ön bilgi**  
> Optik akış, ardışık iki kare arasındaki piksellerin **zaman içindeki yer değiştirme vektörünü** tahmin etmeye yarar. Bu vektör; görüntüdeki parlaklık, doku ve hareket yönü gibi bilgileri içerir ve nesnenin/hareketin yönü ile hızını çıkarımlamamıza olanak tanır.

---

## İçindekiler

1. [Teorik Arka Plan](#teorik-arka-plan)
2. [Klasör Yapısı](#klasör-yapısı)
3. [Betik Açıklamaları](#betik-açıklamaları)
4. [Nasıl Çalıştırılır?](#nasıl-çalıştırılır)
5. [Kaynaklar](#kaynaklar)

---

## Teorik Arka Plan

### 1. Seyrek Optik Akış (Sparse Optical Flow)

Seyrek yöntemlerde, yalnızca **seçili anahtar noktaların (keypoints)** hareketi izlenir. En popüler algoritma **Lucas–Kanade** tekniğidir. Bu yöntem, küçük görüntü yaması (patch) içerisindeki parlaklık değişimini lineer varsayarak, her nokta için en olası hareket vektörünü iteratif olarak çözer.

- Pyramidal Lucas–Kanade (OpenCV: `cv2.calcOpticalFlowPyrLK`)
- Avantaj: Hızlıdır, gerçek-zaman uygulamalarda yaygındır.
- Dezavantaj: Sadece takip edilen noktalar için bilgi verir; arka plandaki büyük hareketleri kaçırabilir.

### 2. Yoğun Optik Akış (Dense Optical Flow)

Yoğun yöntemlerde, **her piksel** için hareket vektörü hesaplanır. Bu, akış haritası (flow field) adı verilen bir görsel ile ifade edilir. Öne çıkan algoritmalardan biri **Farnebäck** yöntemidir.

- Farnebäck (OpenCV: `cv2.calcOpticalFlowFarneback`)
- Avantaj: Tüm sahnenin hareketini gösterir.
- Dezavantaj: Seyrek yönteme göre daha hesaplamalıdır.

### 3. Köşe Tespiti (Good Features to Track)

Lucas–Kanade öncesinde, takip edilecek sağlam noktaları seçmek için `cv2.goodFeaturesToTrack` fonksiyonu kullanılır. Bu fonksiyon, **Shi-Tomasi** veya **Harris** köşe ölçütlerine dayalı olarak kontrastı yüksek, tekrar algılanabilir köşeleri belirler.

---

## Klasör Yapısı

```text
OpticalFlow Object Tracking/
├── corner_detect.py      # ROI içinde köşe seçimi
├── lucas_kanade.py       # Seyrek optik akış (video dosyası)
├── lk2.py                # Seyrek optik akış (web kamerası)
├── optical_dense.py      # Yoğun optik akış (Farnebäck)
├── videos/               # Örnek video dosyaları
└── README.md             # Bu dosya
```

---

## Betik Açıklamaları

| Betik | Ne Yapar? |
|-------|-----------|
| `corner_detect.py` | Seçilen ROI içindeki kontrastı yüksek köşeler arasından **tek bir güvenilir anahtar nokta** belirler ve daha sonraki takibe başlangıç noktası olarak kaydeder. |
| `lucas_kanade.py` | Video dosyasında, başlangıç köşesini girdi alarak **Pyramidal Lucas–Kanade** algoritmasıyla noktanın kareler arasındaki hareketini izler ve izlenen güzergâhı çizer. |
| `lk2.py` | Web kamerasından alınan canlı görüntüde, kullanıcı tarafından tıklanan herhangi bir pikseli Lucas–Kanade yöntemiyle takip eder; böylece **etkileşimli, gerçek-zamanlı** nokta takibi sunar. |
| `optical_dense.py` | Ardışık kareler arasında **Farnebäck** yoğun optik akışını hesaplar ve tüm sahne hareketini HSV tabanlı renkli bir akış haritası olarak görselleştirir. |

---

<!-- detaylar kaldırıldı -->

Kullanıcının seçtiği ROI içindeki **tek** köşeyi tespit eder ve bu noktayı `numpy` dizisine (`p0`) kaydeder.

```python
roi = cv2.selectROI("ROI Secimi", frame)
points = cv2.goodFeaturesToTrack(first_gray, mask=None, **feature_params)
```

Çıktı olarak, ekranda ROI seçim penceresi açılır ve terminalde “Köşe noktası bulundu.” mesajı görülür.

---

### 2. `lucas_kanade.py`

`corner_detect.py` dosyasından aktarılan köşe noktası `p0` kullanılarak, **pyramidal Lucas–Kanade** algoritmasıyla tek nokta takibi yapılır.

Önemli kısımlar:

```python
p1, st, err = cv2.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
mask = cv2.line(mask, (a, b), (c, d), (0, 255, 0), 3)
```

Her yeni karede, eski ve yeni konum arasına çizgi çizilir. Böylece nesnenin izlediği yol görselleştirilir.

---

### 3. `lk2.py`

Gerçek-zamanlı kameradan görüntü alır. Kullanıcı, ekrana **mouse tıklayarak** takip edilecek noktayı seçer. Devamında `calcOpticalFlowPyrLK` ile noktanın hareketi canlı izlenir.

Ekstra özellikler:

- Fare ile nokta seçimi (`cv2.setMouseCallback`).
- Takip vektörlerini `mask` katmanında tutarak geçmiş hareketi gösterme.

---

### 4. `optical_dense.py`

**Farnebäck** algoritmasıyla tüm görüntü için yoğun optik akış hesaplar. HSV renk uzayını kullanarak akış vektörlerini görselleştirir.

```python
flow = cv2.calcOpticalFlowFarneback(prev, next, None,
                                    pyr_scale=0.5,
                                    levels=4,
                                    winsize=15,
                                    iterations=3,
                                    poly_n=5,
                                    poly_sigma=1.2,
                                    flags=0)
```

- Ton (Hue): Hareket yönü  
- Parlaklık (Value): Hız (büyüklük)

Sonuç, renkli bir ısı haritası olarak `cv2.imshow('frame', bgr)` ile gösterilir.

---


> ⚠️ **Not:** Video dosyalarının yolu (`video2.mp4`) betiklerde sabittir. Kendi verinizi kullanmak için dosya adını veya yolu güncelleyin.

---

