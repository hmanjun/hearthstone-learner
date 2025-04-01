import os
import cv2
import numpy as np
from datetime import datetime

# Paths
#BASE_IMAGE_PATH = './data/images/base_background.png'
BASE_IMAGE_PATH = './data/images/358_back.png'
MOUSE_HOVER_IMAGE_PATH = './data/images/mouse_hover.png'
MOUSE_CLOSED_IMAGE_PATH = './data/images/mouse_closed.png'
VERSION = 'v3'
OUTPUT_DIR = f'./output/annotations/{VERSION}'
CLASS_ID = 0  # YOLO class ID for the mouse