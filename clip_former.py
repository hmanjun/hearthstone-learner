import cv2
import os
import numpy as np

file_name = '12_seconds.MOV'
frames_folder = f'./output/frames/{file_name}'

os.makedirs(f'./output/clips/{file_name}', exist_ok=True)
output_folder = f'./output/clips/{file_name}'

clip_intervals = np.loadtxt(f'./output/clips/{file_name}/intervals/clip_intervals.txt', dtype=int)
print(f'clip_intervals: {clip_intervals}')

frames = sorted([f for f in os.listdir(frames_folder) if f.endswith('.png') or f.endswith('.jpg')])

first_frame = cv2.imread(os.path.join(frames_folder, frames[0]))
height, width, layers = first_frame.shape

fourcc = cv2.VideoWriter_fourcc(*'mp4v')

for clip in clip_intervals:
    output_video = f'{output_folder}/{clip}.MOV'
    video = cv2.VideoWriter(output_video, fourcc, 30, (width, height))

    start, end = clip
    print(f'start: {start}, end: {end}')
    for frame in frames[start:end]:
        img = cv2.imread(os.path.join(frames_folder, frame))
        video.write(img)
    
    video.release()

print("Finished")


