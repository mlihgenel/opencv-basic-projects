# Image Segmentation 
---

Bu depo, bilgisayarlı görüde yaygın olarak kullanılan üç farklı görüntü segmentasyon algoritmasının (GrabCut, k-Means, Watershed) Python/OpenCV ile uygulanışını içermektedir. Her algoritma için ayrı bir klasör ve örnek görseller ile birlikte, adım adım açıklamalı kodlar ve detaylı dokümantasyon sunulmuştur.

## Klasörler ve İçerikleri

| Klasör                 | Açıklama                                                                 | GitHub Link |
|------------------------|--------------------------------------------------------------------------|-------------|
| **GrabCut Algortiması** | Etkileşimli segmentasyon için GrabCut algoritmasının uygulaması. Kullanıcı, fare ile nesnenin etrafına dikdörtgen çizer ve algoritma nesneyi arka plandan ayırır. | [GrabCut Algorithm](./GrabCut%20Algorithm/) |
| **k-Means Algortiması** | Renk tabanlı segmentasyon için k-Means kümeleme algoritmasının uygulaması. Piksel renklerine göre görüntü segmentlere ayrılır. | [k-Means Algorithm](./k-Means%20Algorithm) |
| **Watershed Algortiması/** | Marker tabanlı segmentasyon için Watershed algoritmasının uygulaması. Kullanıcı farklı bölgeleri işaretleyerek segmentasyon yapar. | [Watershed Algorithm](./Watershed%20Algorithm/) |

## Amaç
Bu depo, temel birkaç  segmentasyon algoritmalarının mantığını, uygulamasını ve aralarındaki farkları öğrenmek isteyenler için hazırlanmıştır. Her klasörde, ilgili algoritmanın teorik açıklamaları, kod örnekleri ve görsellerle desteklenmiş açıklamalar yer almaktadır.


## Gereksinimler
- Python 3.x
- OpenCV
- NumPy
- (Watershed için) Matplotlib

Her klasörün README dosyasında, o algoritmaya özel ek gereksinimler ve kullanım talimatları ayrıca belirtilmiştir.

---
