import os
import random
import shutil

categories = [2, 3, 6, 7, 8, 15, 16, 17, 19, 22]

all_labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/26_classes/labels'
labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes/train/labels/'

#copy labels
for c in categories:
    images_list = []
    for text in os.listdir(all_labels_dir):
        #get category label from text files
        with open(os.path.join(all_labels_dir, text)) as f:
            for line in f:
                cat = line.split(' ')[0]
                if cat == c:
                    images_list.append(text)
    #copying
    samples = random.sample(images_list, 1200)
    for sample in samples:
        src_dir = os.path.join(all_labels_dir, sample)
        shutil.copy(src_dir, labels_dir)

#copy images
all_images_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/26_classes/images/'
images_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes/train/images/'

for label in labels_dir:
    image_name = label.split('.')[0]+'.jpg'
    image_src_path = os.path.join(all_images_dir, image_name)
    shutil.copy(image_src_path, images_dir)