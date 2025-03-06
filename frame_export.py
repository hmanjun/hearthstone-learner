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
    

video_path = './d2.MOV'
output_folder = './output/d2_frames'
split_video_to_frames(video_path, output_folder)