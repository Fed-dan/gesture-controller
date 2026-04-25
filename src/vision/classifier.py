TIPS_OPEN = [8,  12, 16, 20]   # указательный, средний, безымянный, мизинец
PIPS_OPEN  = [7, 11, 15, 19]

TIPS_PEACE = [8, 12, 15, 19]
PIPS_PEACE = [7, 11, 13, 17]

TIPS_POINT = [8, 8, 11, 15, 19]
PIPS_POINT = [7, 6, 9, 13, 17]

# open 8<7 12<11 16<15 20<19
# peace 8<7 12<11 13<15 17<19
# point 8<7 9<11 13<15 17<19
class GestureClassifier:
    def classify(self, hand_landmarks: list) -> str:
        if [hand_landmarks[tip].y < hand_landmarks[pip].y for tip, pip in zip(TIPS_OPEN, PIPS_OPEN)] == [True, True, True, True]:
            return "OPEN"
        if [hand_landmarks[tip].y < hand_landmarks[pip].y for tip, pip in zip(TIPS_PEACE, PIPS_PEACE)] == [True, True, False, False]:
            return "PEACE"
        if [hand_landmarks[tip].y < hand_landmarks[pip].y for tip, pip in zip(TIPS_POINT, PIPS_POINT)] == [True, True, False, False, False] and not self.is_thumb_straight(hand_landmarks):
            return "POINT"
        if self.is_pinch_mode_entry(hand_landmarks):
            return "PINCH_IN"
        if self.is_pinch_mode_exit(hand_landmarks):
            return "PINCH_OUT"

        return "UNKNOWN"

    def is_thumb_straight(self, hand) -> bool:
        return hand[4].x < hand[3].x


    def is_pinch_mode_entry(self, hand) -> bool:
        return self.is_thumb_straight(hand) and [hand[tip].y < hand[pip].y for tip, pip in zip(TIPS_POINT, PIPS_POINT)] == [True, True, False, False, False]

    def is_pinch_mode_exit(self, hand) -> bool:
        return not self.is_pinch_mode_entry(hand)
