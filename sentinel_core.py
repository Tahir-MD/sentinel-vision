"""
Sentinel Vision Pro - Core Logic with Gesture Control
Created by: Tahir Mahmood
Year: 2026
"""

import cv2
import numpy as np
import mediapipe as mp
import hashlib
import json
from datetime import datetime
import time
import threading
from collections import deque

class SentinelVisionPro:
    """
    Advanced Privacy & Security Shield with Gesture Control
    """

    def __init__(self):
        self.shield_active = False
        self.mode = "stealth"
        self.threats_detected = 0
        self.secure_sessions = 0
        self.encryption_key = None
        self.gesture_active = False
        self.gesture_history = deque(maxlen=10)
        self.last_gesture_time = 0

        # Initialize MediaPipe
        self.mp_selfie = mp.solutions.selfie_segmentation
        self.mp_face = mp.solutions.face_detection
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        self.segmentation = self.mp_selfie.SelfieSegmentation(model_selection=1)
        self.face_detection = self.mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5)
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        # Background plate for invisibility
        self.background_plate = None

        # Security logs
        self.logs = []

        # Gesture mapping
        self.gesture_map = {
            'fist': 'activate_shield',
            'open_palm': 'deactivate_shield',
            'peace': 'toggle_ghost_mode',
            'point': 'toggle_predator_mode',
            'thumbs_up': 'calibrate_background'
        }

        print("🛡️ Sentinel Vision Pro initialized with Gesture Control")

    # ============================================================
    # GESTURE DETECTION
    # ============================================================

    def detect_gesture(self, frame):
        """
        Detect hand gestures from frame
        Returns: gesture_name, hand_landmarks
        """
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        if not results.multi_hand_landmarks:
            return None, None

        hand_landmarks = results.multi_hand_landmarks[0]
        gesture = self._classify_gesture(hand_landmarks)

        # Draw hand landmarks
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )

        return gesture, hand_landmarks

    def _classify_gesture(self, hand_landmarks):
        """
        Classify hand gesture from landmarks
        """
        # Get landmark positions
        landmarks = hand_landmarks.landmark

        # Tip positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        # MCP (base) positions
        index_mcp = landmarks[5]
        middle_mcp = landmarks[9]
        ring_mcp = landmarks[13]
        pinky_mcp = landmarks[17]

        # Check if fingers are extended
        fingers_extended = []

        # Thumb
        thumb_extended = thumb_tip.x > landmarks[3].x
        fingers_extended.append(thumb_extended)

        # Index finger
        index_extended = index_tip.y < index_mcp.y
        fingers_extended.append(index_extended)

        # Middle finger
        middle_extended = middle_tip.y < middle_mcp.y
        fingers_extended.append(middle_extended)

        # Ring finger
        ring_extended = ring_tip.y < ring_mcp.y
        fingers_extended.append(ring_extended)

        # Pinky finger
        pinky_extended = pinky_tip.y < pinky_mcp.y
        fingers_extended.append(pinky_extended)

        # Classify gesture
        extended_count = sum(fingers_extended)

        # Fist: 0 fingers extended
        if extended_count == 0:
            return 'fist'

        # Open Palm: 5 fingers extended
        if extended_count == 5:
            return 'open_palm'

        # Peace: Index and Middle extended
        if fingers_extended[1] and fingers_extended[2] and not fingers_extended[3] and not fingers_extended[4]:
            return 'peace'

        # Point: Index extended only
        if fingers_extended[1] and not fingers_extended[2] and not fingers_extended[3] and not fingers_extended[4]:
            return 'point'

        # Thumbs Up: Thumb extended, others closed
        if fingers_extended[0] and extended_count == 1:
            return 'thumbs_up'

        return 'unknown'

    def handle_gesture(self, gesture, frame):
        """
        Execute action based on detected gesture
        """
        current_time = time.time()

        # Prevent rapid switching
        if current_time - self.last_gesture_time < 0.5:
            return

        self.last_gesture_time = current_time
        self.gesture_history.append(gesture)

        action = self.gesture_map.get(gesture)

        if action == 'activate_shield':
            self.activate_shield()
            self._log_event("Shield activated by gesture", "Info")
            return "🛡️ Shield Activated!"

        elif action == 'deactivate_shield':
            self.deactivate_shield()
            self._log_event("Shield deactivated by gesture", "Info")
            return "🔓 Shield Deactivated!"

        elif action == 'toggle_ghost_mode':
            if self.mode == 'ghost':
                self.mode = 'stealth'
                self._log_event("Switched to Stealth mode", "Info")
                return "🕵️ Stealth Mode"
            else:
                self.mode = 'ghost'
                self._log_event("Switched to Ghost mode", "Info")
                return "👻 Ghost Mode"

        elif action == 'toggle_predator_mode':
            if self.mode == 'predator':
                self.mode = 'stealth'
                self._log_event("Switched to Stealth mode", "Info")
                return "🕵️ Stealth Mode"
            else:
                self.mode = 'predator'
                self._log_event("Switched to Predator mode", "Info")
                return "🌊 Predator Mode"

        elif action == 'calibrate_background':
            if self.background_plate is None:
                self.background_plate = frame.copy()
                self._log_event("Background calibrated", "Info")
                return "📸 Background Calibrated!"

        return None

    # ============================================================
    # SHIELD FUNCTIONS
    # ============================================================

    def activate_shield(self):
        """Activate the privacy shield"""
        self.shield_active = True
        self.secure_sessions += 1
        self._log_event("Shield activated", "Info")
        return True

    def deactivate_shield(self):
        """Deactivate the privacy shield"""
        self.shield_active = False
        self._log_event("Shield deactivated", "Info")
        return True

    def set_mode(self, mode):
        """Set shield mode"""
        valid_modes = ['stealth', 'defense', 'detection', 'ghost', 'predator']
        if mode in valid_modes:
            self.mode = mode
            self._log_event(f"Mode changed to {mode}", "Info")
            return True
        return False

    def calibrate_background(self, frame):
        """Calibrate background from a single frame"""
        if frame is not None:
            self.background_plate = frame.copy()
            self._log_event("Background calibrated", "Info")
            return True
        return False

    def capture_background_from_camera(self, cap, frames=30):
        """Capture clean background from camera"""
        print("🎯 Capturing background...")
        backgrounds = []
        for _ in range(frames):
            ret, frame = cap.read()
            if ret:
                backgrounds.append(frame)

        if backgrounds:
            self.background_plate = np.mean(backgrounds, axis=0).astype(np.uint8)
            self._log_event("Background calibrated", "Info")
            return True
        return False

    # ============================================================
    # FRAME PROCESSING
    # ============================================================

    def process_frame(self, frame):
        """
        Process frame with gesture detection and effects
        """
        # Create working copy
        processed = frame.copy()
        height, width = processed.shape[:2]

        # Detect gesture
        gesture, hand_landmarks = self.detect_gesture(processed)

        # Handle gesture if detected
        gesture_message = None
        if gesture and gesture != 'unknown':
            gesture_message = self.handle_gesture(gesture, processed)

        # Apply effects based on shield status
        if self.shield_active:
            # Apply invisibility/effects
            if self.mode == "ghost":
                processed = self._apply_ghost_mode(processed)
                mode_text = "👻 GHOST"
            elif self.mode == "predator":
                processed = self._apply_predator_mode(processed)
                mode_text = "🌊 PREDATOR"
            else:
                processed = self._apply_invisibility(processed)
                mode_text = "🛡️ STEALTH"
        else:
            mode_text = "📸 NORMAL"

        # Draw HUD
        processed = self._draw_hud(processed, gesture, gesture_message, mode_text)

        return processed, {
            'gesture': gesture,
            'message': gesture_message,
            'shield_active': self.shield_active,
            'mode': self.mode
        }

    # ============================================================
    # EFFECT FUNCTIONS
    # ============================================================

    def _apply_invisibility(self, frame):
        """Apply invisibility effect"""
        if self.background_plate is None:
            return frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.segmentation.process(rgb)

        if results.segmentation_mask is not None:
            mask = results.segmentation_mask
            mask = cv2.GaussianBlur(mask, (15, 15), 0)
            condition = mask > 0.1
            frame[condition] = self.background_plate[condition]

        return frame

    def _apply_ghost_mode(self, frame):
        """Apply ghost mode - semi-transparent"""
        if self.background_plate is None:
            return frame

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.segmentation.process(rgb)

        if results.segmentation_mask is not None:
            mask = results.segmentation_mask
            mask = cv2.GaussianBlur(mask, (15, 15), 0)
            condition = mask > 0.1
            alpha = 0.4
            frame[condition] = cv2.addWeighted(
                frame[condition], alpha,
                self.background_plate[condition], 1-alpha, 0
            )

        return frame

    def _apply_predator_mode(self, frame):
        """Apply predator mode - edge distortion"""
        if self.background_plate is not None:
            # Apply ghost first
            frame = self._apply_ghost_mode(frame)

        # Add shimmer effect
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_points = np.where(edges > 0)

        for i in range(min(len(edge_points[0]), 100)):
            y, x = edge_points[0][i], edge_points[1][i]
            if 3 < y < frame.shape[0]-3 and 3 < x < frame.shape[1]-3:
                dx = np.random.randint(-3, 3)
                dy = np.random.randint(-3, 3)
                frame[y:y+3, x:x+3] = frame[y+dy:y+dy+3, x+dx:x+dx+3]

        return frame

    # ============================================================
    # HUD FUNCTIONS
    # ============================================================

    def _draw_hud(self, frame, gesture, message, mode_text):
        """Draw advanced HUD overlay"""
        overlay = frame.copy()
        cv2.rectangle(overlay, (10, 10), (450, 210), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

        # Shield status
        status = "🛡️ ACTIVE" if self.shield_active else "📸 NORMAL"
        status_color = (0, 255, 0) if self.shield_active else (0, 255, 255)

        cv2.putText(frame, "SENTINEL VISION PRO", (20, 40),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, f"SHIELD: {status}", (20, 65),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 1)
        cv2.putText(frame, f"MODE: {mode_text}", (20, 85),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)

        # Gesture info
        if gesture:
            gesture_emoji = {
                'fist': '✊', 'open_palm': '🖐️', 'peace': '✌️',
                'point': '👉', 'thumbs_up': '👍'
            }.get(gesture, '👋')
            cv2.putText(frame, f"GESTURE: {gesture_emoji} {gesture.upper()}", (20, 110),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

        # Message
        if message:
            cv2.putText(frame, f"MSG: {message}", (20, 135),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

        # Instructions
        cv2.putText(frame, "✊ FIST = Activate", (20, 165),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)
        cv2.putText(frame, "🖐️ PALM = Deactivate", (20, 185),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)
        cv2.putText(frame, "✌️ PEACE = Ghost Mode", (20, 205),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.35, (200, 200, 200), 1)

        # Corner brackets
        for x, y in [(5, 5), (frame.shape[1]-5, 5), (5, frame.shape[0]-5), (frame.shape[1]-5, frame.shape[0]-5)]:
            cv2.line(frame, (x, y), (x+45, y), (0, 255, 0), 1)
            cv2.line(frame, (x, y), (x, y+45), (0, 255, 0), 1)

        return frame

    # ============================================================
    # UTILITY FUNCTIONS
    # ============================================================

    def _log_event(self, event, severity="Info"):
        """Log security events"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'event': event,
            'severity': severity
        }
        self.logs.append(log_entry)

    def get_stats(self):
        """Get current statistics"""
        return {
            'threats': self.threats_detected,
            'sessions': self.secure_sessions,
            'shield_active': self.shield_active,
            'mode': self.mode,
            'logs_count': len(self.logs)
        }

    def get_logs(self):
        """Get security logs"""
        return self.logs