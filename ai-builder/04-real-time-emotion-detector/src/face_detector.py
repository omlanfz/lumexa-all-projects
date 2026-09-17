"""
Face detection module for the Lumexa Real-Time Emotion Detector.

Wraps OpenCV's built-in Haar Cascade classifier. Responsible ONLY for
finding face-shaped regions in a frame -- it knows nothing about
expression classification, confidence, or rendering.
"""

import logging

import cv2

logger = logging.getLogger("emotion_detector.face_detector")


class FaceDetector:
    def __init__(self, config):
        self.config = config
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.cascade = cv2.CascadeClassifier(cascade_path)
        if self.cascade.empty():
            raise RuntimeError(
                f"Failed to load Haar Cascade from '{cascade_path}'. "
                "Check your OpenCV installation."
            )
        logger.info("Face detector initialized (Haar Cascade frontal face default).")

    def detect(self, frame_bgr):
        """
        Detects faces in a BGR frame.

        Returns:
            A list of (x, y, w, h) tuples, one per detected face, giving
            the top-left corner and size of each face's bounding box.
        """
        gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        faces = self.cascade.detectMultiScale(
            gray,
            scaleFactor=self.config.FACE_SCALE_FACTOR,
            minNeighbors=self.config.FACE_MIN_NEIGHBORS,
            minSize=self.config.FACE_MIN_SIZE,
        )
        return list(faces)
