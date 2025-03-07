import cv2
import os

def split_video_to_frames(video_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    cap = cv2.VideoCapture(video_path)
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Rotate frame 90 degrees
        frame = cv2.transpose(frame)
        frame = cv2.flip(frame, flipCode=0) # Flip horizontally after transpose

        # Get new dimensions (after rotation)
        rotated_height, rotated_width = frame.shape[:2]

        frame_filename = os.path.join(output_folder, f'frame_{frame_count:04d}.png')

        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    cap.release()
    

file_name = 'demon_buy.MOV'
video_path = f'./data/videos/{file_name}'
output_folder = f'./output/frames/{file_name}'
split_video_to_frames(video_path, output_folder)