import cv2
import os
import FaceDetector as fd

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 360) # set video height
face_detector = fd.FaceDetector('DNN')

IMG_DIR = 'recognition_data/training_image'
MAX_NUM_PICTURE = 50

print("-" * 40)
print("This program takes picture of your face and save them")
print("Save directory is {0}/<identifier>".format(IMG_DIR))
print("Any pre-existing folder will be overwritten")
print("-" * 40)
iden = input("Enter identifier: ")
print("-" * 40)

SAVE_DIR = IMG_DIR + '/' + iden;
# if alrealdy exist, delete whole folder content
if (os.path.exists(SAVE_DIR)):
    for content in os.listdir(SAVE_DIR):
        os.remove(os.path.join(SAVE_DIR, content))
else:
    os.makedirs(SAVE_DIR)

img_count = 0
while (img_count < MAX_NUM_PICTURE):
    ret, img = cam.read()
    faces = face_detector.detectFaces(img)
    disp_img = img.copy()

    cv2.putText(disp_img,
                "Images taken: {0}".format(img_count),
                (10,350),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255,255,255),
                1)
    for (x1,y1,x2,y2) in faces:
        cv2.rectangle(disp_img, (x1,y1), (x2,y2), (0,255,0), 2)
    cv2.imshow('image', disp_img)

    k = cv2.waitKey(10)
    if (k & 0xFF == ord('s')):
        img_count += 1
        print("WRITE: {0}/{1:02d}.jpg".format(SAVE_DIR, img_count))
        cv2.imwrite("{0}/{1:02d}.jpg".format(SAVE_DIR, img_count), img[y1:y2, x1:x2])
    elif (k & 0xFF == ord('q')):
        break

cam.release()
cv2.destroyAllWindows()
