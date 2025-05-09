import cv2
import matplotlib.pyplot as plt

#----------------------------------------
def display(img, cmap = "gray"):
    plt.figure(figsize=(12,10))
    plt.imshow(img, cmap)
    plt.show()
#----------------------------------------

# içinde arayacağımız resmi okuyoruz
cheerios = cv2.imread('Feature_Matching/assets/cheerios.png',0) 
# sadece plot edilirken daha güzel gözükmesi için boyutları ayarlıyoruz
cheerios = cv2.resize(cheerios, (550, 550), interpolation=cv2.INTER_AREA)
# ana resmimizi okuyoruz, cheerios resmini bu resimde arayacağız
cereals = cv2.imread('Feature_Matching/assets/many_cereals.jpg',0)

# --------- KNN Matching with SIFT Algorithm --------- # 

# sift nesnesini oluşturuyoruz
sift = cv2.SIFT_create()
# sırası ile iki resmimizde de keypoint ve descriptionları buluyoruz
kp1, des1 = sift.detectAndCompute(cheerios, mask=None)
kp2, des2 = sift.detectAndCompute(cereals, mask=None)

# BFMatcher nesnesi oluşturuyoruz
bf = cv2.BFMatcher()
# knnMatch için bf nesnesini kullanıyoruz
matches = bf.knnMatch(des1, des2, k = 2)

# iyi eşleşmeleri tutmak için liste
goodMatch = []
# less distance == better match

for match1, match2 in matches:
    # match1 uzaklığı, match2 uzaklığının %75'inden düşükse iyi eşleşme demektir
    if match1.distance < 0.75*match2.distance:
        goodMatch.append([match1]) # bu eşleşmeleri listemize ekliyoruz
        
# len(matches), len(goodMatch)
# (1502, 78)
# 1502 olan eşleşme sayısını 78 e düşürmüş olduk. Yani elimizde iyi 78 eşleşme var.
# bu sayıyı koyduğumuz sınıra göre değiştirebiliriz. (burada %75 olarak tanımladık). 

# eşleştirmeleri çiziyoruz
knn_matches = cv2.drawMatchesKnn(cheerios, kp1, cereals, kp2, goodMatch, None, flags=2)

display(knn_matches)


