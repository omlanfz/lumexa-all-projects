"""
Snapshot and video clip recording utilities for the Lumexa
Motion-Activated Security Cam.

PRIVACY REMINDER: this module writes real image/video files to local
disk with no automatic deletion or encryption. See the project
README's "Privacy Considerations" section before deploying this in
any real space -- get consent from anyone who might be recorded, and
have a plan for how long footage is retained and who can access it.

This module intentionally implements NO external notification service
(no email, no SMS, no push API) -- only local console logging and local
file saving, so the project has zero external dependencies or accounts
required. See README.md "Extensions" for how one COULD be added.
"""

import logging
import os
from datetime import datetime

import cv2

logger = logging.getLogger("security_cam.recorder")


class EventRecorder:
    def __init__(self, config):
        self.config = config
        os.makedirs(config.CAPTURES_DIR, exist_ok=True)

        self._video_writer = None
        self._clip_frames_remaining = 0
        self._clip_path = None

    def _timestamp(self):
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def notify(self, motion_box_count):
        """Logs a console notification for a motion event. See README for how
        to extend this with a real email/push notification service, optionally."""
        timestamp = datetime.now().isoformat(timespec="seconds")
        logger.warning(
            f"MOTION DETECTED at {timestamp} -- {motion_box_count} region(s) flagged."
        )

    def save_snapshot(self, frame):
        timestamp = self._timestamp()
        path = os.path.join(self.config.CAPTURES_DIR, f"motion_{timestamp}.png")
        cv2.imwrite(path, frame)
        logger.info(f"Snapshot saved to {path}")
        return path

    def start_clip(self, frame_shape):
        """Begins recording a short video clip for the current motion event."""
        if not self.config.RECORD_VIDEO_CLIPS:
            return

        timestamp = self._timestamp()
        self._clip_path = os.path.join(self.config.CAPTURES_DIR, f"motion_clip_{timestamp}.avi")
        height, width = frame_shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self._video_writer = cv2.VideoWriter(
            self._clip_path, fourcc, self.config.CLIP_FPS, (width, height)
        )
        self._clip_frames_remaining = int(self.config.CLIP_DURATION_SECONDS * self.config.CLIP_FPS)
        logger.info(f"Started recording motion clip: {self._clip_path}")

    def write_clip_frame(self, frame):
        """Writes one frame to the in-progress clip, if a clip is active.
        Returns True while the clip is still recording, False once finished."""
        if self._video_writer is None or self._clip_frames_remaining <= 0:
            return False

        self._video_writer.write(frame)
        self._clip_frames_remaining -= 1

        if self._clip_frames_remaining <= 0:
            self.stop_clip()
            return False
        return True

    def is_recording_clip(self):
        return self._video_writer is not None and self._clip_frames_remaining > 0

    def stop_clip(self):
        if self._video_writer is not None:
            self._video_writer.release()
            logger.info(f"Finished recording motion clip: {self._clip_path}")
            self._video_writer = None
            self._clip_frames_remaining = 0
