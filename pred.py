from ultralytics import YOLO

model = YOLO("./runs/detect/train3/weights/best.pt")


# results = model("./output/moues_with_backgrounds/validation/*.png")
results = model("./output/d2_frames/frame_0001.png")

print(f"Len results.boxes: {len(results[0].boxes)}")

for result in results:
    result.show()