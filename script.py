import cv2
import os
import numpy as np
from ultralytics import YOLO
import matplotlib.pyplot as plt


#Paths
VIDEO_PATH = './d2.MOV'
OUTPUT_FOLDER = './output/clips'

# Parameters
CLIP_LENGTH = 5  # Duration of the video clip in seconds
Y_TRANSLATION_THRESHOLD = 100  # Minimum vertical movement to trigger clipping
FPS = 20

# Create output folder
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

    # rotated_height, rotated_width = frame.shape[:2]

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
    
    x_framepoints.append(frame_count)
    y_datapoints.append(y)
    print(f"Mouse position at frame:{frame_count}, x:{x}, y:{y}")

    # Significant y translation is ~49 pixels in 1 frame
    
    """
    x1, y1, x2, y2 = res.boxes[0]
    x = (x1 + x2) / 2
    y = (y1 + y2) / 2"
    """
    

cap.release()

# Create a basic line plot
plt.plot(x_framepoints, y_datapoints, marker='o')  # 'o' adds markers at data points
plt.title('Mouse Y cord at each frame')
plt.xlabel('Frame')
plt.ylabel('Y-axis')

# Show the plot
plt.show()