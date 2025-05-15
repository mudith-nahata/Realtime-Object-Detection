import cv2

def draw_overlay(frame, roi, vehicle_data):
    cv2.rectangle(frame, (roi[0], roi[1]), (roi[2], roi[3]), (255, 0, 0), 2)
    for v in vehicle_data.values():
        if v.inside_roi:
            x1, y1, x2, y2 = v.bbox
            wait_time = format_time(v.get_wait_time())
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, f"ID:{v.id} WT:{wait_time}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

def format_time(seconds):
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02}:{seconds:02}"

