from ultralytics import YOLO

model = YOLO("./yolo_models/mouse_detection.pt")

file_name = '12_seconds.MOV'
#results = model(f'./output/frames/{file_name}/*.png')
results = model(f'./output/frames/{file_name}/frame_0100.png')

#print(f"Len results.boxes: {len(results[0].boxes)}")
#print(f"Len results: {len(results)}")
#print(f'Results: {results}')

#"""
for result in results:
    result.show()
#"""