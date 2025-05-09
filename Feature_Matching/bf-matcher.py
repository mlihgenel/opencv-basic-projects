import cv2
import matplotlib.pyplot as plt

#----------------------------------------
def display(img, cmap = "gray"):
    plt.figure(figsize=(12,10))
    plt.imshow(img, cmap)
    plt.show()
#----------------------------------------

# içinde arayacağımız resmi okuyoruz
cheerios = cv2.imread('Feature_Matching/cheerios.png',0) 
# sadece plot edilirken daha güzel gözükmesi için boyutları ayarlıyoruz
cheerios = cv2.resize(cheerios, (550, 550), interpolation=cv2.INTER_AREA)
# ana resmimizi okuyoruz, cheerios resmini bu resimde arayacağız
cereals = cv2.imread('Feature_Matching/many_cereals.jpg',0)


# display(cheerios)
# display(cereals)

# --------- Brute-Force Matching with ORB Algorithm --------- # 

# ORB nesnesi oluşturuyoruz. 
orb = cv2.ORB_create()

# sırası ile iki resmimizde de keypoint ve descriptionları buluyoruz
kp1, des1 = orb.detectAndCompute(cheerios, mask=None)
kp2, des2 = orb.detectAndCompute(cereals, mask=None)

# brute-force methodu için BFMatcher nesnemizi oluşturuyoruz
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# oluşturduğumuz nesnelere descriptionları gönderip eşleştirme yapıyoruz.
# matches nesneleri '< cv2.DMatch 0x15e48ae10>' gibi nesneler.
matches = bf.match(des1, des2)

# bu eşleşmeleri uzaklıklara göre sıralıyoruz çünkü ne kadar az uzaklık o kadar iyi eşleşme demek
matches = sorted(matches, key = lambda x:x.distance)

# eşleşmeleri çizdiriyoruz (burada ilk 25 eşleşme yani en iyi 25 eşleşme çizildi)
cheerios_matches = cv2.drawMatches(cheerios, kp1, cereals, kp2, matches[:25], None, flags = 2)

display(cheerios_matches)

