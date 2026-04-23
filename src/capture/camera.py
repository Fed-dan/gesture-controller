import cv2
import numpy



class CameraCapture:
    def __init__(self, camera_index: int = 0):
        self.camera = cv2.VideoCapture(camera_index)
        if not self.camera.isOpened():
            raise Exception("Could not open camera")

    def read_frame(self) -> tuple[bool, numpy.ndarray | None]:

        success, frame = self.camera.read()
        return success, frame

    def release(self):
        self.camera.release()

