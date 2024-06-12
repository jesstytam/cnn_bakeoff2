import argparse
import os

# Setup argparse
parser = argparse.ArgumentParser(description='Clean up class ids.')
parser.add_argument('--folder_name',
                    type=str,
                    required=True,
                    help='Folder that needs class replacing.')
args = parser.parse_args()

def replace_classes(original_id, new_id, num, k, dataset):

    parent = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/{args.folder_name}/{num}_img/split_{k}/{dataset}/labels/'

    for filename in os.listdir(parent):
        if filename.endswith('.txt'):  # Ensure processing only text files
            filepath = os.path.join(parent, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            changes_made = False  # Track if changes are made

            for line in lines:
                parts = line.strip().split()
                if parts and int(parts[0]) == original_id:
                    parts[0] = str(new_id)
                    updated_line = ' '.join(parts)
                    updated_lines.append(updated_line)
                    changes_made = True
                else:
                    updated_lines.append(line.strip())

            # Write the modified content back to the file
            if changes_made:
                with open(filepath, 'w') as file:
                    for line in updated_lines:
                        file.write(line + '\n')
                print(f'Modified {filepath}')

def replace_classes_for_datasets(original_id, new_id, num, k, dataset):
    print(f'Replacing {original_id} with {new_id} for data with {num} per class...')
    replace_classes(original_id, new_id, num, k, dataset)
    print(f'done!')

def dataset_summary_b(path):
    
    classes_dict = {}

    for filename in os.listdir(path):
        if filename.endswith('.txt'):  # Ensure it's a text file
            with open(os.path.join(path, filename), 'r') as file:
                for line in file:
                    sp_class = line.split(' ')[0]
                    classes_dict[sp_class] = classes_dict.get(sp_class, 0) + 1

    return dict(sorted(classes_dict.items()))



##############################



#run the thingo
number_of_images = [10, 20, 50, 100, 250, 500, 750, 1000]
datasets = ['train', 'val']

for num in number_of_images:

    for k in range(1, 6):

        for dataset in datasets:

            replace_classes_for_datasets(11, 5, num=num, k=k, dataset=dataset)
            replace_classes_for_datasets(12, 6, num=num, k=k, dataset=dataset)
            replace_classes_for_datasets(13, 8, num=num, k=k, dataset=dataset)
#check a few random folders
print(dataset_summary_b('/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes_b/100_img/split_4/train/labels'))
print(dataset_summary_b('/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes_b/10_img/split_2/train/labels'))
print(dataset_summary_b('/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes_b/750_img/split_1/val/labels'))

