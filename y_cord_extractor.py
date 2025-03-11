from ultralytics import YOLO
import csv
import os

mouse_model = YOLO("./yolo_models/mouse_detection.pt")


file_name = 'slow_buy.MOV'
output_folder = f'./output/cordinates/{file_name}'
results = mouse_model(f'./output/frames/{file_name}/*.png')

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

mouse_cordinates = []

for res in results:

    # Set failed and multiple detection with None
    if len(res.boxes) != 1:
        mouse_cordinates.append((None, None))
        continue

    x1, y1, x2, y2 = res.boxes[0].xyxy[0]
    
    x = float((x1 + x2) / 2)
    y = float((y1 + y1) / 2)

    mouse_cordinates.append((x,y))

csv_path = os.path.join(output_folder, 'mouse_cordinates.csv')

with open(csv_path, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['x', 'y'])
    writer.writerows(mouse_cordinates)


