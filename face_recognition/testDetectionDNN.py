import numpy as np
import cv2

modelPath = 'detection_model/opencv_dnn_face_detect'
modelName = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
configName = 'deploy.prototxt'
net = cv2.dnn.readNetFromCaffe(modelPath + '/' + configName,
                               modelPath + '/' + modelName);
cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,360) # set Height

def cropImage(image, finalWidth, finalHeight):
    currWidth, currHeight = image.shape[1], image.shape[0]
    cropMarginX = int( (currWidth-finalWidth) / 2 ) ;
    cropMarginY = int( (currHeight-finalHeight) / 2 );
    return image[cropMarginY:-cropMarginY, cropMarginX:-cropMarginX]

while True:
    ret, img = cap.read()
    imgCrop = cropImage(img, 300, 300);
    blob = cv2.dnn.blobFromImage(image = cv2.resize(img, (300, 300)),
                                 scalefactor = 1.0,
                                 size = (300, 300),
                                 mean = (104.0, 117.0, 123.0)
                                 )
    net.setInput(blob)
    faces = net.forward()

    for i in range(0, faces.shape[2]):
        confidence = faces[0, 0, i, 2]
        if confidence < 0.5:
            continue

        box = faces[0, 0, i, 3:7] * np.array([640, 360, 640, 360])
        (startX, startY, endX, endY) = box.astype("int")

        # draw the bounding box of the face along with the associated
        # probability
        text = "{:.2f}%".format(confidence * 100)
        y = startY - 10 if startY - 10 > 10 else startY + 10
        cv2.rectangle(img, (startX, startY), (endX, endY),
                      (0, 0, 255), 2)
        cv2.putText(img, text, (startX, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

    cv2.imshow('video',img)

    k = cv2.waitKey(1)
    if (k & 0xFF == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()
