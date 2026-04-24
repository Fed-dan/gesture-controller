import math

import cv2
from src.capture.camera import CameraCapture
from src.vision.detector import HandDetector
from src.capture.renderer import Renderer
from src.vision.classifier import GestureClassifier
from src.vision.smoother import CoordinateSmoother
from src.vision.debounce import GestureDebounce
from src.controller import media, mouse, volume
from collections import deque


click_history = deque(maxlen=30)
click_cooldown = 0
CLICK_COOLDOWN = 0.5


def detect_click(history, hand) -> bool:
    history_list = list(history)

    first_chunk, second_chunk, third_chunk = [
        history_list[i:i + 10]
        for i in range(0, 30, 10)
    ]

    first_chunk_index_max = min(range(len(first_chunk)), key=lambda i: first_chunk[i][0])
    second_chunk_index_min = max(range(len(second_chunk)), key=lambda i: second_chunk[i][0])
    third_chunk_index_max = min(range(len(third_chunk)), key=lambda i: third_chunk[i][0])

    first_chunk_max_value = first_chunk[first_chunk_index_max][0]
    first_chunk_max_gesture = first_chunk[first_chunk_index_max][1]

    second_chunk_min_gesture = second_chunk[second_chunk_index_min][1]
    second_chunk_min_value = second_chunk[second_chunk_index_min][0]

    third_chunk_max_value = third_chunk[third_chunk_index_max][0]
    third_chunk_max_gesture = third_chunk[third_chunk_index_max][1]

    return (first_chunk_max_gesture == third_chunk_max_gesture == "POINT"
            and second_chunk_min_value - first_chunk_max_value  > hand[6].y - hand[8].y
            and second_chunk_min_value - third_chunk_max_value  > hand[6].y - hand[8].y)

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

    pinch_mode = False
    entry_distance = None


    click_cooldown = 0
    CLICK_COOLDOWN = 0.5

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

                    click_history.append((hand[8].y, gesture))
                    confirmed = debounce.update(gesture)

                    if gesture == "POINT": mouse_controller.move(sx, sy)

                    if confirmed:
                        if not pinch_mode:
                            if classifier.is_pinch_mode_entry(hand):
                                pinch_mode = True
                                print("pinch mode")
                                entry_distance = math.sqrt((hand[4].x - hand[8].x) ** 2 + (hand[4].y - hand[8].y) ** 2)
                                continue
                        else:
                            if classifier.is_pinch_mode_exit(hand):
                                pinch_mode = False
                                continue
                            else:
                                distance = math.sqrt((hand[4].x - hand[8].x) ** 2 + (hand[4].y - hand[8].y) ** 2)
                                volume_change = distance / entry_distance
                                volume_controller.set_volume(volume_change)
                                continue

                        renderer.draw_gesture(frame, confirmed)
                        # if confirmed == "OPEN": volume_controller.increase()
                        # if confirmed == "PEACE": volume_controller.decrease()

                    if len(click_history) == 30 and detect_click(click_history, hand):
                        mouse_controller.click()

                cv2.imshow("win", frame)



            if cv2.waitKey(1) & 0xFF == ord('q'): break

    finally:
        c1.release()
        cv2.destroyAllWindows()
