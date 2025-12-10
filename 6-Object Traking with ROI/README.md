# Nesne Takip API'si (Object Tracking API)
---

## Proje Genel Bakış
Bu projede manuel olarak videodan seçilen ROI ile birlikte nesne takibi yapılmaktadır. İki farklı algoritma kullanılmıştır. Bunlar **MIL (Multiple Instance Learning) Tracker** ve **KCF (Kernelized Correlation Filter) Tracker** takip algoritmalarıdır. BU projede takip edilecek nesne tamamen kullanıcıya bağlıdır ve ROI yani (Region of Interest) kullanıcı tarafından belirlenmektedir. 

https://github.com/user-attachments/assets/514912c3-0ca7-4f62-89e9-b5507b70681f

Bu video örnek olarak KFC Algoritması ile ROI seçerek nesne takibini gösterir.  

## Proje Modülleri ve Detaylı Açıklamaları

### Takip Algoritması Seçim Fonksiyonu
```python
def ask_for_tracking_api():
    print('Which Tracker API do you wanna use?')
    print('1 - MIL Tracker')
    print('2 - KCF Tracker')

    choice = int(input('Please select your tracker : '))

    if choice == 1:
        tracker = cv2.TrackerMIL_create()
        return tracker
    elif choice == 2:
        tracker = cv2.TrackerKCF_create()
        return tracker
    else:
        print('Invalid choice. Closing...')
        quit()
```
- Kullanıcıya iki farklı nesne takip algoritması seçeneği sunar.
- Kullanıcının tercihini alır ve buna göre ilgili OpenCV takip nesnesini oluşturur.
- Geçersiz bir seçim yapıldığında programı sonlandırır.

### Takip Algoritmaları 

#### 1. MIL (Multiple Instance Learning) Tracker
- **Çalışma Prensibi:** Bu algoritma, takip edilen nesneyi tek bir birim olarak görmek yerine, etrafındaki birden fazla noktayı (örnekleri) analiz eder. Nesnenin kısmen engellendiği veya görünümünün hafifçe değiştiği durumlarda bile takibi sürdürme yeteneği ile bilinir.
- **Avantajları:**
  - **Kısmi Engellemelere Karşı Dayanıklılık:** Nesnenin bir kısmı başka bir nesnenin arkasında kalsa bile takibi kaybetme olasılığı daha düşüktür.
- **Dezavantajları:**
  - **Daha Yavaş Performans:** KCF'ye göre daha fazla hesaplama gerektirdiği için daha yavaştır.
  - **Hata Kurtarma:** Bir kez takibi kaybettiğinde, doğru nesneyi tekrar bulması zor olabilir.

#### 2. KCF (Kernelized Correlation Filter) Tracker
- **Çalışma Prensibi:** Bu algoritma, nesnenin bir önceki karedeki görünümünü kullanarak bir sonraki karedeki konumunu tahmin eder. Bunu, iki görüntü bölgesi arasındaki "korelasyonu" (benzerliği) bularak yapar. Yüksek hızı ve verimliliği ile öne çıkar.
- **Avantajları:**
  - **Yüksek Hız:** Çok hızlı çalışır ve daha az işlem gücü gerektirir, bu da onu gerçek zamanlı uygulamalar için ideal kılar.
  - **Genel Performans:** Genellikle stabil ve güvenilir sonuçlar verir.
- **Dezavantajları:**
  - **Engellemelere Karşı Hassasiyet:** Nesne tamamen engellendiğinde veya çok hızlı bir şekilde şekil değiştirdiğinde takibi kolayca kaybedebilir.

### Takip Algoritması ve Video (Kamera) Ayarları
```python
tracker = ask_for_tracking_api()
tracker_name = str(tracker).split()[1].split('.')[1]

cap = cv2.VideoCapture('sample_video.mp4')
tracking = False  

```
- `tracker`: Kullanıcının seçtiği takip algoritmasını depolar
- `tracker_name`: Takip algoritmasının adını çıkarır (ekranda gösterilmek üzere)
- `cap = cv2.VideoCapture('sample_video.mp4')`: Dosyada bulunan videoyu okur. Eğer aynı dosyada değilse tam yolu verilmelidir.
  - Eğer `cv2.VideoCapture(0)` olur ise bu bilgisayardaki kamerayı açar. Video üzerinde değil kamera üzerinden işlem yapmış oluruz. 
  - Birden fazla kamera varsa, indeks değiştirilebilir, (0,1,2) gibi.
- `tracking = False`: Takip durumunu kontrol eden değişken

