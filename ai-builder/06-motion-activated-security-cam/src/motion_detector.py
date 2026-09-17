"""
Motion detection module for the Lumexa Motion-Activated Security Cam.

Uses OpenCV's MOG2 (Mixture of Gaussians v2) background subtractor to
build a statistical model of the "normal" unmoving scene, then flags
regions that differ significantly from it as motion -- after cleanup
and area-based filtering to reject sensor noise and shadows.
"""

import logging

import cv2

logger = logging.getLogger("security_cam.motion_detector")


class MotionDetector:
    def __init__(self, config):
        self.config = config
        self.subtractor = cv2.createBackgroundSubtractorMOG2(
            history=config.BACKGROUND_HISTORY,
            varThreshold=config.VAR_THRESHOLD,
            detectShadows=config.DETECT_SHADOWS,
        )
        self._kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        logger.info("Motion detector initialized (MOG2 background subtractor).")

    def detect(self, frame_bgr):
        """
        Runs motion detection on a single BGR frame.

        Returns a list of (x, y, w, h) bounding boxes, one per detected
        motion region with contour area >= config.MIN_MOTION_AREA.
        """
        # Slight blur reduces sensor-noise-driven false positives (see Lesson 2).
        blurred = cv2.GaussianBlur(frame_bgr, (5, 5), 0)

        fg_mask = self.subtractor.apply(blurred)

        # MOG2 marks shadow pixels as gray (127) when detectShadows=True.
        # Threshold at 200 keeps only strong foreground (255), excluding shadows.
        _, thresholded = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)

        # Morphological cleanup: remove small noise, fill small gaps in real regions.
        cleaned = cv2.dilate(thresholded, self._kernel, iterations=self.config.DILATE_ITERATIONS)
        cleaned = cv2.erode(cleaned, self._kernel, iterations=1)

        contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        motion_boxes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.config.MIN_MOTION_AREA:
                x, y, w, h = cv2.boundingRect(contour)
                motion_boxes.append((x, y, w, h))

        return motion_boxes
