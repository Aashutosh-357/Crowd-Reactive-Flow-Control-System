import cv2

# Change the stream_url to the index number 0
stream_index = 0  # This should be your laptop's built-in camera

cap = cv2.VideoCapture(stream_index) 

if not cap.isOpened():
    print("Error: Could not open laptop camera at index 0. Try index 1.")
    exit()
    
print("Success! Reading laptop camera stream. Press 'q' to close.")

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    cv2.putText(frame, "Stream Active!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Live Test Feed", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()