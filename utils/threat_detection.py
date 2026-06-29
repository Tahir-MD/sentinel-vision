"""
Advanced Threat Detection for Sentinel Vision Pro
Created by: Tahir Mahmood
Year: 2026
"""

import cv2
import numpy as np
import random
from collections import deque

class SecurityThreatDetector:
    """
    Advanced threat detection using multiple AI models
    """

    def __init__(self):
        # Use only CSRT and KCF (most stable, widely available)
        self.trackers = {
            'csrt': cv2.TrackerCSRT_create(),
            'kcf': cv2.TrackerKCF_create()
        }
        self.tracking_history = {}
        self.detection_history = deque(maxlen=100)

    def detect_motion(self, frame, prev_frame):
        """Detect motion using frame differencing"""
        if prev_frame is None:
            return []

        diff = cv2.absdiff(frame, prev_frame)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motions = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                motions.append({
                    'bbox': (x, y, w, h),
                    'area': area,
                    'confidence': min(1.0, area / 2000)
                })

        return motions

    def detect_background_subtraction(self, frame, bg_subtractor):
        """Detect foreground using background subtraction"""
        fgmask = bg_subtractor.apply(frame)
        fgmask = cv2.medianBlur(fgmask, 5)
        contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        detections = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 500:
                x, y, w, h = cv2.boundingRect(contour)
                detections.append({
                    'bbox': (x, y, w, h),
                    'area': area,
                    'type': 'foreground'
                })

        return detections

    def track_objects(self, frame, detections):
        """Track detected objects across frames"""
        tracked = []

        for detection in detections:
            bbox = detection['bbox']
            # Use CSRT tracker (more accurate) or KCF (faster)
            tracker_name = 'csrt' if len(self.tracking_history) % 2 == 0 else 'kcf'
            tracker = self.trackers[tracker_name]

            try:
                # Ensure bbox is in correct format
                bbox_tuple = tuple(bbox) if isinstance(bbox, (list, tuple)) else bbox
                tracker.init(frame, bbox_tuple)

                tracked.append({
                    'bbox': bbox,
                    'tracker': tracker_name,
                    'id': len(self.tracking_history) + 1
                })
            except Exception as e:
                print(f"Tracker error: {e}")
                continue

        return tracked

def detect_with_vit(frame):
    """
    Vision Transformer based threat detection
    """
    threats = []

    # Simulate detection with random probability
    if random.random() > 0.85:
        threats.append({
            'type': 'surveillance_camera',
            'confidence': random.uniform(0.7, 0.95),
            'location': (random.randint(0, 100), random.randint(0, 100))
        })

    return threats

def detect_with_yolo(frame):
    """
    YOLO based object detection
    """
    detections = []

    # Simulate detections
    if random.random() > 0.7:
        detections.append({
            'class': 'person',
            'confidence': random.uniform(0.8, 0.99),
            'bbox': [
                random.randint(50, 200),
                random.randint(50, 200),
                random.randint(50, 150),
                random.randint(100, 250)
            ]
        })

    if random.random() > 0.9:
        detections.append({
            'class': 'cell phone',
            'confidence': random.uniform(0.7, 0.9),
            'bbox': [
                random.randint(300, 500),
                random.randint(100, 300),
                random.randint(30, 60),
                random.randint(50, 100)
            ]
        })

    return detections

def track_objects(frame, detections):
    """
    Track multiple objects in real-time
    """
    try:
        # Use CSRT tracker (available in most OpenCV versions)
        tracker = cv2.TrackerCSRT_create()
    except:
        # Fallback to KCF
        tracker = cv2.TrackerKCF_create()

    tracked_objects = []
    for detection in detections:
        bbox = detection.get('bbox')
        if bbox:
            try:
                bbox_tuple = tuple(bbox) if isinstance(bbox, (list, tuple)) else bbox
                tracker.init(frame, bbox_tuple)
                tracked_objects.append({
                    'bbox': bbox,
                    'tracker': 'csrt',
                    'id': random.randint(1000, 9999)
                })
            except Exception:
                continue

    return tracked_objects

def multi_model_detection(frame):
    """
    Combine multiple detection models
    """
    # Initialize background subtractors
    mog2 = cv2.createBackgroundSubtractorMOG2()
    knn = cv2.createBackgroundSubtractorKNN()

    # Run multiple models
    mog2_mask = mog2.apply(frame)
    knn_mask = knn.apply(frame)

    # Combine results
    combined = cv2.bitwise_or(mog2_mask, knn_mask)

    # Count detections
    contours, _ = cv2.findContours(combined, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detections = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:
            x, y, w, h = cv2.boundingRect(contour)
            detections.append({
                'bbox': (x, y, w, h),
                'area': area,
                'models': ['MOG2', 'KNN']
            })

    return detections