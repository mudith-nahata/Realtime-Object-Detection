import cv2
from ultralytics import YOLO
from tracker import VehicleTracker
from utils import draw_overlay

def main():
    video_path = 'input_video.mp4'
    output_path = 'output_video.mp4'
    roi = (465, 248, 1024, 1024)  # Define your ROI here

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    model = YOLO('yolov8s.pt')
    tracker = VehicleTracker(roi)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (1020, 500))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        detections = []
        for box in results[0].boxes:
            cls_id = int(box.cls[0])
            if cls_id == 2:  # Class ID 2 is 'car' in COCO dataset
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                detections.append([x1, y1, x2, y2])

        tracker.update(detections)
        draw_overlay(frame, roi, tracker.vehicles)
        out.write(frame)

        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

