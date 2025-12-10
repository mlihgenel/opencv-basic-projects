
# K-Means Algoritması: Temelleri ve Görüntü Segmentasyonunda Rolü

## 📌 K-Means Algoritmasının Teorik Temelleri

### ➤ Kümeleme ve Gözetimsiz Öğrenme

K-Means, *kümeleme (clustering)* adı verilen ve verileri doğal benzerliklerine göre gruplama temeline dayanan bir makine öğrenmesi yöntemidir. *Gözetimsiz öğrenme (unsupervised learning)* kategorisine girer, yani algoritmanın çalışması için önceden etiketlenmiş örnekler gerekmez; model, verideki gizli kalıpları ve grupları kendi kendine keşfeder.

### ➤ Amaç ve Matematiksel Temel

K-Means, her veri noktasını en yakın küme merkezine atayarak, kümelerin içindeki benzerliği en üst düzeye çıkarmayı hedefler. Bu amaçla, veri noktaları ile ait oldukları küme merkezi arasındaki uzaklıkların karelerinin toplamını **minimize** eder.

---

## ⚙️ K-Means Algoritması Nasıl Çalışır?

1. **Küme Sayısını Belirle (k):** Kaç tane küme oluşturulacağı seçilir.
2. **Rastgele Başlangıç Merkezleri Belirle:** k adet başlangıç merkezi rastgele seçilir.
3. **Her Veri Noktasını En Yakın Merkeze Ata:** Öklid uzaklığı gibi ölçütlerle.
4. **Yeni Küme Merkezlerini Hesapla:** Her küme için ortalama alınır.
5. **Adımları Tekrarla:** Küme atamaları değişmeyene kadar.

---

## 🎯 K-Means Algoritmasının Özellikleri

- ✅ Basit ve hızlı çalışır.
- ✅ Gözetimsiz olduğu için etiket gerekmez.
- ✅ Büyük veri setlerinde verimli.
- ⚠️ k değeri kullanıcı tarafından belirlenmelidir.
- ⚠️ Başlangıç merkezlerine duyarlıdır.
- ⚠️ Küresel değil, yerel optimum bulabilir.
- ✅ K-Means++ gibi iyileştirmeler mevcuttur.

---

## 🖼️ Bilgisayarlı Görüde K-Means Kullanımı

K-Means, bilgisayarlı görüde yaygın olarak kullanılır:

- 🎨 **Renk Kümeleme (Color Quantization)**
- 🧩 **Görüntü Segmentasyonu**
- 🧠 Tıbbi görüntülerde bölgeleme
- 🛰️ Uydu görüntülerinde sınıflandırma
- 🚗 Otonom araçlarda sahne analizi

---

## 🔍 Görüntü Segmentasyonu Nedir?

Segmentasyon, bir görüntünün benzer piksellerden oluşan bölgelere ayrılmasıdır. Bu işlem:

- Görüntüyü anlamlı parçalara ayırır.
- Nesne tanıma öncesi önişlemedir.
- Arka plan ve nesne ayrımı yapar.

---

## 🧠 K-Means ile Görüntü Segmentasyonu: Adım Adım

1. **Piksel Özelliklerini Belirle:** (Örn: RGB)
2. **Küme Sayısını Seç (k):** Örn: k=2 → çiçek ve yaprak
3. **Başlangıç Merkezlerini Ata**
4. **Pikselleri En Yakın Merkeze Ata**
5. **Her Kümenin Ortalamasını Al → Yeni merkez**
6. **İterasyonları Tekrarla**

---

## ✅ Avantajları

- ✔️ Uygulaması kolay
- ✔️ Etiket gerektirmez
- ✔️ Hızlıdır
- ✔️ Farklı segment sayıları denenebilir

---

## ⚠️ Kısıtları

- ❗ k değeri seçimi zordur
- ❗ Başlangıç merkezine duyarlıdır
- ❗ Yalnızca renk gibi basit özelliklere dayanır
- ❗ Benzer renkte ama farklı nesneleri ayırt edemez
- ❗ Konumsal bilgi kullanılmazsa segmentler dağılabilir

---

## 🎓 Sonuç

K-Means, görüntü segmentasyonunda sık kullanılan, anlaşılması kolay bir algoritmadır. Özellikle renk bazlı ayrım yapmak için idealdir. Modern derin öğrenme yöntemlerinin yerini tutmasa da öğrenme ve prototipleme açısından değerlidir.
