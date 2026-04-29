from collections import deque

class ComplexGestureDetector:
    def __init__(self,gestures: list = [], max_len: int = 5):
        self.COMPLEX_GESTURES = gestures
        self.max_len = max_len
        self.confirmed_gestures = deque(maxlen=max_len)

    def update(self, gesture: str, hand_label: str):
        self.confirmed_gestures.append((gesture, hand_label))

    def classify_complex_gesture(self) -> str | None:
        history = list(self.confirmed_gestures)

        for gesture in self.COMPLEX_GESTURES:
            name = gesture["name"]
            sequence = [tuple(s) for s in gesture["sequence"]]

            if len(sequence) > self.max_len or len(history) < len(sequence):
                continue

            recent_sequence = history[-len(sequence):]

            if recent_sequence == sequence:
                return name

        return None