### Ana Döngü ve Takip Mantığı
```python
while True:
    # Videodan anlık bir kare (frame) okunur.
    ret, frame = cap.read()
    # Eğer kare okunamadıysa (video sonu veya kamera hatası), döngüden çıkılır.
    if not ret:
        break

    # 'tracking' değişkeni True ise, yani bir nesne takip ediliyorsa:
    if tracking:
        # Takipçiye yeni kare verilir ve nesnenin yeni konumu (roi) istenir.
        success, roi = tracker.update(frame)
        # roi koordinatları tam sayıya dönüştürülür.
        (x, y, w, h) = tuple(map(int, roi))

        # Takip başarılıysa:
        if success:
            # Nesnenin etrafına yeşil bir dikdörtgen çizilir.
            p1 = (x, y)
            p2 = (x + w, y + h)
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 2)

            # Ekrana kullanılan takip algoritmasının adı yazılır.
            cv2.putText(frame, tracker_name, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        # Takip başarısızsa:
        else:
            # Ekrana kırmızı renkte "Tracking Failure" yazısı yazılır.
            cv2.putText(frame, "Tracking Failure", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Henüz bir nesne seçilmediyse:
    else:
        # Kullanıcıya nesne seçmesi için talimatlar verilir.
        cv2.putText(frame, "Press 's' to select ROI", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        cv2.putText(frame, "After select ROI press Enter button", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

    # İşlenmiş kare "Tracking" adlı pencerede gösterilir.
    cv2.imshow("Tracking", frame)

    # 1 milisaniye boyunca klavyeden bir tuşa basılması beklenir.
    key = cv2.waitKey(1) & 0xFF

    # Eğer 's' tuşuna basıldıysa ve takip başlamadıysa:
    if key == ord('s') and not tracking:
        # Kullanıcının bir ROI (Region of Interest - İlgi Alanı) seçmesi için pencere açılır.
        roi = cv2.selectROI("Tracking", frame, fromCenter=False, showCrosshair=False)
        # Seçilen ROI ile takipçi başlatılır.
        tracker.init(frame, roi)
        # Takip bayrağı True olarak ayarlanır.
        tracking = True

    # Eğer 'q' tuşuna basıldıysa, döngüden çıkılır. Program biter. 
    elif key == ord('q'): 
        break
```
1.  **Sonsuz Döngü (`while True`):** Program, kullanıcı `ESC` tuşuna basana kadar sürekli çalışır.
2.  **Kare Okuma (`cap.read()`):** Her döngü adımında, videodan ya da kameradan o anki görüntü bir "kare" (frame) olarak alınır. `ret` değişkeni, karenin başarılı okunup okunmadığını belirtir.
3.  **Takip Durumu Kontrolü (`if tracking`):**
    *   Eğer `tracking` değişkeni `True` ise (yani kullanıcı 's' tuşuna basıp bir nesne seçtiyse), program `tracker.update(frame)` komutuyla nesnenin yeni konumunu bulmaya çalışır.
    *   `success` değişkeni, takibin o karede başarılı olup olmadığını söyler.
    *   **Başarılıysa:** Nesnenin etrafına yeşil bir kutu çizilir ve ekrana takipçi adı yazılır.
    *   **Başarısızsa:** Ekrana kırmızı bir "Tracking Failure" uyarısı verilir.
4.  **Başlangıç Durumu (`else`):**
    *   Eğer `tracking` `False` ise, ekrana kullanıcıyı yönlendiren "Press 's' to select ROI" gibi bilgilendirme metinleri yazdırılır.
5.  **Görüntüyü Ekranda Gösterme (`cv2.imshow()`):** İşlenen (üzerine yazı yazılmış veya kutu çizilmiş) kare, bir pencerede kullanıcıya gösterilir.
6.  **Klavye Dinleme (`cv2.waitKey()`):** Program, çok kısa bir süre (1ms) klavyeden bir tuşa basılmasını bekler. Bu, hem görüntünün ekranda kalmasını sağlar hem de kullanıcı girdisini yakalar.
7.  **ROI Seçimini Başlatma (`if key == ord('s')`):**
    *   Kullanıcı 's' tuşuna basarsa, `cv2.selectROI` fonksiyonu devreye girer. Bu fonksiyon, ekranı durdurur ve kullanıcının fare ile bir dikdörtgen çizmesine olanak tanır.
    *   Kullanıcı `Enter`'a bastığında, seçilen alan (`roi`) ile `tracker.init(frame, roi)` komutu çalıştırılır. Bu, takipçiye "işte bu nesneyi takip edeceksin" demek anlamına gelir.
    *   Son olarak, `tracking` bayrağı `True` yapılır ve döngünün bir sonraki adımından itibaren takip başlar.
8.  **Programdan Çıkış (`elif key == ord('q')`):** Kullanıcı `Q` tuşuna basarsa, `break` komutu ile `while` döngüsü sonlandırılır ve program biter.

### Sonlandırma
```python
cap.release()
cv2.destroyAllWindows()
```
- Kamera bağlantısını kapatır
- Tüm OpenCV pencerelerini kapatır

