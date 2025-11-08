import cv2

# --- CAMERA & DISPLAY CONFIGURATION ---
CAMERA_INDEX = 0  # Index for your webcam (try 0 or 2 if 1 fails)
WINDOW_NAME = 'YOLOv5 Public Density Monitor'

# OpenCV Display Text Parameters
FONT = cv2.FONT_HERSHEY_DUPLEX
FONT_SCALE = 1.0
TEXT_THICKNESS = 2

# --- YOLOv5 DETECTION CONFIGURATION ---
YOLO_MODEL = 'yolov5s' # The model to load (e.g., yolov5n, yolov5m, etc.)
# PERSON_CLASS_ID = 0    # Class ID for 'person' in the COCO dataset
INFERENCE_SIZE = 640   # Image size used for model detection

# --- TRAFFIC LIGHT LOGIC (Fixed Cycle) ---
DEFAULT_GREEN_DURATION_S = 7
THRESHOLD_LOW_CROWD_X = 3  # Count <= X is LOW (triggers 6s green)
THRESHOLD_HIGH_CROWD_Y = 7 # Count > Y is HIGH (triggers 9s green)
DURATION_INCREMENT_S = 2   # Duration increase for HIGH density
DURATION_DECREMENT_S = 1   # Duration decrease for LOW density

# --- LOGGING CONSTANTS ---
LOG_FILE = 'crowd_control_log.csv'