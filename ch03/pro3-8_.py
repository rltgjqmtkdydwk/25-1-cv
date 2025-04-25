# **보간을 이용해 영상의 기하 변환하기
import cv2 as cv

img=cv.imread('img/rose.png')
patch=img[250:350, 170:270,:]

img=cv.rectangle(img, (170,250), (270,350), (255,0,0),3)
patch1=cv.resize(patch, dsize=(0,0), fx=5, fy=5, interpolation=cv.INTER_NEAREST)
patch2=cv.resize(patch, dsize=(0,0), fx=5, fy=5, interpolation=cv.INTER_LINEAR)
patch3=cv.resize(patch, dsize=(0,0), fx=5, fy=5, interpolation=cv.INTER_CUBIC)

cv.imshow('Original', img)
cv.imshow('Resize nearest', img)
cv.imshow('Resize bilinear', img)
cv.imshow('Resize bicubic', img)

cv.waitKey()
cv.destroyAllWindows()
