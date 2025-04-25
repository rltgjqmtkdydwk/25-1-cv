# RGB 컬러 영상을 채널별로 구분해 디스플레이하기
import cv2 as cv
import sys

img = cv.imread('ch03/img/cat.jpeg')

if img is None:
    sys.exit('파일을 찾을 수 없습니다.')

cv.imshow('original', img)
cv.imshow('Upper left half', img[0:img.shape[0]//2, 0:img.shape[1]//2,:])
cv.imshow('Center half', img[img.shape[0]//4:3*img.shape[0]//4, 
                        img.shape[1]//4:3*img.shape[1]//4,:])
cv.imshow('R', img[:,:,2])
cv.imshow('G', img[:,:,1])
cv.imshow('B', img[:,:,0])

cv.waitKey()
cv.destroyAllWindows()


