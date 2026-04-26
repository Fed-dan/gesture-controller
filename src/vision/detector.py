import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self, max_hands: int = 2, detection_confidence: float = 0.7):
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

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(
                    results.multi_hand_landmarks,
                    results.multi_handedness
            ):
                lm = hand_landmarks.landmark
                hand_label = handedness.classification[0].label

                hands_list.append((lm, hand_label))

        return hands_list



