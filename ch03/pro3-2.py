# 실제 영상에서 히스토그램 구하기
import cv2 as cv 
import matplotlib.pyplot as plt 

img = cv.imread('ch03/img/mistyroad.jpg')
h = cv.calcHist([img], [2], None, [256], [0, 256])

# 히스토그램 그리기
plt.plot(h, color='r', linewidth=1)
plt.title('Red Channel Histogram')
plt.show()