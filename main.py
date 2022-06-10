# This is the main file implementing all the functionality

import nfc
import database
import face_recognition as fr
import random

cardReader = nfc.readReader('i2c')
modelDtB = database.db()

# the main loop, continue until interupted by ^C
while (True):
    cardUID = cardReader.waitForCard()
    cardZeroBlock = cardReader.readCard(cardUID, blockNum = 0)
    cardNumberID = int.from_bytes(cardZeroBlock, byteorder='big')

    recogModelName = modelDtB.getData(cardNumberID)
    if (recogModelName is None or not fr.existRecognitionModel(recogModelName)):
        # the user have not been registered yet
        # or there's data entry for user, but no associated model
        # register them
        registerUser(cardNumberID)
    else:
        # registered user, try authenticate by face recognition
        authenticateUser(recogModelName)

def registerUser(cardNumberID):
    newModelName = getRandomName(length = 30)
    fr.trainRecognitionModel(newModelName)
    modelDtB.addData(cardNumberID, newModelName)

def authenticateUser(modelName):
    print("Start authenticate by recognizing face, stand still")
    success = fr.recognizeFaceFromModel(modelName)
    if (success == True):
        print("Authenticate successfully")
    else:
        print("Can not recognize face, please try again")

def getRandomName(length = 25):
    # get a random generated name of the form [a-zA-z0-9]{<length>}
    # there are 26 + 26 + 10 = 62 unique character
    name = "";
    for i in range(length):
        randomNumber = random.randomInt(0, 62 -1)
        if (randomNumber <= 25):
            # in the a-z range
            name += chr(ord(a) + randomNumber)
        elif (randomNumber <= 51):
            #in the A-Z range
            name += chr(ord(A) + randomNumber - 26)
        else:
            # in the 0-9 range
            name += chr(ord(0) + randomNumber - 52)
    return name
