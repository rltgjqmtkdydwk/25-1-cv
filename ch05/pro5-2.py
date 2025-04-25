# SIFT 검출
import cv2 as cv

img = cv.imread('img/mot_color70.jpg')
print(img)
gray = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)

sift = cv.SIFT_create() # SIFT 기술자
kp, des = sift.detectAndCompute(gray, None)

gray = cv.drawKeypoints(gray, kp, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv.imshow('sift', gray)

k=cv.waitKey()
cv.destroyAllWindows()