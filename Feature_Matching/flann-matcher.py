import cv2
import matplotlib.pyplot as plt

#----------------------------------------
def display(img, cmap = "gray"):
    plt.figure(figsize=(16,12))
    plt.imshow(img, cmap)
    plt.show()
#----------------------------------------

# içinde arayacağımız resmi okuyoruz
cheerios = cv2.imread('Feature_Matching/cheerios.png',0) 
# sadece plot edilirken daha güzel gözükmesi için boyutları ayarlıyoruz
cheerios = cv2.resize(cheerios, (550, 550), interpolation=cv2.INTER_AREA)
# ana resmimizi okuyoruz, cheerios resmini bu resimde arayacağız
cereals = cv2.imread('Feature_Matching/many_cereals.jpg',0)

# --------- FLANN Matching with SIFT Algorithm --------- # 

# sift nesnesini oluşturuyoruz
sift = cv2.SIFT_create()
# sırası ile iki resmimizde de keypoint ve descriptionları buluyoruz
kp1, des1 = sift.detectAndCompute(cheerios, mask=None)
kp2, des2 = sift.detectAndCompute(cereals, mask=None)

# FLANN'ın hangi algoritmasyı kullanacağını belirliyoruz. 
# 0 değeri KD-Tree (k-dimensional tree) algoritmasını kullanacağını belirtir.  
FLANN_INDEX_KDTREE = 0  

# FLANN  için parametreleri belirliyoruz. 
# KDTREE algoritması, 5 ağaç kullanılacak şekilde.
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
# karşılaştırma sayısını belirliyoruz 
search_params = dict(checks = 50)

# FLANN nesnesini oluşturuyoruz.
flann = cv2.FlannBasedMatcher(index_params, search_params)

# eşleştirmeleri yapıyoruz
matches = flann.knnMatch(des1, des2, k = 2)

# iyi eşleşmeleri tutmak için liste
goodMatch = []
# less distance == better match

for match1, match2 in matches:
    # match1 uzaklığı, match2 uzaklığının %75'inden düşükse iyi eşleşme demektir
    if match1.distance < 0.75*match2.distance:
        goodMatch.append([match1]) # bu eşleşmeleri listemize ekliyoruz

# len(matches), len(goodMatch)
# (1417, 34)
# 1417 olan eşleşme sayısını 34 e düşürmüş olduk. Yani elimizde iyi 34 eşleşme var.

# eşleştirmeleri çiziyoruz
flann_matchess = cv2.drawMatchesKnn(cheerios, kp1, cereals, kp2, goodMatch, None, flags = 0)

display(flann_matchess)


# daha iyi görmek için iyi eşleşmeleri ayırıyoruz.
# iyi eşleşmeleri mavi renkle gösteriyoruz. diğer eşleşmeler kırmızı renkli 
matchesMask = [[0,0] for i in range(len(matches))]

for i, (match1, match2) in enumerate(matches):
    if match1.distance < 0.75*match2.distance:
        matchesMask[i] = [1,0]
        
draw_params = dict(matchColor = (0,0,255),
                  singlePointColor = (255,0,0),
                  matchesMask = matchesMask,
                  flags = 0)

flann_matchess = cv2.drawMatchesKnn(cheerios, kp1, cereals, kp2, matches, None, **draw_params)

display(flann_matchess)









