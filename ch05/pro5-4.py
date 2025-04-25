# RANSAC을 이용해 호모그래피 추정하기
import cv2 as cv
import numpy as np

# 영상 로딩 (모델: 버스 부분 크롭, 관찰: 전체 이미지)
img1 = cv.imread('ch05/img/mot_color70.jpg')[190:350, 440:560]  # 모델 영상
gray1 = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
img2 = cv.imread('ch05/img/mot_color83.jpg')  # 관찰 영상
gray2 = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)

# SIFT 추출
sift = cv.SIFT_create()
kp1, des1 = sift.detectAndCompute(gray1, None)
kp2, des2 = sift.detectAndCompute(gray2, None)

# FLANN 매칭
flann_matcher = cv.DescriptorMatcher_create(cv.DescriptorMatcher_FLANNBASED)
knn_match = flann_matcher.knnMatch(des1, des2, k=2)

# 좋은 매칭 선별 (Lowe's ratio test)
T = 0.7
good_match = []
for nearest1, nearest2 in knn_match:
    if nearest1.distance < T * nearest2.distance:
        good_match.append(nearest1)

# 매칭된 점 추출
points1 = np.float32([kp1[m.queryIdx].pt for m in good_match])
points2 = np.float32([kp2[m.trainIdx].pt for m in good_match])

# RANSAC을 이용한 호모그래피 계산
H, _ = cv.findHomography(points1, points2, cv.RANSAC)

# 각 영상의 크기
h1, w1 = img1.shape[0], img1.shape[1]
h2, w2 = img2.shape[0], img2.shape[1]

# 변환 전 박스 좌표 (img1)
box1 = np.float32([[0, 0], [w1, 0], [w1, h1], [0, h1]]).reshape(-1, 1, 2)
# img2로 투영된 박스 좌표 계산
box2 = cv.perspectiveTransform(box1, H)
# 박스를 img2에 그림
img2 = cv.polylines(img2, [np.int32(box2)], True, (0, 255, 0), 2)

# 매칭 결과 시각화
img_match = np.empty((max(h1, h2), w1 + w2, 3), dtype=np.uint8)
cv.drawMatches(img1, kp1, img2, kp2, good_match, img_match,
               flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)

cv.imshow('Matches and Homography', img_match)
cv.waitKey(0)
cv.destroyAllWindows()
