import argparse
import random
import os
import shutil

# Setup argparse
parser = argparse.ArgumentParser(description='Moving data around.')
parser.add_argument('--folder_name',
                    type=str,
                    required=True,
                    help='Name of destination folder.')
args = parser.parse_args()

random.seed(10101010)
classes = range(0, 14)
random_classes = random.sample(classes, 10)
print(f'Random classes: ', random_classes)

number_of_images = [10, 20, 50, 100, 250, 500, 750, 1000]
ksplit = 5
datasets = ['train', 'val']

for num in number_of_images:
    
    for k in range(ksplit):
        
        #copy split files first
        parent_dir = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/{args.folder_name}/{num}_img/split_{k+1}'
        
        for ds in datasets:

            data_dir = os.path.join(parent_dir, ds)
            label_dir = data_dir + '/labels'
            image_dir = data_dir + '/images'

            for txt, jpg in zip(os.listdir(label_dir), os.listdir(image_dir)):
                
                #paths
                label_path = os.path.join(label_dir, txt)
                image_path = os.path.join(image_dir, jpg)
                #see class
                with open(label_path) as f:
                    for line in f:
                        cat = int(line.split(' ')[0]) #classes of image
                #delete file if class isn't in random_classes
                if cat not in random_classes:
                    print(f'... deleting {txt} and {jpg} file ...')
                    os.remove(label_path)
                    os.remove(image_path)
                    print(f'done!')

