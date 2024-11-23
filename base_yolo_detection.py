from ultralytics import YOLO
import cv2
import time

# Load the model
model = YOLO('computer_vision.pt')

# Open the webcam
cam = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    res, frame = cam.read()

    # Perform object detection on the frame
    results = model(frame)

    # Iterate over the detected objects
    for r in results:
        boxes = (r.boxes.xyxy).tolist()

        # Draw bounding boxes and labels for each detected object
        for box, conf, cls in zip(boxes, r.boxes.conf, r.boxes.cls):
            x1, y1, x2, y2 = map(int, box)
            label = model.names[int(cls)]
            confidence = round(conf.squeeze().item() * 100, 2)

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f'{label}: {confidence}%', (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

    # Display the frame
    cv2.imshow("frame", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cam.release()
cv2.destroyAllWindows()
