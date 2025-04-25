# **히스토그램 평활화하기
from turtle import color
import cv2 as cv
import matplotlib.pyplot as plt

img = cv.imread('ch03/img/mistyroad.jpg')

# 명암 영상으로 변환
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
plt.imshow(gray, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

# 히스토그램 계산
h = cv.calcHist([gray], [0], None, [256], [0, 256])
plt.plot(h, color='r', linewidth=1)
plt.show()

equal = cv.equalizeHist(gray) # 히스토그램 평활화
plt.imshow(equal, cmap='gray'), plt.xticks([]), plt.yticks([])
plt.show()

# 히스토그램 계산
h = cv.calcHist([equal], [0], None, [256], [0, 256])
plt.plot(h, color='r', linewidth=1)
plt.show()