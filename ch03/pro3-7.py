# 컨볼루션 적용(가우시안 스무딩과 엠보싱)하기
import cv2 as cv
import numpy as np

img = cv.imread('ch03/img/cat.jpeg')
img = cv.resize(img, dsize=(0,0), fx=0.4, fy=0.4)
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.putText(gray,'cat',(10,20),cv.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)
cv.imshow('Original', gray)

# 스무딩
smooth = np.hstack((cv.GaussianBlur(gray,(5,5),0.0),
                    cv.GaussianBlur(gray,(9,9),(0.0), cv.GaussianBlur(gray,(15,15),0.0))))
cv.imshow('Smooth', smooth)

# 엠보싱
femboss = np.array([[-1.0, 0.0, 0.0],
                    [0.0, 0.0, 0.0],
                    [0.0, 0.0, 1.0]])

gray16 = np.uint16(gray)
emboss=np.uint8(np.clip(cv.filter2D(gray16, -1, femboss)+128, 0, 255))
emboss_bad = np.uint8(cv.filter2D(gray16, -1, femboss)+128)
emboss_worse=cv.filter2D(gray,-1,femboss)

cv.imshow('Emnoss', emboss)
cv.imshow('Emnoss_bad', emboss_bad)
cv.imshow('Emnoss_worse', emboss_worse)

cv.waitKey()
cv.destroyAllWindows()