import os
import numpy as np
import matplotlib.pyplot as plt
import csv

file_name = '12_seconds.MOV'
csv_path = f'./output/cordinates/{file_name}/mouse_cordinates.csv'
mouse_cordinates = []

with open(csv_path, 'r') as f:
    reader = csv.reader(f)
    next(reader)  # Skip the header
    mouse_cordinates = [(float(x), float(y)) if x and y else None for x, y in reader]

prev_y = None

dy0 = None
y0 = None
f0 = None

curr_frame = -1

curr_x = None
curr_y = None

idle = False

# Significant movement

clip_intervals = []

# Visualize mouse movement
x_framepoints = []
y_datapoints = []
dy_datapoints = [0,0]

def is_same_direction(initial_dy, current_dy):
    return (initial_dy > 0 and current_dy > 0) or (initial_dy < 0 and current_dy < 0) or (abs(current_dy) < 15)

def is_idle(y_datapoints, curr_y):
    return (abs(curr_y - y_datapoints[-30]) < 5) # If mouse hasnt moved in half second (60 frames:second)

for cord in mouse_cordinates:
    curr_frame += 1

    if cord == None: # Skip frames that don't have mouse data
        print(f'Skipping frame: {curr_frame}')
        continue

    curr_x, curr_y = cord

    x_framepoints.append(curr_frame)
    y_datapoints.append(curr_y)

    if prev_y == None: # Intialization on first frame
        prev_y = curr_y
        y0 = curr_y
        continue

    curr_dy = curr_y - prev_y

    if dy0 == None: # Intialization on second frame
        dy0 = curr_dy
        f0 = curr_frame
        prev_y = curr_y
        continue

    if curr_frame < 350:
        print(f'Frame: {curr_frame} ------------------------')
        print(f'y: {curr_y}, dy: {curr_dy}, y0: {y0}, dy0: {dy0}')

    if not is_same_direction(dy0, curr_dy):
        print(f'Changed directions ******************************')
        if abs(curr_y - y0) > 200: # Clip (Fine tune)
            clip_intervals.append((f0, curr_frame))
        y0 = prev_y
        dy0 = curr_dy
        f0 = curr_frame

    if len(y_datapoints) > 30:
        if is_idle(y_datapoints, curr_y):
            idle = True
        elif idle:
            print(f'broke idle state, curr_y:{curr_y}, y0: {y0}')
            if abs(curr_y - y0) > 180: # Clip (Fine tune)
                print(f'and clipped')
                clip_intervals.append((f0, curr_frame))
            y0 = prev_y
            dy0 = curr_dy
            f0 = curr_frame
            idle = False
        
    prev_y = curr_y

print(f'Clip intervals: {clip_intervals}, len: {len(clip_intervals)}')

os.makedirs(f'./output/clips/{file_name}/intervals', exist_ok=True)
np.savetxt(f'./output/clips/{file_name}/intervals/clip_intervals.txt', clip_intervals, fmt='%d')

# Visualize mouse movement in video

# Create a basic line plot
#"""
#plt.plot(x_framepoints, y_datapoints, marker='o')  # 'o' adds markers at data points
plt.plot(x_framepoints, y_datapoints, marker='o')
plt.title('Mouse Y cord at each frame')
plt.xlabel('Frame')
plt.ylabel('Y-axis')
#"""

# Show the plot
plt.show()