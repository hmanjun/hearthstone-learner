import os
import random
import shutil

# Define directories
image_dir = 'path/to/images/'
label_dir = 'path/to/labels/'

# Create new directories for splits
train_image_dir = 'path/to/train/images/'
val_image_dir = 'path/to/val/images/'
test_image_dir = 'path/to/test/images/'

train_label_dir = 'path/to/train/labels/'
val_label_dir = 'path/to/val/labels/'
test_label_dir = 'path/to/test/labels/'

# Create directories if they don't exist
for dir in [train_image_dir, val_image_dir, test_image_dir, train_label_dir, val_label_dir, test_label_dir]:
    os.makedirs(dir, exist_ok=True)

# List all images and labels
images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]  # Adjust to your image extension
labels = [f.replace('.jpg', '.txt') for f in images]  # Assuming labels are in .txt files

# Shuffle and split
random.seed(42)  # For reproducibility
random.shuffle(images)

# Define split proportions
train_ratio = 0.7
val_ratio = 0.2
test_ratio = 0.1

# Calculate the number of images for each set
train_size = int(len(images) * train_ratio)
val_size = int(len(images) * val_ratio)
test_size = len(images) - train_size - val_size

train_images = images[:train_size]
val_images = images[train_size:train_size+val_size]
test_images = images[train_size+val_size:]

# Function to copy images and labels to corresponding directories
def move_files(image_list, source_image_dir, source_label_dir, target_image_dir, target_label_dir):
    for image in image_list:
        label = image.replace('.jpg', '.txt')
        shutil.copy(os.path.join(source_image_dir, image), os.path.join(target_image_dir, image))
        shutil.copy(os.path.join(source_label_dir, label), os.path.join(target_label_dir, label))

# Move files to the respective directories
move_files(train_images, image_dir, label_dir, train_image_dir, train_label_dir)
move_files(val_images, image_dir, label_dir, val_image_dir, val_label_dir)
move_files(test_images, image_dir, label_dir, test_image_dir, test_label_dir)

print(f"Train: {len(train_images)} | Val: {len(val_images)} | Test: {len(test_images)}")
