# 정규화 절단 알고리즘으로 영역 분할하기(시간x)
from cProfile import label
from tkinter import N
import skimage
import numpy as np
import cv2 as cv

coffee = skimage.data.coffee()

slic=skimage.segmentation.slic(coffee, compactness=20, n_segments=600, label=1)

g = skimage.future.graph.rag_mean_color(coffee, slic, mode='similarity')
ncut = skimage.future.graph.cut_normalized(slic, g) # 정규화 절단 : 유사도 비교 후 클수록 더 쪼갠다

marking = skimage.segmentation.mark_boundaries(coffee, ncut)
ncut_coffee = np.uint8(marking*255.0)

cv.imshow('Normalized cut', cv.cvtColor(ncut_coffee, cv.COLOR_RGB2BGR))
cv.waitKey()
cv.destroyAllWindows()