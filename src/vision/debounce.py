class GestureDebounce:
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        self.last_gesture: dict[str, tuple[str, int] | None] = {
            "Left": None,
            "Right": None
        }

    def update(self, gesture, hand: str) -> str | None:
        if hand not in self.last_gesture:
            return None

        if self.last_gesture[hand] and gesture == self.last_gesture[hand][0]:
            count = self.last_gesture[hand][1] + 1
        else:
            count = 1

        self.last_gesture[hand] = (gesture, count)
        return gesture if count == self.threshold else None
