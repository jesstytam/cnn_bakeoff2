import argparse
import os

# Setup argparse
parser = argparse.ArgumentParser(description='Clean up class ids.')
parser.add_argument('--number_of_images',
                    type=str,
                    required=True,
                    help='The number of images per species.')
args = parser.parse_args()

def replace_classes(original_id, new_id):

    parent = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/{args.number_of_images}_img/labels/'

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

def replace_classes_for_datasets(original_id, new_id):
    print(f'Replacing {original_id} with {new_id} for data with {args.number_of_images} per class...')
    replace_classes(original_id, new_id)
    print(f'done!')

replace_classes_for_datasets(22, 1)
replace_classes_for_datasets(19, 4)
replace_classes_for_datasets(17, 5)
replace_classes_for_datasets(16, 9)
replace_classes_for_datasets(15, 12)
replace_classes_for_datasets(14, 13)