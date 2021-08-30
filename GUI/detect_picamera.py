import tensorflow as tf
import cv2
import time
import numpy as np
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')   # Suppress Matplotlib warnings
from picamera import PiCamera
import picamera
import picamera.array

def activateCamera():
  with picamera.PiCamera() as camera:
    print("Capturing image")
    camera.rotation = 180
    camera.resolution = (224, 224)
    camera.capture("saved_image.jpg")
    camera.stop_preview()
  print("Captured image")

def load_image_into_numpy_array(path):
  return np.array(Image.open(path))

def annotateImage(image_path):
  print("Starting predictions")
  model = tf.saved_model.load("./mobilenet-model/export/saved_model") #Load the model
  img_imread = cv2.imread(image_path)
  image_np = load_image_into_numpy_array(image_path) #Load image into the numpy array
  input_tensor = tf.convert_to_tensor(image_np)
  input_tensor = input_tensor[tf.newaxis, ...]
  detections = model(input_tensor)
  num_detections = int(detections.pop('num_detections'))
  detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}
  detections['num_detections'] = num_detections
  detections['detection_classes'] = detections['detection_classes'].astype(np.int64) #Get detection classes
  h,w,c=img_imread.shape
  labels=['dirty','clean']
  confident_classes=[]
  print("Starting annotation....")
  for score, (ymin,xmin,ymax,xmax), label in zip(detections['detection_scores'], detections['detection_boxes'], detections['detection_classes']):
    if score < 0.5:
        continue #only get the class with a confidence level higher than 0.5
    xmax=int(xmax*w)
    xmin=int(xmin*w)
    ymax=int(ymax*h)
    ymin=int(ymin*h) 
    confident_classes.append(label)
    print(xmax,xmin,ymax,ymin)
    score_txt = f'{100 * round(score)}%'
    img_boxes = cv2.rectangle(img_imread,(xmin, ymin),(xmax, ymax),(0,0,0),2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(img_boxes, str(labels[label-1]),(xmin, ymin), font, 1, (255,0,0), 2, cv2.LINE_AA)
    # cv2.putText(img_boxes,str(score_txt),(50, 50), font, 1, (255,0,0), 2, cv2.LINE_AA)
    cv2.imwrite("detection_result.jpg",img_boxes)
  print("Classes detected:",confident_classes)
  return 2 in confident_classes

def predictClass(image_path):
  print("Starting predictions")
  model = tf.saved_model.load("./mobilenet-model/export/saved_model") #Load the model
  image_np = load_image_into_numpy_array(image_path) #Load image into the numpy array
  input_tensor = tf.convert_to_tensor(image_np)
  input_tensor = input_tensor[tf.newaxis, ...]
  detections = model(input_tensor)
  num_detections = int(detections.pop('num_detections'))
  detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}
  detections['num_detections'] = num_detections
  detections['detection_classes'] = detections['detection_classes'].astype(np.int64) #Get detection classes
  confident_classes=[]
  print("Getting only classes with confidence level above 0.5....")
  for score, label in zip(detections['detection_scores'], detections['detection_classes']):
    if score < 0.5:
        continue #only get the class with a confidence level higher than 0.5
    confident_classes.append(label)
  print("Classes detected:",confident_classes)
  return 2 in confident_classes

#import time
#start = time.time()
#print(predictClass("classification-images/clean/IMG_20210824_154806.jpg"))
#end = time.time()
#hours, rem = divmod(end-start, 3600)
#minutes, seconds = divmod(rem, 60)
#print("{:0>2}:{:0>2}:{:05.2f}".format(int(hours),int(minutes),seconds))
