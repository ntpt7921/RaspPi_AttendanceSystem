from .FaceDetector import FaceDetector
from .FaceRecognizer import FaceRecognizer
import os
import time
import cv2

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 360
COLOR_BGR_GREEN = (0, 255, 0)
COLOR_BGR_WHITE = (255, 255, 255)
CONFIDENCE_THRES = 50
AUTHEN_TIME_BEFORE_TIMEOUT = 10 # second
AUTHEN_TIME_DELAY = 2 # second

packagePath = os.path.dirname(__file__)
recogModelPath = os.path.join(packagePath, 'recognition_data', 'saved_LBPH_model_state')
trainingFacesPath = os.path.join(packagePath, 'recognition_data', 'training_image')

def getRecognitionModel(modelName):
    return  FaceRecognizer(recogModelPath + '/' + modelName + '.yml')

def getDetectionModel(modelType = 'DNN'):
    return FaceDetector(modelType)

def existRecognitionModel(modelName):
    modelNames = [filename.split('.', 2)[0] for filename in os.listdir(recogModelPath)]
    if (modelName in modelNames):
        return True
    else:
        return False

def recognizeFaceFromModel(modelName):
    if not existRecognitionModel(modelName):
        raise FileNotFoundError()

    detect = getDetectionModel('DNN')
    recog = getRecognitionModel(modelName)
    cam = setupCamera(CAMERA_WIDTH, CAMERA_HEIGHT)
    startTime = time.time();
    isRecognized = False
    isAuthenticated = False

    while (True):
        elapsedTime = time.time() - startTime; # in second .
        if (elapsedTime >= AUTHEN_TIME_BEFORE_TIMEOUT):
            break;

        _, img = cam.read()
        displayImg = img.copy()

        faces = detect.detectFaces(img)
        if (len(faces) == 0):
            continue
        (x1, y1, x2, y2) = getLargestFace(faces)
        _, confidence = recog.recognizeFace(img[y1:y2,x1:x2])

        # only authenticate if recognized continuously for AUTHEN_TIME_DELAY
        if (confidence < CONFIDENCE_THRES):
            if (not isRecognized):
                startBeingRecognizedAt = time.time()
                isRecognized = True
        else:
            isRecognized = False
        if (isRecognized and (time.time() - startBeingRecognizedAt) >= AUTHEN_TIME_DELAY):
            isAuthenticated = True
            break
        print(isRecognized, confidence)

        drawFaceBox(displayImg,
                    coordUpperLeft = (x1, y1),
                    coordLowerRight = (x2, y2),
                    color = COLOR_BGR_GREEN)
        drawText(displayImg,
                 text = "Time left: {0}".format(round(10 - elapsedTime)),
                 coord = (10, 10),
                 size = 0.5,
                 color = COLOR_BGR_WHITE)
        showImage(displayImg, "Authenticate face")

    cam.release()
    cv2.destroyAllWindows()
    return isAuthenticated

def trainRecognitionModel(newModelName):
    takeFacePictures(newModelName)
    trainWithFacesPictures(newModelName)

def takeFacePictures(iden, imgCountMax = 30):
    # test for folder to save image, if exist then overwrite folder content
    idenFolderPath = trainingFacesPath + '/' + iden
    if (os.path.exists(idenFolderPath)):
        for content in os.listdir(idenFolderPath):
            os.remove(os.path.join(idenFolderPath, content))
    else:
        os.makedirs(idenFolderPath)

    # start to take image through loop, the current image is saved when pressing s
    # can quit prematurely with pressing q
    cam = setupCamera(CAMERA_WIDTH, CAMERA_HEIGHT)
    detect = getDetectionModel('DNN')
    imgCount = 0;
    while (imgCount < imgCountMax):
        _, img = cam.read()
        displayImg = img.copy()

        faces = detect.detectFaces(img)
        if (len(faces) == 0):
            continue
        (x1, y1, x2, y2) = getLargestFace(faces)
        drawFaceBox(displayImg,
                    coordUpperLeft = (x1, y1),
                    coordLowerRight = (x2, y2),
                    color = COLOR_BGR_GREEN)
        drawText(displayImg,
                 text = "Images taken: {0}".format(imgCount),
                 coord = (10, 10),
                 size = 0.5,
                 color = COLOR_BGR_WHITE)

        showImage(displayImg, "Take training image")

        k = cv2.waitKey(10)
        if (k & 0xFF == ord('s')):
            imgCount += 1
            cv2.imwrite("{0}/{1:02d}.jpg".format(idenFolderPath, imgCount),
                        img[y1:y2, x1:x2])
        elif (k & 0xFF == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()


def trainWithFacesPictures(newModelName):
    imageFolderPath = os.path.join(trainingFacesPath, newModelName)
    if not os.path.exists(imageFolderPath):
        raise FileNotFoundError(imageFolderPath)

    imagePaths = [os.path.join(imageFolderPath, f) for f in os.listdir(imageFolderPath)]
    faceSamples = [cv2.imread(imagePath) for imagePath in imagePaths]

    recog = FaceRecognizer();
    recog.trainWithFaces(faceSamples, [0] * len(faceSamples)) # train with id of zero for all image
    recog.saveModel(recogModelPath, newModelName)

def getLargestFace(faceCoords):
    if (len(faceCoords) == 0):
        return None;
    faceSizes = [(x2 - x1 + y2 - y1) for (x1, y1, x2, y2) in faceCoords]
    minSizeIndex = min(range(len(faceSizes)), key=faceSizes.__getitem__) # get min value's index'
    return faceCoords[minSizeIndex]

def drawFaceBox(img, coordUpperLeft, coordLowerRight, color):
    cv2.rectangle(img, coordUpperLeft, coordLowerRight, color, 2)

def drawText(img, text, coord, size, color):
    cv2.putText(img, text, coord,
                cv2.FONT_HERSHEY_SIMPLEX,
                size, color, 2)

def showImage(img, message):
    cv2.imshow(message, img)

def setupCamera(width, height):
    cam = cv2.VideoCapture(0)
    cam.set(3, width)
    cam.set(4, height)
    return cam
