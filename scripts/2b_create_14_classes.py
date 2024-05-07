import os
import random
import shutil

categories = [0, 2, 3, 6, 7, 8, 10, 11, 14, 15, 16, 17, 19, 22]

all_labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/26_classes/labels'
train_labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/train/labels/'
# test_labels_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/test/labels/'
random.seed(42)

#copy labels
print('Copying labels to training folder...')
for c in categories:
    print(f'... copying labels from category {c} ...')
    images_list = []
    for text in os.listdir(all_labels_dir):
        #get category label from text files
        with open(os.path.join(all_labels_dir, text)) as f:
            for line in f:
                cat = int(line.split(' ')[0])
                # print(cat)
        if cat == c:
            images_list.append(text)
    print(f'image_list length = {len(images_list)}')
    #copying
    samples = random.sample(images_list, 1000)
    print(f'samples length = {len(samples)}')
    print(f'... copying labels for category {c} to train folder ...')
    for sample in samples:
        src_dir = os.path.join(all_labels_dir, sample)
        dst_dir = os.path.join(train_labels_dir, sample)
        # print(f'... copying {sample} ...')
        shutil.copy(src_dir, dst_dir)
    print(f'done!')
    # print(f'... copying labels for category {c} to test folder ...')
    # for sample in samples[1000:]:
    #     src_dir = os.path.join(all_labels_dir, sample)
    #     dst_dir = os.path.join(test_labels_dir, sample)
    #     # print(f'... copying {sample} ...')
    #     shutil.copy(src_dir, dst_dir)
    # print(f'... labels for category {c} copied to testing folder!')
    # print(f'done!')
print('all labels copied!')

#copy images
all_images_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/26_classes/images/'
train_images_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/train/images/'
# test_images_dir = '/media/jess/DATA/PhD/data/ecoflow/yolo_labels/14_classes/test/images/'

print('Copying images to training folder...')
for label in os.listdir(train_labels_dir):
    image_name = label.split('.')[0]+'.jpg'
    image_src_dir = os.path.join(all_images_dir, image_name)
    image_dst_dir = os.path.join(train_images_dir, image_name)
    # print(f'... copying {image_name} ...')
    shutil.copy(image_src_dir, image_dst_dir)
# print('Copying images to testing folder...')
# for label in os.listdir(test_labels_dir):
#     image_name = label.split('.')[0]+'.jpg'
#     image_src_dir = os.path.join(all_images_dir, image_name)
#     image_dst_dir = os.path.join(test_images_dir, image_name)
#     # print(f'... copying {image_name} ...')
#     shutil.copy(image_src_dir, image_dst_dir)
print('done!')