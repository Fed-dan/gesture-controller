import cv2
from src.capture.camera import CameraCapture
from src.vision.detector import HandDetector
from src.capture.renderer import Renderer
from src.vision.classifier import GestureClassifier
from src.vision.smoother import CoordinateSmoother
from src.vision.debounce import GestureDebounce
from src.controller import media, mouse, volume


if __name__ == "__main__":
    c1 = CameraCapture()
    detector = HandDetector()
    renderer = Renderer()
    classifier = GestureClassifier()
    smoother = CoordinateSmoother()
    debounce = GestureDebounce()

    mouse_controller = mouse.MouseController()
    media_controller = media.MediaController()
    volume_controller = volume.VolumeController()

    try:
        while True:
            success, frame = c1.read_frame()
            if success and frame is not None:

                hands_list = detector.find_hands(frame)

                if hands_list:
                    lm8 = hands_list[0][8]
                    sx, sy = smoother.smooth(lm8.x, lm8.y)
                    lm8.x, lm8.y = sx, sy

                renderer.draw_landmarks(frame, hands_list)

                for hand in hands_list:
                    gesture = classifier.classify(hand)
                    if gesture == "POINT": mouse_controller.move(sx, sy)

                    confirmed = debounce.update(gesture)
                    if confirmed:
                        renderer.draw_gesture(frame, confirmed)
                        if confirmed == "OPEN": volume_controller.increase()
                        if confirmed == "PEACE": volume_controller.decrease()


                cv2.imshow("win", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'): break

    finally:
        c1.release()
        cv2.destroyAllWindows()
