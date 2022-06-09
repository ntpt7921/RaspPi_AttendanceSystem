import numpy as np
import os.path as path
import cv2

class FaceDetector:
    modelType = None
    __model = None
    __modelPath = None
    __modelDetectFunction = None

    def __init__(self, mType, mPath = path.dirname(__file__)):
        self.modelType = mType
        self.__modelPath = mPath
        self.__initDetectionModel()
        self.__initDetectionFunction()

    def detectFaces(self, image):
        return self.__modelDetectFunction(image);

    def __initDetectionModel(self):
        if (self.modelType == 'HaarCascade'):
            self.__initHaarModel()
        elif (self.modelType == 'DNN'):
            self.__initDNNModel()
        elif (self.modelType == 'LBPCascade'):
            self.__initLBPModel()
        else:
            raise Exception("Unknown detection model type, provided " + self.modelType)

    def __initHaarModel(self):
        modelPath = self.__modelPath + '/' + 'detection_model/opencv_harr_cascade'
        modelName = 'haarcascade_frontalface_default.xml'
        self.__model = cv2.CascadeClassifier(modelPath + '/' + modelName)

    def __initDNNModel(self):
        modelPath = self.__modelPath + '/' + 'detection_model/opencv_dnn_face_detect'
        modelName = 'res10_300x300_ssd_iter_140000_fp16.caffemodel'
        configName = 'deploy.prototxt'
        self.__model = cv2.dnn.readNetFromCaffe(modelPath + '/' + configName,
                                                modelPath + '/' + modelName);

    def __initLBPModel(self):
        modelPath = self.__modelPath + '/' + 'detection_model/opencv_lbp_cascade'
        modelName = 'lbpcascade_frontalface_improved.xml'
        self.__model = cv2.CascadeClassifier(modelPath + '/' + modelName)

    def __initDetectionFunction(self):
        if (self.modelType == 'HaarCascade'):
            self.__modelDetectFunction = self.__initHaarDetectFunction
        elif (self.modelType == 'DNN'):
            self.__modelDetectFunction = self.__initDNNDetectFunction
        elif (self.modelType == 'LBPCascade'):
            self.__modelDetectFunction = self.__initLBPDetectFunction
        else:
            raise Exception("Unknown detection model type, provided " + self.modelType)

    def __initHaarDetectFunction(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.__model.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(50, 50)
        )
        return [(x, y, x+w, y+h) for (x, y, w, h) in faces]

    def __initDNNDetectFunction(self, image):
        height, width = image.shape[0], image.shape[1]
        blob = cv2.dnn.blobFromImage(image = cv2.resize(image, (300, 300)),
                                     scalefactor = 1.0,
                                     size = (300, 300),
                                     mean = (104.0, 117.0, 123.0)
                                     )
        self.__model.setInput(blob)
        faces = self.__model.forward()
        outputFaces = []

        for i in range(0, faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence < 0.7:
                continue
            box = faces[0, 0, i, 3:7] * np.array([width, height, width, height])
            outputFaces.append(box.astype("int"))

        return outputFaces

    def __initLBPDetectFunction(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.__model.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5,
            minSize=(50, 50)
        )
        return [(x, y, x+w, y+h) for (x, y, w, h) in faces]
