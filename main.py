import cv2, yaml, os

from src.capture.camera import CameraCapture
from src.capture.renderer import Renderer
from src.controller.action_controller import ActionController
from src.vision.detector import HandDetector
from src.vision.classifier import GestureClassifier
from src.vision.smoother import CoordinateSmoother
from src.vision.debounce import GestureDebounce
from src.vision.pinch_detector import PinchDetector
from src.vision.complex_gesture_detector import ComplexGestureDetector
from src.controller.mouse import MouseController
from src.controller.media import MediaController
from src.controller.volume import VolumeController
from src.controller.brightness import BrightnessController
from src.controller.app_controller import AppController


if __name__ == "__main__":

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    try:
        with open(os.path.join(BASE_DIR, "config", "config.yaml"), encoding="utf-8") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/config.yaml not found.")
        exit(1)

    try:
        with open(os.path.join(BASE_DIR, "config", "gestures.yaml"), encoding="utf-8") as f:
            gestures = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/gestures.yaml not found.")
        exit(1)

    try:
        with open(os.path.join(BASE_DIR, "config", "complex_gestures.yaml"), encoding="utf-8") as f:
            complex_config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/complex_gestures.yaml not found.")
        exit(1)

    try:
        with open(os.path.join(BASE_DIR, "config", "auxiliary.yaml"), encoding="utf-8") as f:
            auxiliary_config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/auxiliary.yaml not found.")
        exit(1)


    try:
        with open(os.path.join(BASE_DIR, "config", "combined_gestures.yaml"), encoding="utf-8") as f:
            combined_config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/combined_gestures.yaml not found.")
        exit(1)

    try:
        with open(os.path.join(BASE_DIR, "config", "actions.yaml"), encoding="utf-8") as f:
            actions = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/actions.yaml not found.")
        exit(1)

    try:
        with open(os.path.join(BASE_DIR, "config", "apps.yaml"), encoding="utf-8") as f:
            apps_config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Error: config/apps.yaml not found.")
        exit(1)


    try:
        c1 = CameraCapture(camera_index=config["camera"]["camera_index"])
        renderer = Renderer()

        detector = HandDetector(
            max_hands=config["detector"]["max_hands"],
            detection_confidence=config["detector"]["detection_confidence"]
        )
        app_controller = AppController()

        classifier = GestureClassifier(
            gestures=gestures["GESTURES"],
            auxiliary=auxiliary_config["AUXILIARY"],
            combined=combined_config["COMBINED_GESTURES"]
        )

        pinch_detector = PinchDetector()

        complex_gestures = ComplexGestureDetector(
            gestures=complex_config["COMPLEX_GESTURES"],
            max_len=config["complex_gestures"]["max_len"])

        smoother = CoordinateSmoother(alpha=config["smoother"]["alpha"])

        debounce = GestureDebounce(threshold=config["debounce"]["threshold"])

        mouse_controller = MouseController(duration=config["mouse"]["duration"])

        media_controller = MediaController()

        volume_controller = VolumeController(
            inc_step=config["volume"]["inc_step"],
            dec_step=config["volume"]["dec_step"]
        )

        brightness_controller = BrightnessController(
            inc_step=config["brightness"]["inc_step"],
            dec_step=config["brightness"]["dec_step"]
        )

        action_controller = ActionController(
            actions=actions["ACTIONS"],
            action_map={
                "volume_increase": lambda: volume_controller.increase(),
                "volume_decrease": lambda: volume_controller.decrease(),
                "brightness_increase": lambda: brightness_controller.increase(),
                "brightness_decrease": lambda: brightness_controller.decrease(),
                "mouse_click": lambda: mouse_controller.click(),
            },
            app_map = {
            name: (lambda path: lambda: app_controller.launch(path))(path)
            for name, path in apps_config["APPS"].items()
            }
        )

    except KeyError as e:
        print(f"Error: missing key {e} in config/config.yaml. Please complete the config.")
        exit(1)
    except TypeError as e:
        print(f"Error: {e} Please check the types of values in config/config.yaml.")
        exit(1)

    try:
        while True:
            success, frame = c1.read_frame()
            if success and frame is not None:

                hands_list = detector.find_hands(frame)
                renderer.draw_landmarks(frame, hands_list)

                for hand in hands_list:

                    if not hand: continue

                    lm8 = hand[0][8]
                    sx, sy = smoother.smooth(lm8.x, lm8.y)
                    lm8.x, lm8.y = sx, sy

                    gesture = classifier.classify(hand)
                    confirmed = debounce.update(gesture, hand[1])

                    hand_landmarks = hand[0]
                    hand_label = hand[1]


                    distance = pinch_detector.update(hand, classifier)

                    if pinch_detector.is_active(hand_label):
                        if hand_label == "Left" and distance is not None :
                            volume_controller.set_volume(distance)
                        elif hand_label == "Right" and distance is not None:
                            brightness_controller.set_brightness(distance)
                        continue



                    if confirmed:

                        complex_gestures.update(confirmed, hand_label)
                        complex_gesture = complex_gestures.classify_complex_gesture()

                        if complex_gesture:
                            action_controller.execute(complex_gesture, hand_label, "complex")
                            renderer.draw_gesture(frame, complex_gesture, hand_label)
                        else:
                            action_controller.execute(confirmed, hand_label, "simple")
                            renderer.draw_gesture(frame, confirmed, hand_label)

                cv2.imshow("win", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'): break

    finally:
        c1.release()
        cv2.destroyAllWindows()
