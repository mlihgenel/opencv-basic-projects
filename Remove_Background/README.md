## Remove Background 
---
Bu projede verilen kivi resminde kivileri yapraklardan ayırıp sadece kiviler olacak şekilde maskelenip arkaplanın siyah yapılıp kivileri beyaz yapmaktır. 
<p align="center">
  <img src="../assest/kivi.jpg" width="300px">

Bunu yaparken maskeleme yontemi, hsv renk uzayı ile renk tespiti yapılıp contur bulunarak objeler arkaplandan ayrılmıştır. 

Program çalıştırıldığında bu sonuçları vermektedir; 

<p align="center">
  <img src="../assest/kivi_mask.png" width="300px">

</p>

Bu kısımda kiviler arkaplandan ayrılmış ve maskeleme işlemi gerçekleştirlmiştir ancak istenilen sonuç bu değildir.

<p align="center">
  <img src="../assest/kivi_last.png" width="300px">
</p>

Gerekli contur işlemleri ve morfolojik işlemler uygulandıktan sonra en çok bizden istenen çıktı. 


