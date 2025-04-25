#케니 에지 실험하기
import cv2 as cv

img = cv.imread('ch04/img/soccer.jpg')

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# Canny : 임계값 T 설정
canny1 = cv.Canny(gray, 50, 150)    # T최소 = 50, T최대 = 150 (high 엣지 수가 많기 때문에 T최소만 잘 맞춰주면 됨)
canny2 = cv.Canny(gray, 100, 200)   # T최소 = 100, T최대 = 200
canny3 = cv.Canny(gray, 400, 500)   # 그냥 해봄

cv.imshow('Original', gray)
cv.imshow('Canny1', canny1)
cv.imshow('Canny2', canny2)
cv.imshow('Canny3', canny3)

cv.waitKey()
cv.destroyAllWindows()
