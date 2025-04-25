# 영상 파일을 읽고 윈도우에 디스플레이하기
import cv2 as cv
import sys

img = cv.imread('img/soccer.jpg')

if img is None:
    sys.exit('no file')

cv.imshow('Image Display', img)

cv.waitKey()
cv.destroyAllWindows()