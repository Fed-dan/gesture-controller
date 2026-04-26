import cv2
import numpy as np



class CameraCapture:
    def __init__(self, camera_index: int = 0):
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise Exception("Could not open camera")

    def read_frame(self) -> tuple[bool, np.ndarray | None]:

        success, frame = self.camera.read()
        if success and frame is not None: frame = cv2.flip(frame, 1)

        return success, frame

    def release(self) -> None:
        self.camera.release()

