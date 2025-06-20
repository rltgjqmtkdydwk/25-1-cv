import cv2 as cv
import numpy as np
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions

model = ResNet50(weights='imagenet')

img = cv.imread('ullim.jpeg')
x=np.reshape(cv.resize(img, (224,224)),(1, 224,224, 3))
x = preprocess_input(x)

preds = model.predict(x)
top5 = decode_predictions(preds, top=5)[0]
print('예측결과: ', top5)

for i in range(5):
    txt = top5[i][1]+ ':' +str(top5[i][2])
    cv.putText(img, txt, (20, 40+i*40), cv.FONT_HERSHEY_SIMPLEX, 1.5, (255,255,255), 2)

cv.imshow('Recognition result', img)

cv.waitKey()
cv.destroyAllWindows()