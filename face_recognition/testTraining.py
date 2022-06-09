import numpy as np
import os
import cv2
import FaceRecognizer as fr

IMG_DIR = 'recognition_data/training_image'
MODEL_DIR = 'recognition_data/saved_LBPH_model_state'

print("-" * 40)
print("This program will read face image of subject identified by identifier")
print("and use it to train LBPH recognizer, model is saved with the same identifier")
print("Path to image folder is {0}/<identifier>".format(IMG_DIR))
print("Path to save model is {0}".format(MODEL_DIR))
print("-" * 40)
iden = input("Enter identifier: ")
print("-" * 40)

READ_IMG_DIR = os.path.join(IMG_DIR, iden)

# if does not exist, throw an error
if not os.path.exists(READ_IMG_DIR):
    raise FileNotFoundError(READ_IMG_DIR)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    for imagePath in imagePaths:
        print("READ IMAGE: {0}".format(imagePath))
        img = cv2.imread(imagePath)
        faceSamples.append(img)

    return faceSamples, [0] * len(faceSamples)

# all ids returned is 0 for this test
faces, ids = getImagesAndLabels(READ_IMG_DIR)

recog = fr.FaceRecognizer();
print("TRAIN WITH IMAGES, PLEASE WAIT...")
recog.trainWithFaces(faces, ids)
print("SAVE MODEL TO FILE " + "{0}/{1}.yml".format(MODEL_DIR, iden))
recog.saveModel(MODEL_DIR, iden)
