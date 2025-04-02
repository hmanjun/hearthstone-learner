import os
import cv2
import numpy as np
from datetime import datetime
import random

# Paths
#BASE_IMAGE_PATH = './data/images/base_background.png'
BASE_IMAGE_PATH = './data/images/clear_back.png'
MINIONS_IMAGE_PATH = './data/images/minions'
VERSION = 'negatives_v1'
OUTPUT_DIR = f'./output/annotations/{VERSION}'
file_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Get all image file names
minions_files = [f for f in os.listdir(MINIONS_IMAGE_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
minions_images = [cv2.imread(os.path.join(MINIONS_IMAGE_PATH, img)) for img in minions_files]

base_img = cv2.imread(BASE_IMAGE_PATH)

# Get dimensions
base_h, base_w, _ = base_img.shape

# Define placement range
shop_x_start, shop_x_end = 624, 1200

board_x_start, board_x_end = 550, 1200

x,y = shop_x_start, 245
for i in range(random.randint(1,6)):
    if x > shop_x_end:
        break

    add_img = minions_images[random.randint(0, len(minions_images))]
    #print(f"len: {len(add_img)}, shape: {add_img.shape}")
    minion_h, minion_w, _ = add_img.shape

    alpha_channel = add_img[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha_channel

    for c in range(3):
        base_img[y:y+minion_h, x:x+minion_w, c] = (
            add_img[:, :, c] * alpha_channel +
            base_img[y:y+minion_h, x:x+minion_w, c] * alpha_inv
        )

img_filename = f"negative.png"
cv2.imwrite(f'{OUTPUT_DIR}/images/{img_filename}', base_img)

