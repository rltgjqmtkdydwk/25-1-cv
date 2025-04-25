import cv2 as cv

img = cv.imread('img/cat.jpeg')
bg = cv.imread('img/bg.jpeg')

img = cv.cvtColor(img, cv.COLOR_RGB2BGR)

height, width, ch = img.shape
img = cv.resize(img, (966, 604))
print(img.shape)
print(bg.shape)

img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
cv.imwrite('ullim_resize.jpg', img)

cv.waitKey()
cv.destroyAllWindows()