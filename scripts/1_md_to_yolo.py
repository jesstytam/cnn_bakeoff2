import json
from collections import defaultdict

#load md results
coco_path = '/media/jess/DATA/PhD/cnn_bakeoff2/data/raw/coco_camera_trap.json'
coco = json.load(open(coco_path))

#create a list to store a refined version of results
md_results = []

for im in coco['images']:
    for an in coco['annotations']:
        if im['id']==an['id']:
            new_file_name = im['file_name'].split('/')[-1]
            category_id = an['category_id']
            bbox = an['bbox']
            print(f'Appending {new_file_name}...')
            md_results.append({'file':new_file_name,
                               'category_id':category_id,
                               'bbox':bbox})
            print('done!')

#save the list
print('Saving cleaned megadetector results...')
save_path = '/media/jess/DATA/PhD/cnn_bakeoff2/data/raw/md_results.json'
with open(save_path, 'w') as file:
    json.dump(md_results, file, indent=4)
print('done!')

#create yolo files
def md_to_yolo(bbox, img_width=2048, img_height=1536): 
    x, y, w, h = bbox
    x_centre = (x + w / 2.0) / img_width
    y_centre = (y + h / 2.0) / img_height
    w = w / img_width
    h = h / img_height
    return [x_centre, y_centre, w, h]

# Group labels by file
labels_by_file = defaultdict(list)
for d in md_results:
    labels_by_file[d['file']].append(d)

labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/26_classes/labels/'

print('Creating YOLO labels...')
for file_name, annotations in labels_by_file.items():
    new_filename = file_name.split('.')[0]
    text_file_path = labels_dir+new_filename+'.txt'
    with open(text_file_path, 'w') as file:
        for annotation in annotations:
            new_cat = annotation['category_id']-1
            new_box = md_to_yolo(annotation['bbox'])
            file.write(f'{new_cat} {new_box[0]} {new_box[1]} {new_box[2]} {new_box[3]}\n')
print('done!')