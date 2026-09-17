"""
Lumexa Object Recognition App -- real-time webcam detection entry point.

Run: python src/detect_webcam.py
Press 'q' to quit. Press 's' to save a snapshot of the current annotated frame.
"""

import logging
import os
import time
from datetime import datetime

import cv2

from config import Config
from detector import ObjectDetector
from renderer import ResultRenderer

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("object_recognition.detect_webcam")


class WebcamDetectionApp:
    def __init__(self, config):
        self.config = config
        self.detector = ObjectDetector(config)
        self.renderer = ResultRenderer(config)
        os.makedirs(config.SNAPSHOT_DIR, exist_ok=True)

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
                "Check that a webcam is connected and not in use elsewhere."
            )
            return

        logger.info("Lumexa Object Recognition (webcam) started. Press 'q' to quit, 's' to snapshot.")
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
                    last_detections = self.detector.detect(frame)

                current_time = time.time()
                elapsed = current_time - prev_time
                fps = 1.0 / elapsed if elapsed > 0 else 0.0
                prev_time = current_time

                annotated = self.renderer.draw(frame.copy(), last_detections, fps)
                cv2.imshow("Lumexa Object Recognition", annotated)

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
    app = WebcamDetectionApp(Config())
    app.run()
