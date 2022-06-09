import os
import cv2
import FaceDetector as fd
import FaceRecognizer as fr

SAVED_LBPH_PATH = 'recognition_data/saved_LBPH_model_state'

print('-' * 40)
print("This program will test the face detection ability")
print("It will first ask for the saved model name")
print("Load the model at {0}".format(SAVED_LBPH_PATH))
print("Test current detected face with the model, providing ID and confidence level")
print('-' * 40)
MODEL_NAME = input("Enter model name: ")
print('-' * 40)

MODEL_PATH = os.path.join(SAVED_LBPH_PATH, MODEL_NAME + ".yml")
recog = fr.FaceRecognizer(MODEL_PATH)
detect = fd.FaceDetector('DNN')

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 360)

while True:
    ret, img = cam.read()
    faces = detect.detectFaces(img)

    for (x1, y1, x2, y2) in faces:
        cv2.rectangle(img, (x1, y1), (x2, y2), (0,255,0), 2)
        label, confidence = recog.recognizeFace(img[y1:y2,x1:x2])

        cv2.putText(img,
                    str(label),
                    (x1+5,y1-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2
                   )
        cv2.putText(img,
                    str(round(confidence, 1)),
                    (x1+5,y2-5),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255,255,255),
                    2
                   )

    cv2.imshow('camera',img)

    k = cv2.waitKey(10)
    if (k & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()
