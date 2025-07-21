# Optik Akış ile Nesne Takibi (Optical Flow Object Tracking)
---
Bu klasörde, **optik akış** (optical flow) kavramını kullanarak nesne takibi yapmak için hazırlanmış örnek Python betikleri yer almaktadır. Dosyalar, optik akışın hem **seyrek (sparse)** hem de **yoğun (dense)** yaklaşımlarını içerecek şekilde düzenlenmiştir. Ayrıca köşe (corner) tespiti adımı da dâhil edilerek Lucas–Kanade metoduyla nokta takibi gerçekleştirilmektedir.


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
├── corner_detect.py      
├── lucas_kanade.py       
├── lk2.py                
├── optical_dense.py      
├── videos/               
└── README.md             
```

---

## Betik Açıklamaları

| Dosya | Ne Yapar? | Dosya Yolu |
|-------|-----------|---------|
| `corner_detect.py` | Seçilen ROI içindeki kontrastı yüksek köşeler arasından **tek bir güvenilir anahtar nokta** belirler ve daha sonraki takibe başlangıç noktası olarak kaydeder. |[**corner_detect.py**](./corner_detect.py)|
| `lucas_kanade.py` | Video dosyasında, başlangıç köşesini girdi alarak **Pyramidal Lucas–Kanade** algoritmasıyla noktanın kareler arasındaki hareketini izler ve izlenen güzergâhı çizer. | [**lucas_kanade.py**](./lucas_kanade.py)|
| `lk2.py` | Web kamerasından alınan canlı görüntüde, kullanıcı tarafından tıklanan herhangi bir pikseli Lucas–Kanade yöntemiyle takip eder; böylece **etkileşimli, gerçek-zamanlı** nokta takibi sunar. |[**lk2.py**](./lk2.py)|
| `optical_dense.py` | Ardışık kareler arasında **Farnebäck** yoğun optik akışını hesaplar ve tüm sahne hareketini HSV tabanlı renkli bir akış haritası olarak görselleştirir. | [**optical_dense.py**](./optical_dense.py) |

---


> ⚠️ **Not:** Video dosyalarının yolu kod dosyalarında sabittir. Kendi verinizi kullanmak için dosya adını veya yolu güncelleyin.



