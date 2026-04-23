import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands: int = 1, detection_confidence: float = 0.7):
        mp_hands = mp.solutions.hands

        self.hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence
        )

    def find_hands(self, frame) -> list:

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if hasattr(results, 'multi_hand_landmarks') and results.multi_hand_landmarks:
            lm = results.multi_hand_landmarks[0].hand_landmarks[8]
            x, y = int(lm.x * frame.shape[1]), int(lm.y * frame.shape[0])
            print(f"x: {x}, y: {y}")




