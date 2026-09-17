"""
Lumexa Real-Time Emotion Detector -- main application entry point.

RESPONSIBLE USE REMINDER: this app classifies visible facial expression
PATTERNS in real time. It does not know anyone's true feelings, and its
confidence scores are estimates of pattern similarity to training data,
not guarantees. See README.md for the full disclaimer. Always let anyone
on camera know this analysis is running.

Run: python src/main.py
Press 'q' to quit. Press 's' to save a snapshot.
"""

import logging
import os
import time
from datetime import datetime

import cv2

from config import Config
from face_detector import FaceDetector
from emotion_model import ExpressionClassifier
from renderer import ResultRenderer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("emotion_detector.main")


class EmotionDetectorApp:
    def __init__(self, config):
        self.config = config
        self.detector = FaceDetector(config)
        self.classifier = ExpressionClassifier(config)
        self.renderer = ResultRenderer(config)

        if not self.classifier.is_available():
            logger.warning(
                "Running in DETECTION-ONLY mode: no emotion model loaded. "
                "Faces will be boxed but not classified. See models/README.md."
            )

        os.makedirs(config.SNAPSHOT_DIR, exist_ok=True)

    def process_frame(self, frame):
        faces = self.detector.detect(frame)
        detections = []
        for (x, y, w, h) in faces:
            face_crop = frame[y:y + h, x:x + w]
            label, confidence = self.classifier.classify(face_crop)
            detections.append({"box": (x, y, w, h), "label": label, "confidence": confidence})
        return detections

    def save_snapshot(self, frame):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(self.config.SNAPSHOT_DIR, f"snapshot_{timestamp}.png")
        cv2.imwrite(path, frame)
        logger.info(f"Snapshot saved to {path}")

    def run(self):
        cap = cv2.VideoCapture(self.config.CAMERA_INDEX)
        if not cap.isOpened():
            logger.error(
                f"Could not open camera index {self.config.CAMERA_INDEX}. "
                "Check that a webcam is connected and not in use by another application."
            )
            return

        logger.info("Lumexa Real-Time Emotion Detector started. Press 'q' to quit, 's' to snapshot.")
        frame_count = 0
        prev_time = time.time()
        last_detections = []

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("Frame capture failed; ending session.")
                    break

                if frame_count % self.config.PROCESS_EVERY_N_FRAMES == 0:
                    last_detections = self.process_frame(frame)

                current_time = time.time()
                elapsed = current_time - prev_time
                fps = 1.0 / elapsed if elapsed > 0 else 0.0
                prev_time = current_time

                annotated = self.renderer.draw(frame.copy(), last_detections, fps)
                cv2.imshow("Lumexa Real-Time Emotion Detector", annotated)

                frame_count += 1
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    logger.info("Quit key pressed by user.")
                    break
                elif key == ord('s'):
                    self.save_snapshot(annotated)

        except KeyboardInterrupt:
            logger.info("Shutdown requested via Ctrl+C.")
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}")
        finally:
            cap.release()
            cv2.destroyAllWindows()
            logger.info(f"Session ended. Processed {frame_count} frames total.")


if __name__ == "__main__":
    app = EmotionDetectorApp(Config())
    app.run()
