# Face recognition library for this project

## Introduction

This is the library for face recognition used in this project, written with OpenCV.

The library has two purpose: detection and recognition. Both task are divided into their own class (file `FaceDetector.py` and `FaceRecognizer.py`).

For face detection, three different method of the OpenCV library are used: LBPCascade, HaarCascade and DNN. Each method need model data (saved in `detection_model`).

For face recognition, only one method of OpenCV are used: LBPHFaceRecognizer. We can train a recognizer model with a list of face image (stored in `recognition_data/training_image`) and then save the model into a YML file for later use (stored in `recognition_data/saved_LBP_model_state`).

The example code `test*.py` shows how to use the library without wrapper.

For external use, wrapper (defined in `__init__.py`) is provided for convinence.

## Basic usage

This section descibe how to use the library with wrapper externally. It is assumed that user are importing the library from project root. Most of the internal operation detail are omitted when using this wrapper, making it easy to use.

### Importing library

```python
import face_recognition as fr
```

### Recognize face given model name

```python
fr.recognizeFaceFromModel(modelName)
```

### Train new model

```python
fr.trainRecognitionModel(newModelName)
```

### Check if a model with given name exists

```python
fr.existRecognitionModel(modelName)
```

## More information
See [the note file](NOTE.md) for more information and resources.
