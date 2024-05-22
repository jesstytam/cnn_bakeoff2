import argparse
import torch
from ultralytics import YOLO
from codecarbon import EmissionsTracker

#setup carbon tracker
tracker = EmissionsTracker()
# tracker.start()

# Setup argparse
parser = argparse.ArgumentParser(description='Running detection model for the different datasets.')
parser.add_argument('--model',
                    type=str,
                    required=True,
                    help='Choice of model.')
# parser.add_argument('--number_of_images',
#                     type=str,
#                     required=True,
#                     help='The number of images per species.')
args = parser.parse_args()

#check cuda
device = '0' if torch.cuda.is_available() else 'cpu'
if device=='0':
    torch.cuda.set_device(0)
print(f'Device: {device}')

#get model
print(f'Getting {args.model} for detection task.')
model = YOLO(f'{args.model}.yaml')
model = YOLO(f'{args.model}.pt')
model = YOLO(f'{args.model}.yaml').load(f'{args.model}.pt')

#initilise some parameters
ksplit = 5
results = {}

number_of_images = [10, 20, 50, 100]

#run models
for num in number_of_images:

    tracker.start()
    
    print(f'Running {args.model} with {num} images per species.')

    for k in range(ksplit):

        print(f'Running model for split {k+1}...')

        ds_yaml = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes_1x/{num}_img/2024-05-21_5-Fold_Cross-val/split_{k+1}/split_{k+1}_dataset.yaml'
        dataset_yaml = ds_yaml

        model.train(data=dataset_yaml,
                    seed=42,
                    dropout=0.5,
                    epochs=100,
                    batch=64,
                    patience=10,
                    plots=True,
                    name=f'fold_{k+1}', #name of sub-folder
                    project=f'{num}images_{args.model}_1xaug')  #name of parent folder
        
        results[k+1] = model.metrics  # save output metrics for further analysis
        print('... done!')

    tracker.stop()