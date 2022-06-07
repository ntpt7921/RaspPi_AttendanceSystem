import numpy as np
import cv2

modelPath = 'detection_model/opencv_harr_cascade'
modelName = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(modelPath + '/' + modelName)

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,360) # set Height

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,
        minSize=(50, 50)
    )

    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    cv2.imshow('video',img)

    k = cv2.waitKey(1)
    if (k & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
