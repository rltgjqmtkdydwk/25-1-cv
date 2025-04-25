# 에지 맵에서 경계선 찾기
import cv2 as cv

# img = cv.imread('img/soccer.jpg')
img = cv.imread('ch04/img/cat.jpeg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
canny = cv.Canny(gray, 100, 200) # canny 결과랑 비교

contour, hierarchy = cv.findContours(canny, cv.RETR_LIST, cv.CHAIN_APPROX_NONE) # cv.CHAIN_APPROX_NONE : 여러가지 근사 버전 제공

lcontour=[]
for i in range(len(contour)):
    if contour[i].shape[0]>100: # 에지의 길이가 100보다 크면(시작점으로 돌아오는 것까지 추적하므로 실제로는 50보다)
        lcontour.append(contour[i])

cv.drawContours(img, lcontour,-1,(0,255,0),3)

cv.imshow('Original with contours', img)
cv.imshow('Canny', canny)

cv.waitKey()
cv.destroyAllWindows()
