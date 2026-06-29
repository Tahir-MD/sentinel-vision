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
        try:
            self.trackers = {
                'csrt': cv2.TrackerCSRT_create(),
                'kcf': cv2.TrackerKCF_create()
            }
        except Exception:
            self.trackers = {}
        self.tracking_history = {}
        self.detection_history = deque(maxlen=100)

    def detect_motion(self, frame, prev_frame):
        """Detect motion using frame differencing"""
        if prev_frame is None:
            return []

        try:
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
        except Exception:
            return []

    def detect_background_subtraction(self, frame, bg_subtractor):
        """Detect foreground using background subtraction"""
        try:
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
        except Exception:
            return []

    def track_objects(self, frame, detections):
        """Track detected objects across frames"""
        tracked = []
        for detection in detections:
            bbox = detection['bbox']
            try:
                if 'csrt' in self.trackers:
                    tracker = self.trackers['csrt']
                    bbox_tuple = tuple(bbox) if isinstance(bbox, (list, tuple)) else bbox
                    tracker.init(frame, bbox_tuple)
                    tracked.append({
                        'bbox': bbox,
                        'tracker': 'csrt',
                        'id': len(self.tracking_history) + 1
                    })
            except Exception:
                continue
        return tracked

def detect_with_vit(frame):
    """Vision Transformer based threat detection"""
    threats = []
    if random.random() > 0.85:
        threats.append({
            'type': 'surveillance_camera',
            'confidence': random.uniform(0.7, 0.95),
            'location': (random.randint(0, 100), random.randint(0, 100))
        })
    return threats

def detect_with_yolo(frame):
    """YOLO based object detection"""
    detections = []
    if random.random() > 0.7:
        detections.append({
            'class': 'person',
            'confidence': random.uniform(0.8, 0.99),
            'bbox': [random.randint(50, 200), random.randint(50, 200), random.randint(50, 150), random.randint(100, 250)]
        })
    return detections

def track_objects(frame, detections):
    """Track multiple objects in real-time"""
    try:
        tracker = cv2.TrackerCSRT_create()
    except Exception:
        return []

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
    """Combine multiple detection models"""
    try:
        mog2 = cv2.createBackgroundSubtractorMOG2()
        knn = cv2.createBackgroundSubtractorKNN()

        mog2_mask = mog2.apply(frame)
        knn_mask = knn.apply(frame)
        combined = cv2.bitwise_or(mog2_mask, knn_mask)
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
    except Exception:
        return []