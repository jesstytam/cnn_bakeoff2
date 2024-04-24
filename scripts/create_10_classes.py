import os
import random

categories = [2, 3, 6, 7, 8, 15, 16, 17, 19, 22]

all_labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/26_classes/labels'

#copy labels
for c in categories:
    images_list = []
    for text in os.listdir(all_labels_dir):
        with open(os.path.join(all_labels_dir, text)) as f:
            for line in f:
                cat = line.split(' ')[0]
                if cat == c:
                    images_list.append(text)
    #copying
    labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes/train/labels/'
    samples = random.sample(images_list, 1200)

#copy images
images_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes/train/images/'