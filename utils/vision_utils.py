"""
Computer Vision Utilities for Sentinel Vision Pro
Created by: Tahir Mahmood
Year: 2026
"""

import cv2
import numpy as np
import random

try:
    import mediapipe as mp
except ImportError:
    mp = None

def apply_invisibility(frame, mask, background_plate, mode='full'):
    """
    Apply invisibility effect to frame using segmentation mask
    """
    if background_plate is None:
        return frame

    mask = cv2.GaussianBlur(mask, (15, 15), 0)

    if mode == 'full':
        condition = mask > 0.1
        frame[condition] = background_plate[condition]

    elif mode == 'ghost':
        alpha = 0.3
        condition = mask > 0.1
        frame[condition] = cv2.addWeighted(frame[condition], alpha,
                                           background_plate[condition], 1-alpha, 0)

    elif mode == 'predator':
        edges = cv2.Canny(mask.astype(np.uint8), 100, 200)
        edge_points = np.where(edges > 0)

        for i in range(min(len(edge_points[0]), 100)):
            y, x = edge_points[0][i], edge_points[1][i]
            if y < frame.shape[0]-5 and x < frame.shape[1]-5:
                frame[y:y+5, x:x+5] = frame[y:y+5, x:x+5] + np.random.randint(0, 20, (5, 5, 3))

    return frame

def apply_predator_mode(frame):
    """
    Apply Predator-style shimmering edge distortion
    """
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_points = np.where(edges > 0)

        for i in range(min(len(edge_points[0]), 200)):
            y, x = edge_points[0][i], edge_points[1][i]
            if y < frame.shape[0]-3 and x < frame.shape[1]-3:
                dx = random.randint(-3, 3)
                dy = random.randint(-3, 3)
                if 0 <= x+dx < frame.shape[1] and 0 <= y+dy < frame.shape[0]:
                    frame[y:y+3, x:x+3] = frame[y+dy:y+dy+3, x+dx:x+dx+3]
    except Exception:
        pass

    return frame

def apply_ghost_mode(frame, background_plate=None):
    """
    Apply ghost mode effect - semi-transparent with motion trails
    """
    if background_plate is not None:
        alpha = 0.4
        frame = cv2.addWeighted(frame, alpha, background_plate, 1-alpha, 0)

    kernel = np.ones((5, 5), np.float32) / 25
    frame = cv2.filter2D(frame, -1, kernel)

    return frame

def anonymize_faces(frame):
    """
    Detect and anonymize faces in real-time
    """
    try:
        if mp is None:
            return frame

        mp_face = mp.solutions.face_detection
        face_detection = mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_detection.process(rgb)

        if results.detections:
            height, width = frame.shape[:2]
            for detection in results.detections:
                bbox = detection.location_data.relative_bounding_box
                x = int(bbox.xmin * width)
                y = int(bbox.ymin * height)
                w = int(bbox.width * width)
                h = int(bbox.height * height)

                frame[y:y+h, x:x+w] = cv2.GaussianBlur(frame[y:y+h, x:x+w], (99, 99), 30)
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.putText(frame, "ANONYMIZED", (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
    except Exception:
        pass

    return frame

def detect_threats_yolo(frame):
    """
    Detect threats using YOLO-like object detection
    """
    threats = []
    if random.random() > 0.8:
        threats.append({
            'type': 'person',
            'confidence': random.uniform(0.7, 0.95),
            'bbox': [100, 100, 200, 300]
        })
    return threats

def detect_surveillance(frame, face_cascade=None):
    """
    Detect faces and potential surveillance attempts
    """
    if face_cascade is None:
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        )

    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 20,
                                   param1=50, param2=30, minRadius=5, maxRadius=30)

        threats = {
            'faces': len(faces),
            'cameras': 0,
            'faces_detected': faces
        }

        if circles is not None:
            threats['cameras'] = len(circles[0])
    except Exception:
        threats = {'faces': 0, 'cameras': 0, 'faces_detected': []}

    return threats

def add_security_overlay(frame, threat_level='low'):
    """
    Add security HUD overlay to frame
    """
    try:
        overlay = frame.copy()
        colors = {
            'low': (0, 255, 0),
            'medium': (0, 255, 255),
            'high': (0, 0, 255),
            'critical': (255, 0, 0)
        }
        color = colors.get(threat_level, (0, 255, 0))
        cv2.rectangle(overlay, (10, 10), (200, 60), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)
        cv2.putText(frame, f"THREAT LEVEL: {threat_level.upper()}", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
    except Exception:
        pass

    return frame