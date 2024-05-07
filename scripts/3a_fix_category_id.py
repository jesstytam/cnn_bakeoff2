import os

def replace_classes(dataset, original_id, new_id):

    parent = f'/media/jess/DATA/PhD/data/ecoflow/yolo_labels/10_classes/labels/{dataset}/'

    for filename in os.listdir(parent):
        if filename.endswith('.txt'):  # Ensure processing only text files
            filepath = os.path.join(parent, filename)
            with open(filepath, 'r') as file:
                lines = file.readlines()

            updated_lines = []
            for line in lines:
                parts = line.strip().split()
                if parts and parts[0] == original_id:
                    parts[0] = new_id  
                    updated_line = ' '.join(parts)
                    updated_lines.append(updated_line)
                else:
                    updated_lines.append(line.strip())

            # Write the modified content back to the file
            with open(filepath, 'w') as file:
                for line in updated_lines:
                    file.write(line + '\n')
                    print(line)

def replace_classes_for_datasets(datasets, original_id, new_id):
    for data in datasets:
        print(f'Replacing {original_id} with {new_id} for {data}...')
        replace_classes(data, str(original_id), str(new_id))
        print(f'done!')

datasets=['train','test']

replace_classes_for_datasets(datasets, 15, 0)
replace_classes_for_datasets(datasets, 16, 1)
replace_classes_for_datasets(datasets, 17, 4)
replace_classes_for_datasets(datasets, 19, 5)
replace_classes_for_datasets(datasets, 22, 9)