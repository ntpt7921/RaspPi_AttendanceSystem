import FaceDetector
import cv2

dt = FaceDetector.FaceDetector('LBPCascade')

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,360) # set Height

while True:
    ret, img = cap.read()
    faces =  dt.detectFaces(img)

    for (x1,y1,x2,y2) in faces:
        cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
    cv2.imshow('video',img)

    k = cv2.waitKey(1)
    if (k & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
