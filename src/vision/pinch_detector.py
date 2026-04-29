import math


class PinchDetector:
    def __init__(self):
        self.pinch_mode = {"Left": False, "Right": False}
        self.entry_distance = {"Left": None, "Right": None}

    def update(self, hand, classifier) -> float | None:
        is_entry = classifier.classify_combined(hand) == "PINCH_IN"

        if not self.pinch_mode[hand[1]]:
            if is_entry:
                self.pinch_mode[hand[1]] = True
                self.entry_distance[hand[1]] = math.dist(
                    (hand[0][4].x, hand[0][4].y),
                    (hand[0][8].x, hand[0][8].y)
                )
            return None

        elif not is_entry:
            self.pinch_mode[hand[1]] = False
            return None

        return math.dist((hand[0][4].x, hand[0][4].y), (hand[0][8].x, hand[0][8].y)) / self.entry_distance[hand[1]]


    def is_active(self, hand_label: str) -> bool:
        return self.pinch_mode[hand_label]