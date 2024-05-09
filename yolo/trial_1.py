# 1. Import necessary libraries
from ultralytics import YOLO # Here we import YOLO 
import yaml                  # for yaml files 
import torch
from PIL import Image
import os
import cv2
import time

# 2. Choose our yaml file
yaml_filename = 'config/trial_1.yaml' 

# 3. Create Yolo model
model = YOLO('yolov9c.yaml') # creates Yolo object from 'yolov8n.yaml' configuration file. 
model = YOLO('yolov9c.pt')   # Loads pretrained weights             
model = YOLO('yolov9c.yaml').load('yolov9c.pt')  # build from YAML and transfer weights

# 4. Train the model
model.train(data='{}'.format(yaml_filename), epochs=100, patience=5, batch=64,  imgsz=640) 