import cv2

# Initialize a list of trackers
trackers = cv2.MultiTracker_create()

# Read the video
video = cv2.VideoCapture("./video-data/Sakri Dengarours Road Accident Live CCTV Footage.mp4")

# Read the first frame
ret, frame = video.read()
if not ret:
    print("Failed to read video")

# Initialize tracking objects on the first frame
# Replace bbox with the bounding boxes detected by your motion detection
for bbox in bboxes:
    tracker = cv2.TrackerKCF_create()
    trackers.add(tracker, frame, bbox)

while video.isOpened():
    ret, frame = video.read()
    if not ret:
        break

    # Update the tracking result
    success, boxes = trackers.update(frame)

    # Draw the tracked objects
    for box in boxes:
        (x, y, w, h) = [int(v) for v in box]
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the frame
    cv2.imshow('Tracking', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video.release()
cv2.destroyAllWindows()
