import os
import cv2
import numpy as np

class FaceRecognizer:
    __recogModel = None
    __recogModelPath = None

    def __init__(self, path = None):
        self.__recogModelPath = path
        self.__loadModel()

    def __loadModel(self):
        self.__recogModel = cv2.face.LBPHFaceRecognizer_create()

        if self.__recogModelPath is None: # if this is new model, don't load from existing file'
            return

        if not os.path.exists(self.__recogModelPath):
            raise FileNotFoundError(self.__recogModelPath)

        self.__recogModel.read(self.__recogModelPath)

    def saveModel(self, path = None, modelname = None):
        if self.__recogModelPath is None: # if new model, don't have path yet'
            self.__recogModel.write("{0}/{1}.yml".format(path, modelname))
            self.__recogModelPath = "{0}/{1}.yml".format(path, modelname)
        else: # loaded model, save to the same file
            self.__recogModel.write(self.__recogModelPath)

    def recognizeFace(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        label, confidence = self.__recogModel.predict(gray)
        return label, confidence

    def trainWithFaces(self, faces, ids):
        grays = [cv2.cvtColor(face, cv2.COLOR_BGR2GRAY) for face in faces]
        self.__recogModel.train(grays, np.array(ids))
