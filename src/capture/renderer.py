import cv2

FINGERTIPS = [4, 8, 12, 16, 20]

class Renderer:
    def draw_landmarks(self, frame, hands_list: list):
        h, w = frame.shape[:2]

        for hand in hands_list:

            for i in FINGERTIPS:
                x, y = int(hand[i].x * w), int(hand[i].y * h)
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

    def draw_gesture(self, frame, gesture: str):
        cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)