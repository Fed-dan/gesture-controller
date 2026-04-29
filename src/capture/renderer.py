import cv2

TIPS = [4, 8, 12, 16, 20]

class Renderer:
    def draw_landmarks(self, frame, hands_list: list) -> None:
        h, w = frame.shape[:2]

        for landmarks, hand_label in hands_list:
            if hand_label == "Left":
                color = (0, 255, 0)
            elif hand_label == "Right":
                color = (0, 0, 255)
            else:
                color = (255, 0, 0)

            for i in TIPS:
                x, y = int(landmarks[i].x * w), int(landmarks[i].y * h)
                cv2.circle(frame, (x, y), 5, color, -1)

    def draw_gesture(self, frame, gesture, hand_label: str) -> None:
        font_size, thickness = 1, 2

        if hand_label == "Left":
            cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 255, 0), thickness)
        elif hand_label == "Right":
            w = frame.shape[1]
            (text_w, text_h), baseline = cv2.getTextSize(gesture, cv2.FONT_HERSHEY_SIMPLEX, font_size, thickness)
            x = w - text_w - 10
            cv2.putText(frame, gesture, (x, 30), cv2.FONT_HERSHEY_SIMPLEX, font_size, (0, 255, 0), thickness)