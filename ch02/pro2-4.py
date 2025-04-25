# 웹 캠으로 비디오 획득하기
import cv2 as cv
import sys

img = cv.imread('img/soccer.jpg')

if img is None:
    sys.exit('no file')