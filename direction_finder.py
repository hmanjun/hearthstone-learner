import os
import matplotlib.pyplot as plt
import csv

file_name = 'slow_buy.MOV'
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

# Significant movement

clip_intervals = []

# Visualize mouse movement
x_framepoints = []
y_datapoints = []
dy_datapoints = [0,0]

def is_same_direction(initial_dy, current_dy):
    #print(f'is_same_direction result @frame {curr_frame}, {(initial_dy > 0 and current_dy > 0)} {(initial_dy < 0 and current_dy < 0)} {abs(current_dy - initial_dy) < 15}')
    """
    if 0 < curr_frame < 25:
        print(f'y: {curr_y} frame: {curr_frame}, initial_dy: {initial_dy}, current_dy: {current_dy}')
    #"""
    return (initial_dy > 0 and current_dy > 0) or (initial_dy < 0 and current_dy < 0) or (abs(current_dy) < 15)

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
    """
    if curr_dy > 0:
        dy_datapoints.append(1)
    else:
        dy_datapoints.append(-1)
    #"""
    #dy_datapoints.append(curr_dy)

    """
    if curr_frame > 416:
        print(f'Frame: {curr_frame}, dy: {curr_dy}, y: {curr_y}')
    #"""

    if dy0 == None: # Intialization on second frame
        #print(f'setting dy0 to {curr_dy} @frame {curr_frame}')
        dy0 = curr_dy
        f0 = curr_frame
        prev_y = curr_y
        continue

    """
    pivot = is_same_direction(dy0, curr_dy)
    if pivot:
        dy_datapoints.append(1)
    else:
        dy_datapoints.append(-1)
    #"""

    if curr_frame < 350:
        print(f'Frame: {curr_frame} ------------------------')
        print(f'y: {curr_y}, dy: {curr_dy}, y0: {y0}, dy0: {dy0}')

    if not is_same_direction(dy0, curr_dy):
        #print(f'Changed directions at frame: {curr_frame}, dy0: {dy0}, curr_dy: {curr_dy}')
        print(f'Changed directions ******************************')
        if abs(curr_y - y0) > 200: # Clip (Fine tune)
            #print(f'Clipped******************************')
            #print(f'Clip ({f0},{curr_frame}), curr_y: {curr_y}, y0: {y0}, dy0: {dy0}, curr_dy: {curr_dy}')
            clip_intervals.append((f0, curr_frame))
        y0 = prev_y
        dy0 = curr_dy
        f0 = curr_frame


    prev_y = curr_y

print(f'Clip intervals: {clip_intervals}, len: {len(clip_intervals)}')

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