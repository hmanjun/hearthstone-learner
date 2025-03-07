from ultralytics import YOLO
import os
import matplotlib.pyplot as plt

mouse_model = YOLO("./yolo_models/mouse_detection.pt")

file_name = 'demon_buy.MOV'
results = mouse_model(f'./output/frames/{file_name}/*.png')

prev_y = None

y0 = None
f0 = None

curr_frame = -1

curr_x = None
curr_y = None

# Start of siginificant movement (fine tune)
SIGNIFICANT_MOVEMENT = 49 # In pixels

clip_intervals = []

# Visualize mouse movement
x_framepoints = []
y_datapoints = []

for res in results:
    curr_frame += 1
    # Avoid false detections issue by ignoring frames with multiple detections
    if len(res.boxes) != 1:
        #print("Multiple mice detected in frame")
        continue
    
    x1, y1, x2, y2 = res.boxes[0].xyxy[0]
    curr_x = (x1 + x2) / 2
    curr_y = (y1 + y2) / 2

    x_framepoints.append(curr_frame)
    y_datapoints.append(curr_y)

    if prev_y != None and SIGNIFICANT_MOVEMENT < abs(curr_y - prev_y):
        #print(f"Significant movement detected! {curr_frame}, y = {curr_y}")
        if y0 == None:
            print(f"Start of significant movement at frame: {curr_frame}, y = {curr_y}")
            y0 = curr_x
            f0 = curr_frame
        else: 
            if abs(curr_y - y0) <= 30: # When mouse goes back to original position before movement (fine tune)
                print(f"Mouse returned: {curr_frame}, y = {curr_y}")
                clip_intervals.append((f0-1, curr_frame))
                y0 = None
                f0 = None
            
    else:
        if y0 != None: # When mouse stops accelerating
            print(f"Mouse stopped accelerating: {curr_frame}, y = {curr_y}")
            clip_intervals.append((f0-1, curr_frame))
            y0 = None
            f0 = None

    prev_y = curr_y

print(f'Clip intervals: {clip_intervals}, len: {len(clip_intervals)}')


# Visualize mouse movement in video

# Create a basic line plot
#"""
plt.plot(x_framepoints, y_datapoints, marker='o')  # 'o' adds markers at data points
plt.title('Mouse Y cord at each frame')
plt.xlabel('Frame')
plt.ylabel('Y-axis')
#"""

# Show the plot
plt.show()


# Create output folder
if not os.path.exists('./output/intervals'):
        os.makedirs('./output/intervals')

with open(f'./output/intervals/{file_name}.txt', "w") as file:
    for interval in clip_intervals:
        file.write(f"{interval[0]} {interval[1]}\n")

