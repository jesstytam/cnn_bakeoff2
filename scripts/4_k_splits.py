import argparse
import datetime
import os
import shutil
from pathlib import Path
from collections import Counter

import yaml
import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

# Setup argparse
parser = argparse.ArgumentParser(description='Clean up class ids.')
parser.add_argument('--number_of_images',
                    type=str,
                    required=True,
                    help='The number of images per species.')
args = parser.parse_args()

#------------------------------

#generate dataset

print('Generating dataset.')

dataset_path = Path(f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes_1x/{args.number_of_images}_img/') # replace with 'path/to/dataset' for your custom data
labels = sorted(dataset_path.rglob("*labels/*.txt")) # all data in 'labels'

yaml_file = '/media/jess/DATA/PhD/cnn_bakeoff2/yolo/config/trial_aug.yaml'  # your data YAML with data directories and names dictionary
with open(yaml_file, 'r', encoding="utf8") as y:
    classes = yaml.safe_load(y)['names']
cls_idx = sorted(classes.keys())

indx = [l.stem for l in labels] # uses base filename as ID (no extension)
labels_df = pd.DataFrame([], columns=cls_idx, index=indx)

for label in labels:
    lbl_counter = Counter()

    with open(label,'r') as lf:
        lines = lf.readlines()

    for l in lines:
        # classes for YOLO label uses integer at first position of each line
        lbl_counter[int(l.split(' ')[0])] += 1

    # labels_df.loc[label.stem] = lbl_counter
    labels_df.loc[label.stem] = [lbl_counter[cls] for cls in classes]

labels_df = labels_df.fillna(0.0) # replace `nan` values with `0.0`

#------------------------------

#k-fold splits

print('Setting up the splits.')

ksplit = 5
kf = KFold(n_splits=ksplit, shuffle=True, random_state=20)   # setting random_state for repeatable results

kfolds = list(kf.split(labels_df))

folds = [f'split_{n}' for n in range(1, ksplit + 1)]
folds_df = pd.DataFrame(index=indx, columns=folds)

for idx, (train, val) in enumerate(kfolds, start=1):
    folds_df[f'split_{idx}'].loc[labels_df.iloc[train].index] = 'train'
    folds_df[f'split_{idx}'].loc[labels_df.iloc[val].index] = 'val'

fold_lbl_distrb = pd.DataFrame(index=folds, columns=cls_idx)

for n, (train_indices, val_indices) in enumerate(kfolds, start=1):
    train_totals = labels_df.iloc[train_indices].sum()
    val_totals = labels_df.iloc[val_indices].sum()

    # To avoid division by zero, we add a small value (1E-7) to the denominator
    ratio = val_totals / (train_totals + 1E-7)
    fold_lbl_distrb.loc[f'split_{n}'] = ratio

supported_extensions = ['.jpg', '.jpeg', '.png']

# Initialize an empty list to store image file paths
images = []

# Loop through supported extensions and gather image files
for ext in supported_extensions:
    images.extend(sorted((dataset_path / 'images').rglob(f"*{ext}")))

# Create the necessary directories and dataset YAML files (unchanged)
save_path = Path(dataset_path / f'{datetime.date.today().isoformat()}_{ksplit}-Fold_Cross-val')
save_path.mkdir(parents=True, exist_ok=True)
ds_yamls = []

for split in folds_df.columns:
    # Create directories
    split_dir = save_path / split
    split_dir.mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'train' / 'labels').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'images').mkdir(parents=True, exist_ok=True)
    (split_dir / 'val' / 'labels').mkdir(parents=True, exist_ok=True)

    # Create dataset YAML files
    dataset_yaml = split_dir / f'{split}_dataset.yaml'
    ds_yamls.append(dataset_yaml)

    with open(dataset_yaml, 'w') as ds_y:
        yaml.safe_dump({
            'path': split_dir.as_posix(),
            'train': 'train',
            'val': 'val',
            'names': classes
        }, ds_y)

print('Splitting now.')

for image, label in zip(images, labels):
    for split, k_split in folds_df.loc[image.stem].items():
        # Destination directory
        img_to_path = save_path / split / k_split / 'images'
        lbl_to_path = save_path / split / k_split / 'labels'

        # Copy image and label files to new directory (SamefileError if file already exists)
        shutil.copy(image, img_to_path / image.name)
        shutil.copy(label, lbl_to_path / label.name)

#save records
folds_df.to_csv(save_path / "kfold_datasplit.csv")
fold_lbl_distrb.to_csv(save_path / "kfold_label_distribution.csv")

#------------------------------

#checking

print('Running final checks.')

def dataset_summary_b(path):
    
    classes_dict = {}

    for filename in os.listdir(path):
        if filename.endswith('.txt'):  # Ensure it's a text file
            with open(os.path.join(path, filename), 'r') as file:
                for line in file:
                    sp_class = line.split(' ')[0]
                    classes_dict[sp_class] = classes_dict.get(sp_class, 0) + 1

    return dict(sorted(classes_dict.items()))

for num in range(1, 5):
    print(dataset_summary_b(f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes_1x/{args.number_of_images}_img/2024-05-21_5-Fold_Cross-val/split_{num}/train/labels'))