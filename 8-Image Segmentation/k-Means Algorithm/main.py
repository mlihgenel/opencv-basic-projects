import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_results(img1, img2):
    plt.figure(figsize=(10,6))
    plt.subplot(121)
    plt.imshow(img1)
    plt.title('Original Image')

    plt.subplot(122)
    plt.imshow(img2)
    plt.title(f'Segmented with k-Means K:{K}')
    plt.show()


img = cv2.imread('ladybug.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

Z = img.reshape((-1,3))
Z = np.float32(Z)

criteria = (cv2.TermCriteria_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.1)    
K = 8
ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

center = np.uint8(center)
res = center[label.flatten()]
segmented_image = res.reshape((img.shape))

show_results(img, segmented_image)