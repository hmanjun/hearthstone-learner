import cv2
import os
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt


#Paths
VIDEO_FILE = 'double_sell.MOV'
VIDEO_PATH = f'./data/videos/{VIDEO_FILE}'
OUTPUT_FOLDER = f'./output/clips/{VIDEO_FILE}'

# Parameters
CLIP_LENGTH = 2  # Duration of the video clip in seconds
Y_TRANSLATION_THRESHOLD = 100  # Minimum vertical movement to trigger clipping
#FPS = 20

# Create output folder
if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)

# Open video
cap = cv2.VideoCapture(VIDEO_PATH)
fps = int(cap.get(cv2.CAP_PROP_FPS))
CLIP_FRAMES = CLIP_LENGTH * fps

# Initialize YOLO
mouse_detection_model = YOLO("./yolo_models/mouse_detection.pt")

# Track moouse Y postion
prev_y = None
clip_count = 0
out = None
frame_count = 0

x_framepoints = []
y_datapoints = []

while cap.isOpened():

    ret, frame = cap.read()
    if not ret:
        break
    
    frame_count += 1

    # Rotate frame 90 degrees
    frame = cv2.transpose(frame)
    frame = cv2.flip(frame, flipCode=0) # Flip horizontally after transpose
    rotated_height, rotated_width = frame.shape[:2]

    # Find mouse in frame
    results = mouse_detection_model(frame)
    res = results[0]

    # Avoid false detections issue by ignoring frames with multiple detections
    if len(res.boxes) != 1:
        print("Multiple mice detected in frame")
        continue

    # Get mouse x,y position (Note: top-left corner is 0,0)
    x = None
    y = None
    for box in res.boxes:
        x1, y1, x2, y2 = box.xyxy[0]
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

    # Detect significant y translation
    if prev_y != None and 49 <= abs(y - prev_y) < 100:
        if out:
            out.release()

        clip_count += 1
        clip_filename = os.path.join(OUTPUT_FOLDER, f"clip_{clip_count:03d}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        # Create VideoWriter with the rotated frame dimensions
        out = cv2.VideoWriter(clip_filename, fourcc, fps, (rotated_width, rotated_height))

        # Write frames for the clip
        for _ in range(CLIP_FRAMES):
            ret, frame = cap.read()
            if not ret:
                break
            # Apply 90-degree rotation for each frame
            frame = cv2.transpose(frame)
            frame = cv2.flip(frame, flipCode=0)  # Apply 90-degree rotation
            out.write(frame)
        out.release()

    prev_y = y
    


    # Visualize mouse movement in video
    """
    x_framepoints.append(frame_count)
    y_datapoints.append(y)
    print(f"Mouse position at frame:{frame_count}, x:{x}, y:{y}")

    # Significant y translation is ~49 pixels in 1 frame
    """

    
    """
    x1, y1, x2, y2 = res.boxes[0]
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2"
    """
    

cap.release()
if out:
    out.release()

# Visualize mouse movement in video
"""
# Create a basic line plot
plt.plot(x_framepoints, y_datapoints, marker='o')  # 'o' adds markers at data points
plt.title('Mouse Y cord at each frame')
plt.xlabel('Frame')
plt.ylabel('Y-axis')

# Show the plot
plt.show()
"""