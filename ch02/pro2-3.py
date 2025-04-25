# 영상을 명암 영상으로 변환하고 반으로 축소하기
import cv2 as cv
import sys

img = cv.imread('img/soccer.jpg')

if img is None:
    sys.exit('no file')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

height, width = gray.shape
gray_small = cv.resize(gray, (width // 2, height // 2))

cv.imwrite('soccer_gray.jpg', gray) # 이미지 저장 함수
cv.imwrite('soccer_gray_small.jpg', gray_small)

cv.imshow('Color image', img)
cv.imshow('soccer_gray.jpg', gray)
cv.imshow('soccer_gray_small.jpg', gray_small)

cv.waitKey()
cv.destroyAllWindows()
