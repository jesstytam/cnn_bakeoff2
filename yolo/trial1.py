# from ultralytics import YOLO

# # Load a COCO-pretrained YOLOv5n model
# model = YOLO('yolov5n.pt')

# # Train the model on the COCO8 example dataset for 100 epochs
# results = model.train(data='config/trial1.yaml', epochs=100, imgsz=640)

# # Run inference with the YOLOv5n model on the 'bus.jpg' image
# results = model('path/to/bus.jpg')



# 1. Import necessary libraries
from ultralytics import YOLO # Here we import YOLO 
import yaml                  # for yaml files 
import torch
from PIL import Image
import os
import cv2
import time

# 2. Choose our yaml file
yaml_filename = 'yolo/config/trial1.yaml' 

# 3. Create Yolo model
model = YOLO('yolov5nu.yaml') # creates Yolo object from 'yolov8n.yaml' configuration file. 
model = YOLO('yolov5nu.pt')   # Loads pretrained weights             
model = YOLO('yolov5nu.yaml').load('yolov5nu.pt')  # build from YAML and transfer weights

# 4. Train the model
model.train(data='{}'.format(yaml_filename), epochs=100, patience=5, batch=64,  imgsz=640) 