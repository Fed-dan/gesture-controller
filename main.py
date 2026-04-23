import cv2
from src.capture.camera import CameraCapture
from src.vision.detector import HandDetector
from src.capture.renderer import Renderer
from src.vision.classifier import GestureClassifier

if __name__ == "__main__":
    c1 = CameraCapture()
    detector = HandDetector()
    renderer = Renderer()
    classifier = GestureClassifier()


    try:
        while True:
            success, frame = c1.read_frame()
            if success and frame is not None:

                hands_list = detector.find_hands(frame)
                renderer.draw_landmarks(frame, hands_list)

                for hand in hands_list:
                    gesture = classifier.classify(hand)
                    renderer.draw_gesture(frame, gesture)

                cv2.imshow("win", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        c1.release()
        cv2.destroyAllWindows()
