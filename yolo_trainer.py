import ultralytics
from ultralytics import YOLO

#ultralytics.checks()

#%pip install -q comet_ml
logger = 'Comet' #@param ['Comet', 'TensorBoard']
import comet_ml; comet_ml.init()

# Load COCO-pretrained YOLO11n model
model = YOLO("yolo11n.pt") # or yolo11l.pt, yolo11n.pt (large, nano)

# Load custom YOLOv11 model
#model = YOLO("./runs/detect/train4/weights/best.pt")
#model = YOLO("./yolo11n.pt")

# Additional training with resume flag
results = model.train(data="c:/Users/Harsh/Documents/CS Projects/hearthstone-learner/output/annotations/v1/data.yaml", epochs=2, batch=16, verbose=True, resume=False)