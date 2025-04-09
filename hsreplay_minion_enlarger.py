import os
from PIL import Image

# Folder containing the images
input_folder = './data/images/minions'
output_folder = './data/images/resized_minions'

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Resize factor
resize_factor = 1.09  # 9% increase

# Supported image extensions
image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff']

# Process each image
for filename in os.listdir(input_folder):
    if any(filename.lower().endswith(ext) for ext in image_extensions):
        img_path = os.path.join(input_folder, filename)
        with Image.open(img_path) as img:
            # Compute new dimensions
            new_width = int(img.width * resize_factor)
            new_height = int(img.height * resize_factor)
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            # Save resized image
            output_path = os.path.join(output_folder, filename)
            resized_img.save(output_path)
            print(f"Resized {filename} to {new_width}x{new_height}")