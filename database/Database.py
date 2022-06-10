import json
import os

DATA_PATH = '.'
DATA_NAME = 'data.json'

class Database:
    __data = None # is a dict after __init__
    __dataFilePath = None # store path to file after __init__

    def __init__(self, pathToFile = os.path.join(DATA_PATH, DATA_NAME)):
        if (not os.path.exists(pathToFile)):
            self.startNewDatabase(pathToFile)
        else:
            self.loadFromJSON(pathToFile)

    def startNewDatabase(self, path):
        open(path, 'w+').close() # create new file
        self.__data = {} # new empty dict
        self.__dataFilePath = path


    def loadFromJSON(self, path):
        jsonFile = open(path, 'r+')
        jsonText = jsonFile.read()
        jsonFile.close()

        self.__data = json.loads(jsonText)
        self.__dataFilePath = path

    def saveToJSON(self):
        if (self.__dataFilePath is None):
            return # do nothing

        jsonText = json.dumps(self.__data, indent=4)
        f = open(self.__dataFilePath, 'w') # overwrite everything
        f.write(jsonText)
        f.close()

    def clearData(self):
        self.__data.clear()

    def getData(self, key):
        # get value for associated key, return None if not found
        return self.__data.get(key)

    def addData(self, key, value):
        self.__data[key] = value

    def removeData(self, key):
        # user have to make sure key exist, or error will be raised
        self.__data.pop(key)
