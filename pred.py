from ultralytics import YOLO

model = YOLO("./yolo_models/mouse_detection.pt")


# results = model("./output/moues_with_backgrounds/validation/*.png")
results = model("./output/frames/demon_buy.MOV/frame_0013.png")

print(f"Len results.boxes: {len(results[0].boxes)}")

for result in results:
    result.show()