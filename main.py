import cv2
from src.capture.camera import CameraCapture
from src.vision.detector import HandDetector

if __name__ == "__main__":
    c1 = CameraCapture()
    detector = HandDetector()

    try:
        while True:
            success, frame = c1.read_frame()
            if success and frame is not None:
                cv2.imshow("win", frame)

                print(detector.find_hands(frame))

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        c1.release()
        cv2.destroyAllWindows()
