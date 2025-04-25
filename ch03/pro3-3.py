# 오츄 알고리즘으로 이진화하기
import cv2 as cv 
import sys

img = cv.imread('ch03/img/cat.jpeg')

t, bin_img = cv.threshold(img[:,:,2], 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
print('오츄 알고리즘이 찾은 최적 임계값 = ', t)

cv.imshow('R', img[:,:,2])
cv.imshow('R', bin_img)

cv.waitKey()
cv.destroyAllWindows()