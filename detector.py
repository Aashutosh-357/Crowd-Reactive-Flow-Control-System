import torch
import cv2
import pandas as pd
from config import YOLO_MODEL, INFERENCE_SIZE # Just import PERSON_CLASS_ID for person

# Load the YOLOv5 model globally so it's only done once when the script starts
try:
    # Use torch.hub.load to fetch the model (it caches the weights)
    yolo_model = torch.hub.load('ultralytics/yolov5', YOLO_MODEL, pretrained=True)
    
    # Filter detections to only target the 'person' class (ID 0)
    # yolo_model.classes = [PERSON_CLASS_ID] # For person only
    
    # For all objects
    # if hasattr(yolo_model, 'classes'):
    #     del yolo_model.classes
    yolo_model.conf = 0.25
    print(f"✅ AI Detector Loaded: YOLOv5 '{YOLO_MODEL}' is ready.")
except Exception as e:
    print(f"❌ Error loading YOLOv5 model: {e}")
    # Raise the exception to stop the entire application, as the core functionality is missing
    raise

def process_frame_for_crowd(frame: cv2.Mat) -> tuple[int, pd.DataFrame]:
    """
    Runs YOLOv5 inference on a single frame and calculates the crowd count.

    Args:
        frame: A single frame (NumPy array) from the video stream.

    Returns:
        A tuple containing:
        1. The total count of people detected (int).
        2. The full detection results (pandas DataFrame) for later annotation.
    """
    # 1. Run Inference
    # The model handles resizing, normalization, and detection automatically
    results = yolo_model(frame, size=INFERENCE_SIZE)
    
    # 2. Extract Data
    # Get the raw predictions for the first image (index 0) in the batch
    detections = results.pandas().xyxy[0]   
    
    # 3. Calculate Count
    # Since we set model.classes = [0], the DataFrame only contains people.
    # We double-check the 'name' column for robustness, though it's technically filtered.
    # person_count = len(detections[detections['name'] == 'person']) # Detects only person
    object_count = len(detections) # Detects all objects
    
    # 4. Return results and the raw output object (for rendering bounding boxes later)
    return object_count, results