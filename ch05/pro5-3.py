# FLANN 라이브러리를 이용한 SIFT 매칭
import cv2 as cv
import numpy as np
import time

# 버스를 크롭하여 모델 영상으로 사용
img1 = cv.imread('ch05/img/mot_color70.jpg')[190:350, 440:560]  # 모델 영상 (크롭된 이미지)
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

# 관염 영상
img2 = cv.imread('ch05/img/mot_color83.jpg')
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

# SIFT 생성
sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# FLANN 매칭기
start = time.time()
flann_matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
knn_match = flann_matcher.knnMatch(des1, des2, k=2)

# Lowe's ratio test 적용
T = 0.7
good_match = []
for nearest1, nearest2 in knn_match:
    if nearest1.distance < T * nearest2.distance:
        good_match.append(nearest1)

print("매칭에 걸린 시간:", time.time() - start)

# 결과 시각화
img_match = np.empty((max(img1.shape[0], img2.shape[0]), img1.shape[1] + img2.shape[1], 3), dtype=np.uint8)
cv.drawMatches(img1, kp1, img2, kp2, good_match, img_match,
               flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv.imshow('Good Matches', img_match)
cv.waitKey(0)
cv.destroyAllWindows()
