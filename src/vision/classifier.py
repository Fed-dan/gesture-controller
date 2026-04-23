TIPS = [8,  12, 16, 20]   # указательный, средний, безымянный, мизинец
PIPS = [6,  10, 14, 18]   # их вторые суставы

class GestureClassifier:
    def classify(self, hand_landmarks: list) -> str:
        fingers = [hand_landmarks[tip].y < hand_landmarks[pip].y
                   for tip, pip in zip(TIPS, PIPS)]

        if fingers == [True, True, True, True]:   return "OPEN"
        if fingers == [True, True, False, False]: return "PEACE"
        if fingers == [True, False, False, False]: return "POINT"

        return "UNKNOWN"
