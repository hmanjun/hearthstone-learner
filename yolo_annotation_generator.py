import os
import cv2
import numpy as np
from datetime import datetime

# Paths
#BASE_IMAGE_PATH = './data/images/base_background.png'
BASE_IMAGE_PATH = './data/images/358_back.png'
MOUSE_HOVER_IMAGE_PATH = './data/images/mouse_hover.png'
MOUSE_CLOSED_IMAGE_PATH = './data/images/mouse_closed.png'
VERSION = 'v4'
OUTPUT_DIR = f'./output/annotations/{VERSION}'
CLASS_ID = 0  # YOLO class ID for the mouse

# Load images
base_img = cv2.imread(BASE_IMAGE_PATH)
mouse_hover = cv2.imread(MOUSE_HOVER_IMAGE_PATH, cv2.IMREAD_UNCHANGED)
mouse_closed = cv2.imread(MOUSE_CLOSED_IMAGE_PATH, cv2.IMREAD_UNCHANGED)

# Get dimensions
base_h, base_w, _ = base_img.shape
mouse_h, mouse_w, _ = mouse_hover.shape

# Define placement range
x_start, x_end = 369, 1540
y_start, y_end = 68, 860

# Define split proportions
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Calculate the number of images for each set
step = 100
total_images = ((x_end - x_start) // step + 1) * ((y_end - y_start) // step + 1) * 2
train_size = int(total_images * train_ratio)
val_size = int(total_images * val_ratio)
test_size = total_images - train_size - val_size
current_image = 0

# Ensure output directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
#os.makedirs(os.path.join(OUTPUT_DIR, "images"), exist_ok=True)
#os.makedirs(os.path.join(OUTPUT_DIR, "labels"), exist_ok=True)

# Function to overlay mouse image and save
def overlay_and_save(mouse_img, x, y, suffix, current_image):
    file_prefix = datetime.now().strftime("%Y%m%d_%H%M%S")
    combined_img = base_img.copy()

    if x + mouse_w > base_w or y + mouse_h > base_h:
        return

    alpha_channel = mouse_img[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha_channel

    #"""
    output_folder = ''
    if current_image <= train_size:
        output_folder = f'{OUTPUT_DIR}/train'
    elif train_size < current_image <= train_size + val_size:
        output_folder = f'{OUTPUT_DIR}/valid'
    else:
        output_folder = f'{OUTPUT_DIR}/test'

    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(os.path.join(output_folder, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "labels"), exist_ok=True)
    #"""
    #output_folder = f'{OUTPUT_DIR}/train'


    for c in range(3):
        combined_img[y:y+mouse_h, x:x+mouse_w, c] = (
            mouse_img[:, :, c] * alpha_channel +
            combined_img[y:y+mouse_h, x:x+mouse_w, c] * alpha_inv
        )

    img_filename = f"{file_prefix}_{x}_{y}_{suffix}.png"
    cv2.imwrite(f'{output_folder}/images/{img_filename}', combined_img)

    x_center = (x + mouse_w / 2) / base_w
    y_center = (y + mouse_h / 2) / base_h
    w_norm = mouse_w / base_w
    h_norm = mouse_h / base_h

    label_filename = f"{file_prefix}_{x}_{y}_{suffix}.txt"
    with open(os.path.join(output_folder, "labels", label_filename), "w") as f:
        f.write(f"{CLASS_ID} {x_center:.6f} {y_center:.6f} {w_norm:.6f} {h_norm:.6f}\n")

    print(f"Saved image: {img_filename} and label: {label_filename}")

# Generate images and annotations
for x in range(x_start, x_end + 1, step):
    for y in range(y_start, y_end + 1, step):
        current_image += 1
        overlay_and_save(mouse_hover, x, y, "hover", current_image)
        current_image += 1
        overlay_and_save(mouse_closed, x, y, "closed", current_image)

print("Finished generating images and labels!")
