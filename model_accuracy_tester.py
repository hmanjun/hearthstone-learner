from ultralytics import YOLO
import csv
import cv2
import glob
import os

mouse_model = YOLO("./yolo_models/v1wneg_grayscaled.pt")
file_name = '12_seconds.MOV'

frame_dir = f'./output/frames/{file_name}'
frame_paths = sorted(glob.glob(os.path.join(frame_dir, '*.png')))

batch_img = []

for path in frame_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # Read as grayscale directly
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)   # Convert to 3-channel grayscale (YOLO expects 3 channels)
    batch_img.append(img)

#results = mouse_model(f'./output/frames/{file_name}/*.png')
results = mouse_model(batch_img)


num_fails = 0
num_total = 0

for res in results:
    num_total += 1

    if len(res.boxes) != 1:
        num_fails += 1
        continue

print(f"Total frames: {num_total}, num fails: {num_fails}, success rate: {100 - (num_fails / num_total) * 100:.2f}%")