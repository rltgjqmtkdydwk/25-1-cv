# GrabCut 을 이용해 물체 분할하기
import cv2 as cv
import numpy as np

img = cv.imread('img/soccer.jpg')
img_show = np.copy(img)

mask = np.zeros((img.shape[0], img.shape[1]), np.uint8) # shape 에러
mask[:,:] = cv.GC_PR_BGD    # 모든 화소를 배경으로 추측하는 상태로 초기화

BrushSiz = 9
LColor, RColor = (255,0,0),(255,0,0) # 파란색(물체), 빨간색(배경)

def painting(event, x, y, flags):
    if event == cv.EVENT_LBUTTONDOWN:
        cv.circle(img_show, (x,y), BrushSiz, LColor, -1) # 왼쪽 버튼 파란색
        cv.circle(mask, (x,y), BrushSiz, cv.GC_FGD, -1)
    elif event == cv.EVENT_RBUTTONDOWN:
        cv.circle(img_show, (x,y), BrushSiz, RColor, -1) # 오른쪽 버튼 빨간색
        cv.circle(mask, (x,y), BrushSiz, cv.GC_BGD, -1)
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_LBUTTON:
        cv.circle(img_show, (x,y), BrushSiz, LColor, -1) # 왼쪽 버튼 클릭하고 이동 파란색
        cv.circle(mask, (x,y), BrushSiz, cv.GC_FGD, -1)
    elif event == cv.EVENT_MOUSEMOVE and flags == cv.EVENT_FLAG_RBUTTON:
        cv.circle(img_show, (x,y), BrushSiz, RColor, -1) # 오른쪽 버튼 클릭하고 이동 빨간색
        cv.circle(mask, (x,y), BrushSiz, cv.GC_BGD, -1)

cv.namedWindow('Painting')
cv.setMouseCallback('Painting', painting)
cv.imshow('Painting', img_show)

while(True):
    if cv.waitKey(1) == ord('q'): # 끝내기 q
        break

# 여기부터 GrabCut 적용
background = np.zeros((1,65), np.float64) # 배경 히스토그램 0
foreground = np.zeros((1,65), np.float64) # 물체 히스토그램 0

cv.grabCut(img, mask, None, background, foreground, 5, cv.GC_INIT_WITH_MASK)
mask2 = np.where((mask == cv.GC_BGD) | (mask==cv.GC_PR_BGD), 0, 1).astype('uint8')
grab = img*mask2[:,:,np.newaxis]
cv.imshow('Grab cut image', grab)

cv.waitKey()
cv.destroyAllWindows()