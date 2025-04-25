# 소벨 에지 검출하기 (Sobel 함수 사용)
import cv2 as cv

# img = cv.imread('img/soccer.jpg')
img=cv.imread('ch04/img/cat.jpeg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

grad_x=cv.Sobel(gray, cv.CV_32F,1,0,ksize=3)    # 소벨 사용
grad_y=cv.Sobel(gray, cv.CV_32F,0,1,ksize=3)

sobel_x=cv.convertScaleAbs(grad_x)  # 절댓값을 취해 양수로 변환(최소 0을 넘어가면 0, 최대 255를 넘어가면 255)
sobel_y=cv.convertScaleAbs(grad_y)

edge_strength=cv.addWeighted(sobel_x, 0.5, sobel_y, 0.5, 0) # 에지 강도 계산(위와 동일)

cv.imshow('Original', gray)
cv.imshow('Sobelx', sobel_x)
cv.imshow('Sobely', sobel_y)
cv.imshow('Edge Strength', edge_strength)

cv.waitKey()
cv.destroyAllWindows()