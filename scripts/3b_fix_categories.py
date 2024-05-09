import os

def replace_classes(dataset, original_id, new_id):

    parent = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/{dataset}/labels/'

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

def replace_classes_for_datasets(datasets, original_id, new_id):
    for data in datasets:
        print(f'Replacing {original_id} with {new_id} for {data}...')
        replace_classes(data, original_id, new_id)
        print(f'done!')

datasets=['train']

replace_classes_for_datasets(datasets, 22, 1)
replace_classes_for_datasets(datasets, 19, 4)
replace_classes_for_datasets(datasets, 17, 5)
replace_classes_for_datasets(datasets, 16, 9)
replace_classes_for_datasets(datasets, 15, 12)
replace_classes_for_datasets(datasets, 14, 13)