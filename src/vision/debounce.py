class GestureDebounce:
    def __init__(self, threshold: int = 10):
        self.threshold = threshold
        self.last_gesture: tuple[str, int] | None = None

    def update(self, gesture: str) -> str | None:
        if self.last_gesture and gesture == self.last_gesture[0]:
            count = self.last_gesture[1] + 1
        else:
            count = 1

        self.last_gesture = (gesture, count)
        return gesture if count == self.threshold else None
