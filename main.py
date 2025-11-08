import cv2
import time
import sys # For clean exit on error

# Import configuration and functionality from our modules
from config import CAMERA_INDEX, WINDOW_NAME, FONT, FONT_SCALE, TEXT_THICKNESS
from detector import process_frame_for_crowd # Imports the function AND initializes the YOLO model
from logic import evaluate_crowd_status

def main():
    """
    The main application loop for the Crowd-Reactive Traffic Control System.
    """
    
    # --- 1. INITIALIZE CAMERA ---
    cap = cv2.VideoCapture(CAMERA_INDEX)
    
    if not cap.isOpened():
        print(f"❌ Error: Cannot open video stream at index {CAMERA_INDEX}.")
        print("💡 HINT: Try changing the CAMERA_INDEX in config.py (e.g., to 0 or 2).")
        sys.exit(1)

    print("✅ Camera Stream Opened Successfully.")
    print("🚀 Starting real-time flow control monitoring...")
    
    start_time = time.time()
    frame_count = 0

    while True:
        # Read the current frame
        ret, frame = cap.read()

        if not ret:
            print("Stream ended or error reading frame.")
            break

        # --- 2. DETECTION CORE (Call to detector.py) ---
        # The detector handles model inference and returns the count.
        person_count, results = process_frame_for_crowd(frame)

        # --- 3. BUSINESS LOGIC (Call to logic.py) ---
        # The logic module determines status and logs changes.
        crowd_status, green_duration, status_color = evaluate_crowd_status(person_count)
        
        # --- 4. ANNOTATION AND DISPLAY ---
        
        # Render the boxes and make a Writable copy for drawing text (CRITICAL STEP!)
        annotated_frame = results.render()[0].copy()
        
        # Determine font scale for alerts
        status_scale = FONT_SCALE * (1.5 if crowd_status == "HIGH DENSITY" else 1.0)
        status_thickness = TEXT_THICKNESS + (1 if crowd_status == "HIGH DENSITY" else 0)

        # Line 1: Crowd Count
        count_text = f"Crowd Count: {person_count}"
        cv2.putText(annotated_frame, count_text, (10, 50), FONT, FONT_SCALE, (255, 255, 255), TEXT_THICKNESS, cv2.LINE_AA)
        
        # Line 2: Crowd Status
        status_text = f"STATUS: {crowd_status}"
        cv2.putText(annotated_frame, status_text, (10, 100), FONT, status_scale, status_color, status_thickness, cv2.LINE_AA)
        
        # Line 3: Calculated Duration (The Decision)
        duration_text = f"NEXT GREEN: {green_duration} SECONDS"
        cv2.putText(annotated_frame, duration_text, (10, 150), FONT, status_scale, status_color, status_thickness, cv2.LINE_AA)
        
        # Show the annotated frame
        cv2.imshow(WINDOW_NAME, annotated_frame)
        
        frame_count += 1
        
        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- CLEAN UP ---
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print("\n--- PERFORMANCE SUMMARY ---")
    print(f"Total frames processed: {frame_count}")
    if elapsed_time > 0:
        print(f"Average FPS: {frame_count / elapsed_time:.2f}")

    cap.release()
    cv2.destroyAllWindows()
    print("Stream closed. Cleanup complete. Data logged in crowd_control_log.csv.")


if __name__ == "__main__":
    # Ensure the required libraries are available
    try:
        main()
    except Exception as e:
        print(f"\nFATAL ERROR: Application failed to start. {e}")
        sys.exit(1)