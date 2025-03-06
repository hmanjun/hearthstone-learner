import ultralytics
from ultralytics import YOLO

#ultralytics.checks()

#%pip install -q comet_ml
logger = 'Comet' #@param ['Comet', 'TensorBoard']
import comet_ml; comet_ml.init()

# Load COCO-pretrained YOLO11n model
#model = YOLO("yolo11m.pt") # or yolo11l.pt, yolo11n.pt (large, nano)

# Load custom YOLOv11 model
model = YOLO("./runs/detect/train/weights/best.pt")

# Additional training with resume flag
results = model.train(data="c:/Users/Harsh/Documents/CS Projects/hearthstone-learner/data/mouse_annotations/data.yaml", epochs=5, batch=16, verbose=True, resume=False)