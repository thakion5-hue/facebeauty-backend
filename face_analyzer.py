"""
얼굴 분석 모듈 - MediaPipe FaceMesh 기반
얼굴형, 피부톤, 이목구비 특징 추출
"""
import cv2
import numpy as np
import mediapipe as mp
from typing import Dict, List, Tuple


class FaceAnalyzer:
    LANDMARK_FOREHEAD = 10
    LANDMARK_CHIN = 152
    LANDMARK_LEFT_CHEEK = 234
    LANDMARK_RIGHT_CHEEK = 454
    LANDMARK_LEFT_JAW = 172
    LANDMARK_RIGHT_JAW = 397
    LANDMARK_LEFT_EYE_OUTER = 33
    LANDMARK_RIGHT_EYE_OUTER = 263
    LANDMARK_NOSE_TIP = 1

    SKIN_SAMPLE_POINTS = [10, 234, 454, 50, 280, 6, 197, 117, 346]

    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
        )

    def detect_landmarks(self, img_bgr: np.ndarray) -> Dict:
        rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return {"success": False, "landmarks": []}

        h, w = img_bgr.shape[:2]
        landmarks = []
        for lm in results.multi_face_landmarks[0].landmark:
            landmarks.append({
                "x": int(lm.x * w),
                "y": int(lm.y * h),
                "z": float(lm.z),
            })

        return {"success": True, "landmarks": landmarks}

    def classify_face_shape(self, landmarks: List[Dict], img_shape: Tuple) -> str:
        forehead = landmarks[self.LANDMARK_FOREHEAD]
        chin = landmarks[self.LANDMARK_CHIN]
        left_cheek = landmarks[self.LANDMARK_LEFT_CHEEK]
        right_cheek = landmarks[self.LANDMARK_RIGHT_CHEEK]
        left_jaw = landmarks[self.LANDMARK_LEFT_JAW]
        right_jaw = landmarks[self.LANDMARK_RIGHT_JAW]

        face_length = self._distance(forehead, chin)
        cheek_width = self._distance(left_cheek, right_cheek)
        jaw_width = self._distance(left_jaw, right_jaw)
        forehead_width = self._distance(landmarks[103], landmarks[332])

        if cheek_width == 0:
            return "oval"

        length_ratio = face_length / cheek_width
        jaw_cheek_ratio = jaw_width / cheek_width
        forehead_jaw_ratio = forehead_width / jaw_width if jaw_width > 0 else 1.0

        if length_ratio > 1.55:
            return "long"
        if length_ratio > 1.25 and 0.85 < jaw_cheek_ratio < 1.0:
            return "oval"
        if length_ratio < 1.15 and jaw_cheek_ratio > 0.9:
            return "round"
        if jaw_cheek_ratio > 0.95 and length_ratio < 1.3:
            return "square"
        if forehead_jaw_ratio > 1.15 and jaw_cheek_ratio < 0.85:
            return "heart"
        if forehead_jaw_ratio < 0.9 and jaw_cheek_ratio < 0.85:
            return "diamond"
        return "oval"

    def analyze_skin_tone(self, img_bgr: np.ndarray, landmarks: List[Dict]) -> Dict:
        h, w = img_bgr.shape[:2]
        samples = []

        for idx in self.SKIN_SAMPLE_POINTS:
            if idx >= len(landmarks):
                continue
            cx, cy = landmarks[idx]["x"], landmarks[idx]["y"]
            x1, y1 = max(0, cx - 8), max(0, cy - 8)
            x2, y2 = min(w, cx + 8), min(h, cy + 8)
            patch = img_bgr[y1:y2, x1:x2]
            if patch.size > 0:
                samples.append(patch.reshape(-1, 3).mean(axis=0))

        if not samples:
            return {
                "category": "medium", "undertone": "neutral",
                "rgb": [180, 150, 130], "hsv": [20, 60, 180],
                "luminance": 155.0
            }

        avg_bgr = np.mean(samples, axis=0)
        b, g, r = float(avg_bgr[0]), float(avg_bgr[1]), float(avg_bgr[2])
        rgb = [int(r), int(g), int(b)]

        luminance = 0.299 * r + 0.587 * g + 0.114 * b
        if luminance > 210:
            category = "fair"
        elif luminance > 175:
            category = "light"
        elif luminance > 140:
            category = "medium"
        elif luminance > 100:
            category = "tan"
        else:
            category = "deep"

        rb_diff = r - b
        if rb_diff > 28:
            undertone = "warm"
        elif rb_diff < 10:
            undertone = "cool"
        else:
            undertone = "neutral"

        hsv_img = cv2.cvtColor(np.uint8([[avg_bgr]]), cv2.COLOR_BGR2HSV)[0][0]

        return {
            "category": category,
            "undertone": undertone,
            "rgb": rgb,
            "hsv": [int(hsv_img[0]), int(hsv_img[1]), int(hsv_img[2])],
            "luminance": round(float(luminance), 1),
        }

    def analyze_features(self, landmarks: List[Dict], img_shape: Tuple) -> Dict:
        eye_width = self._distance(landmarks[33], landmarks[133])
        eye_height = self._distance(landmarks[159], landmarks[145])
        eye_ratio = eye_height / eye_width if eye_width > 0 else 0.3

        lip_thickness = self._distance(landmarks[13], landmarks[14])
        face_width = self._distance(
            landmarks[self.LANDMARK_LEFT_CHEEK],
            landmarks[self.LANDMARK_RIGHT_CHEEK]
        )
        nose_length = self._distance(landmarks[6], landmarks[2])

        eye_size = "large" if eye_ratio > 0.35 else ("small" if eye_ratio < 0.25 else "medium")
        lip_ratio = lip_thickness / face_width if face_width > 0 else 0.06
        lip_type = "full" if lip_ratio > 0.08 else ("thin" if lip_ratio < 0.05 else "medium")
        nose_ratio = nose_length / face_width if face_width > 0 else 0.4
        nose_type = "long" if nose_ratio > 0.5 else ("short" if nose_ratio < 0.35 else "medium")

        return {
            "eyes": {"size": eye_size, "ratio": round(eye_ratio, 3)},
            "lips": {"type": lip_type, "thickness_ratio": round(lip_ratio, 3)},
            "nose": {"type": nose_type, "length_ratio": round(nose_ratio, 3)},
            "face_width_px": round(face_width, 1),
        }

    def draw_landmarks(self, img: np.ndarray, landmarks: List[Dict]) -> np.ndarray:
        # 얼굴 윤곽 그리기
        contour_indices = [10, 338, 297, 332, 284, 251, 389, 356, 454, 323,
                           361, 288, 397, 365, 379, 378, 400, 377, 152, 148,
                           176, 149, 150, 136, 172, 58, 132, 93, 234, 127,
                           162, 21, 54, 103, 67, 109, 10]
        pts = np.array([[landmarks[i]["x"], landmarks[i]["y"]] for i in contour_indices
                       if i < len(landmarks)], dtype=np.int32)
        if len(pts) > 1:
            cv2.polylines(img, [pts], False, (255, 105, 180), 2)

        # 주요 특징점만 표시
        key_indices = [33, 133, 159, 145, 263, 362, 386, 374, 1, 61, 291, 13, 14]
        for idx in key_indices:
            if idx < len(landmarks):
                cv2.circle(img, (landmarks[idx]["x"], landmarks[idx]["y"]), 3, (0, 255, 180), -1)
        return img

    @staticmethod
    def _distance(p1: Dict, p2: Dict) -> float:
        return float(np.sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2))
