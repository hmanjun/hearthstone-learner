import os
import cv2
import numpy as np
from datetime import datetime
import random

# Paths
#BASE_IMAGE_PATH = './data/images/base_background.png'
BASE_IMAGE_PATH = './data/images/clear_back.png'
MINIONS_IMAGE_PATH = './data/images/minions'
VERSION = 'v4'
OUTPUT_DIR = f'./output/annotations/{VERSION}'
num_to_generate = 100

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all image file names
minions_files = [f for f in os.listdir(MINIONS_IMAGE_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
minions_images = [cv2.imread(os.path.join(MINIONS_IMAGE_PATH, img)) for img in minions_files]

base_img = cv2.imread(BASE_IMAGE_PATH)

# Get dimensions
base_h, base_w, _ = base_img.shape


def overlay_and_save(minions_images, base, save_location, img_num):
    file_suffix = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = base_img.copy()
    
    # Define placement range
    shop_x_start, shop_x_end = 624, 1200

    board_x_start, board_x_end = 550, 1200

    #Add shop minions
    x,y = shop_x_start, 245
    ran_num = random.randint(1, 6)

    for i in range(ran_num):
        if x > shop_x_end:
            break

        add_img = minions_images[random.randint(0, len(minions_images)-1)]

        minion_h, minion_w, _ = add_img.shape

        base[y:y+minion_h, x:x+minion_w] = add_img
        x += 103 + 20


    #Add tavern minions
    x,y = board_x_start, 420
    ran_num = random.randint(1, 7)

    for i in range(ran_num):
        if x > board_x_end:
            break

        add_img = minions_images[random.randint(0, len(minions_images)-1)]

        minion_h, minion_w, _ = add_img.shape

        base[y:y+minion_h, x:x+minion_w] = add_img
        x += 103 + 20


    img_filename = f"negative_{img_num}_{file_suffix}.png"
    cv2.imwrite(f'{save_location}/images/{img_filename}', base)

    with open(f"{save_location}/labels/{img_filename}.txt", "w") as file:
        pass  # Creates an empty file
    
    print(f"Saved image: {img_filename} and label: {img_filename}.txt")


# Define split proportions
train_ratio = 0.4
val_ratio = 0.3
test_ratio = 0.3

train_size = int(num_to_generate * train_ratio)
val_size = int(num_to_generate * val_ratio)
test_size = num_to_generate - train_size - val_size

current_image = 0

while current_image < num_to_generate:
    output_folder = ''
    if current_image <= train_size:
        output_folder = f'{OUTPUT_DIR}/train'
    elif train_size < current_image <= train_size + val_size:
        output_folder = f'{OUTPUT_DIR}/valid'
    else:
        output_folder = f'{OUTPUT_DIR}/test'

    overlay_and_save(minions_images, base_img, output_folder, current_image)
    current_image += 1