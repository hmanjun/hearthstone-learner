import os
import cv2
import numpy as np
import random

# Paths
BASE_IMAGE_PATH = './data/images/base_background.png'
MOUSE_HOVER_IMAGE_PATH = './data/images/mouse_hover.png'
MOUSE_CLOSED_IMAGE_PATH = './data/images/mouse_closed.png'
VERSION = 'v1'
OUTPUT_FOLDER = f'./output/annotations/{VERSION}'
CLASS_ID = 0

# Load images
base_image = cv2.imread(BASE_IMAGE_PATH)
mouse_hover = cv2.imread(MOUSE_HOVER_IMAGE_PATH)
mouse_closed = cv2.imread(MOUSE_CLOSED_IMAGE_PATH)

# Get dimensions
base_h, base_w, _ = base_image.shape
mouse_h, mouse_w, _ = mouse_hover.shape

# Top Left cornor (369, 68)
# Bottomr Right cornor (1540, 860)

# Ensure output directories exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(os.path.join(OUTPUT_FOLDER, "images"), exist_ok=True)
os.makedirs(os.path.join(OUTPUT_FOLDER, "labels"), exist_ok=True)

# Generate images and annotations
for i in range(369, 1541):
    for j in range(68, 861):
        # Copy base image
        img = base_image.copy()

        # Paste mouse image
        img[j:j+mouse_h, i:i+mouse_w] = mouse_hover

        # Save image
        img_path = os.path.join(OUTPUT_FOLDER, "images", f"{i}_{j}.png")
        cv2.imwrite(img_path, img)

        # Save annotation
        label_path = os.path.join(OUTPUT_FOLDER, "labels", f"{i}_{j}.txt")
        with open(label_path, 'w') as f:
            f.write(f"{CLASS_ID} {i + mouse_w/2} {j + mouse_h/2} {mouse_w} {mouse_h}\n")
        
        print(f"Saved image: {img_path} and label: {label_path}")

