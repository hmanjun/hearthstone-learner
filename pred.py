from ultralytics import YOLO

model = YOLO("./yolo_models/v1wneg_best.pt")

file_name = '12_seconds.MOV'
#results = model(f'./output/frames/{file_name}/*.png')
results = model(f'./output/frames/{file_name}/frame_0420.png')

#print(f"Len results.boxes: {len(results[0].boxes)}")
#print(f"Len results: {len(results)}")
#print(f'Results: {results}')

#"""
for result in results:
    result.show()
#"""