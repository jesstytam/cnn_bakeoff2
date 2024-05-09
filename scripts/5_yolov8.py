import argparse
import torch
from ultralytics import YOLO

# Setup argparse
parser = argparse.ArgumentParser(description='Running YOLOv8 for the different datasets.')
parser.add_argument('--model',
                    type=str,
                    required=True,
                    help='Size of YOLOv8.')
parser.add_argument('--number_of_images',
                    type=str,
                    required=True,
                    help='The number of images per species.')
args = parser.parse_args()

#check cuda
device = '0' if torch.cuda.is_available() else 'cpu'
if device=='0':
    torch.cuda.set_device(0)
print(f'Device: {device}')

#get model
model = YOLO(f'{args.model}.yaml')
model = YOLO(f'{args.model}.pt')
model = YOLO(f'{args.model}.yaml').load(f'{args.model}.pt')

#initilise some parameters
ksplit = 5
results = {}

# Define your additional arguments here
batch = 64
project = f'kfold_{args.number_of_images}images'
epochs = 100
patience = 10

#run models
for k in range(ksplit):
    print(f'Running model for split {k+1}...')
    ds_yaml = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/{args.number_of_images}_img/2024-05-09_5-Fold_Cross-val/split_{k+1}/split_{k+1}_dataset.yaml'
    dataset_yaml = ds_yaml
    model.train(data=dataset_yaml,
                epochs=epochs,
                batch=batch,
                patience=patience,
                project=project)  # include any train arguments
    results[k+1] = model.metrics  # save output metrics for further analysis
    print('... done!')

print("Training results:", results)