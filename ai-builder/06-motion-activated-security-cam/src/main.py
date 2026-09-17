"""
Lumexa Motion-Activated Security Cam -- main application entry point.

PRIVACY REMINDER: only run this in spaces you have the right to monitor,
and let anyone who might be recorded know it's active. See README.md
"Privacy Considerations" before deploying this anywhere real.

Run: python src/main.py
Press 'q' to quit.
"""

import logging
import time

import cv2

from config import Config
from motion_detector import MotionDetector
from recorder import EventRecorder

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("security_cam.main")


class SecurityCamApp:
    def __init__(self, config):
        self.config = config
        self.detector = MotionDetector(config)
        self.recorder = EventRecorder(config)
        self._last_event_time = 0.0

    def _cooldown_elapsed(self):
        return (time.time() - self._last_event_time) >= self.config.COOLDOWN_SECONDS

    def _draw_overlay(self, frame, motion_boxes, fps):
        for (x, y, w, h) in motion_boxes:
            cv2.rectangle(frame, (x, y), (x + w, y + h), self.config.BOX_COLOR, 2)

        cv2.putText(frame, "MONITORING ACTIVE", (10, 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2, cv2.LINE_AA)

        if motion_boxes:
            cv2.putText(frame, "MOTION DETECTED", (10, 55),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2, cv2.LINE_AA)

        if self.recorder.is_recording_clip():
            cv2.circle(frame, (frame.shape[1] - 30, 25), 8, (0, 0, 255), -1)
            cv2.putText(frame, "REC", (frame.shape[1] - 70, 32),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2, cv2.LINE_AA)

        if fps is not None and self.config.SHOW_FPS:
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, frame.shape[0] - 15),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)

        return frame

    def run(self):
        cap = cv2.VideoCapture(self.config.CAMERA_INDEX)
        if not cap.isOpened():
            logger.error(
                f"Could not open camera index {self.config.CAMERA_INDEX}. "
                "Check that a webcam is connected and not in use elsewhere."
            )
            return

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.FRAME_HEIGHT)

        logger.info("Lumexa Motion-Activated Security Cam started. Press 'q' to quit.")
        logger.warning(
            "Reminder: only monitor spaces you have the right to monitor, and let "
            "anyone who might be recorded know this system is active."
        )

        prev_time = time.time()

        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    logger.warning("Frame capture failed; ending session.")
                    break

                motion_boxes = self.detector.detect(frame)

                current_time = time.time()
                elapsed = current_time - prev_time
                fps = 1.0 / elapsed if elapsed > 0 else 0.0
                prev_time = current_time

                if motion_boxes and self._cooldown_elapsed():
                    self._last_event_time = current_time
                    self.recorder.notify(len(motion_boxes))
                    snapshot_frame = self._draw_overlay(frame.copy(), motion_boxes, fps)
                    self.recorder.save_snapshot(snapshot_frame)
                    self.recorder.start_clip(frame.shape)

                annotated = self._draw_overlay(frame.copy(), motion_boxes, fps)

                if self.recorder.is_recording_clip():
                    self.recorder.write_clip_frame(frame)

                cv2.imshow("Lumexa Motion-Activated Security Cam", annotated)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    logger.info("Quit key pressed by user.")
                    break

        except KeyboardInterrupt:
            logger.info("Shutdown requested via Ctrl+C.")
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}")
        finally:
            self.recorder.stop_clip()
            cap.release()
            cv2.destroyAllWindows()
            logger.info("Session ended. Resources released.")


if __name__ == "__main__":
    app = SecurityCamApp(Config())
    app.run()
