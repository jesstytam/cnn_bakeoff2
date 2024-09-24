import os
import albumentations as A
import cv2
import numpy as np
import random
from PIL import Image

#setup loop
random.seed(666)
number_of_images = [10, 20, 50, 100, 250]
splits = [1, 2, 3, 4, 5]

for num in number_of_images:

    for split in splits:

        print(f'Doing transformations for {num} images per species.')
        parent_dir = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes_1x/{num}_img/2024-05-21_5-Fold_Cross-val/split_{split}'
        jpg_path = f'{parent_dir}/train/images'
        txt_path = f'{parent_dir}/train/labels'

        for im in os.listdir(jpg_path):
            print(f'Transforming {im} now...')

            #get images
            image_path = os.path.join(jpg_path, im)
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            #get bbox
            text_file = im.replace('.jpg', '.txt')
            box_path = os.path.join(txt_path, text_file)

            box_text = open(box_path, 'r')
            box_text = box_text.readline().replace('\n', '').split(' ')
            bbox = box_text[1:] + [box_text[0]]
            bbox = [list(np.float_(bbox))]
            labels = [bbox[0][-1]]

            #transformations
            width = random.randint(1024, 2048)
            height = random.randint(768, 1536)
            transform = A.Compose([
                A.Flip(p=0.5),
                A.RandomSizedBBoxSafeCrop(p=0.5, erosion_rate=0.5, width=width, height=height),
                A.RandomBrightnessContrast(p=0.5),
                A.GaussNoise(p=0.5),
                A.GaussianBlur(p=0.5),
                A.Rotate(p=0.5)
            ], bbox_params=A.BboxParams(format='yolo', label_fields=['labels']))

            #get new attributes
            print('Transforming image...')
            transformed_bbox = None
            try:
                while transformed_bbox is None or len(transformed_bbox)==0:
                    transformed = transform(image=image, bboxes=bbox, labels=labels)
                    transformed_image = transformed['image']
                    transformed_bbox = transformed['bboxes']
                    print(transformed_bbox)
            except (ValueError) as e:
                print(f'Transformed bbox: {transformed_bbox}')
                bbox=list(transformed_bbox)
                for i in range(4):
                    if (bbox[i]<0):
                        bbox[i]=0
                    elif (bbox[i]>1):
                        bbox[i]=1
                transformed_bbox=tuple(bbox)
                            
            #create new jpg
            new_im_name = im.replace('.jpg', '_a.jpg')
            new_im_path = os.path.join(jpg_path, new_im_name) 

            new_im = Image.fromarray(transformed_image)
            new_im.save(new_im_path)
            print(f'{new_im_path} saved!')

            #create new txt
            new_txt_name = im.replace('.jpg', '_a.txt')
            new_txt_path = os.path.join(txt_path, new_txt_name)
            
            print(transformed_bbox)
            new_bbox = transformed_bbox[0][:-1]
            new_label_dirty = transformed_bbox[0][-1]
            new_label = str(new_label_dirty).split('.')[0]
            
            with open(new_txt_path, 'w') as file:
                file.write(f'{new_label} {new_bbox[0]} {new_bbox[1]} {new_bbox[2]} {new_bbox[3]}')
                print(f'{new_bbox} {new_label}')