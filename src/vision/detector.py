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

        hands_list = []

        if hasattr(results, 'multi_hand_landmarks') and results.multi_hand_landmarks:
            for multi_hlm in results.multi_hand_landmarks:
                lm = multi_hlm.landmark
                hands_list.append(lm)
        return hands_list



