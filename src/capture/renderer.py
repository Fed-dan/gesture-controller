import cv2

TIPS = [4, 8, 12, 16, 20]

class Renderer:
    def draw_landmarks(self, frame, hands_list: list) -> None:
        h, w = frame.shape[:2]

        for landmarks, hand_label in hands_list:

            for i in TIPS:
                x, y = int(landmarks[i].x * w), int(landmarks[0].y * h)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def draw_gesture(self, frame, gesture: str) -> None:
        cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)