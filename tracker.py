import time
import math

class Vehicle:
    def __init__(self, id, bbox):
        self.id = id
        self.bbox = bbox
        self.centroid = self.compute_centroid(bbox)
        self.enter_time = time.time()
        self.inside_roi = True

    def update(self, bbox):
        self.bbox = bbox
        self.centroid = self.compute_centroid(bbox)

    def compute_centroid(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

    def get_wait_time(self):
        if self.inside_roi:
            return time.time() - self.enter_time
        return 0

class VehicleTracker:
    def __init__(self, roi, max_distance=50):
    	#created instance data members to track the vehicles based on the parameters required
        self.roi = roi
        self.max_distance = max_distance
        self.vehicles = {}
        self.next_id = 0

    def update(self, detections):
    	#declared an empty set to update the ids of each detected object 
        updated_ids = set()
        #iterating through the detections which contains list of boxes inside it so when we iterate we get a singleboxes for each objet
        for bbox in detections:
            #centroid describes the centre of the bounding boxes
            centroid = self.compute_centroid(bbox)
            #declared the initial_matchid is None
            matched_id = None
            for vid, vehicle in self.vehicles.items():
                dist = self.euclidean(centroid, vehicle.centroid)
                if dist < self.max_distance:
                    matched_id = vid
                    break
            if matched_id is not None:
                self.vehicles[matched_id].update(bbox)
                updated_ids.add(matched_id)
            else:
                new_vehicle = Vehicle(self.next_id, bbox)
                self.vehicles[self.next_id] = new_vehicle
                updated_ids.add(self.next_id)
                self.next_id += 1

        for vid, vehicle in self.vehicles.items():
            cx, cy = vehicle.centroid
            in_roi = self.inside_roi(cx, cy)
            vehicle.inside_roi = in_roi

    def inside_roi(self, x, y):
        x1, y1, x2, y2 = self.roi
        return x1 <= x <= x2 and y1 <= y <= y2

    def euclidean(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def compute_centroid(self, bbox):
        x1, y1, x2, y2 = bbox
        return ((x1 + x2) // 2, (y1 + y2) // 2)

