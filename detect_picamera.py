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
  # with open('mobilenet-model/tfjsexport/model.json', 'r') as json_file:
  #   saved_json_model=json_file.read()
  print("Starting predictions")
  model = tf.saved_model.load("./mobilenet-model/export/saved_model")

  img_imread = cv2.imread(image_path)
  image_np = load_image_into_numpy_array(image_path)

  # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
  input_tensor = tf.convert_to_tensor(image_np)
  # The model expects a batch of images, so add an axis with `tf.newaxis`.
  input_tensor = input_tensor[tf.newaxis, ...]
  tic = time.time()
  detections = model(input_tensor)
  num_detections = int(detections.pop('num_detections'))
  detections = {key: value[0, :num_detections].numpy()
                   for key, value in detections.items()}
  detections['num_detections'] = num_detections
  detections['detection_classes'] = detections['detection_classes'].astype(np.int64)
  h,w,c=img_imread.shape
  # labels=['dirty','clean']
  confident_classes=[]
  toc = time.time()
  print(f"Model finished detection in {toc - tic:0.4f} minutes")
  print("Starting annotation....")
  for score, (ymin,xmin,ymax,xmax), label in zip(detections['detection_scores'], detections['detection_boxes'], detections['detection_classes']):
    if score < 0.5:
        continue
    # xmax=int(xmax*w)
    # xmin=int(xmin*w)
    # ymax=int(ymax*h)
    # ymin=int(ymin*h) 
    confident_classes.append(label)
    # print(xmax,xmin,ymax,ymin)
    # score_txt = f'{100 * round(score)}%'
    # img_boxes = cv2.rectangle(img_imread,(xmin, ymin),(xmax, ymax),(0,0,0),2)
    # font = cv2.FONT_HERSHEY_SIMPLEX
    # print(label)
    # cv2.putText(img_boxes, str(labels[label-1]),(xmin, ymin), font, 1, (255,0,0), 2, cv2.LINE_AA)
    # # cv2.putText(img_boxes,str(score_txt),(50, 50), font, 1, (255,0,0), 2, cv2.LINE_AA)
    # cv2.imwrite("detection_result.jpg",img_boxes)
  print(confident_classes)
  return 1 in confident_classes
print(annotateImage("saved_image.jpg"))
