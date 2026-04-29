class GestureClassifier:
    def __init__(self, gestures: list = [], auxiliary: list = [], combined: list = []):
        self.gestures = gestures
        self.auxiliary = {a["name"]: a for a in auxiliary}  # словарь для быстрого поиска
        self.combined = combined

    def classify(self, hand: list) -> str:
        combined = self.classify_combined(hand)
        if combined:
            return combined

        for gesture in self.gestures:
            if self.compare_y(hand, gesture["compare_a"], gesture["compare_b"], gesture["expected"]):
                return gesture["name"]

        return "UNKNOWN"

    def classify_combined(self, hand) -> str | None:
        hand_label = hand[1]
        for gesture in self.combined:
            if gesture["hand"] != hand_label:
                continue

            # проверяем base жест
            base = next((g for g in self.gestures if g["name"] == gesture["base"]), None)
            if not base or not self.compare_y(hand, base["compare_a"], base["compare_b"], base["expected"]):
                continue

            # проверяем auxiliary жест
            aux = self.auxiliary.get(gesture["requires"])
            if not aux:
                continue

            if aux["axis"] == "x":
                if self.compare_x(hand, aux["compare_a"], aux["compare_b"], aux["expected"]):
                    return gesture["name"]
            else:
                if self.compare_y(hand, aux["compare_a"], aux["compare_b"], aux["expected"]):
                    return gesture["name"]

        return None

    def compare_y(self, hand, compare_a, compare_b, expected) -> bool:
        lm = hand[0]
        return all((lm[compare_a[i]].y < lm[compare_b[i]].y) == expected[i] for i in range(len(compare_a)))

    def compare_x(self, hand, compare_a, compare_b, expected) -> bool:
        lm = hand[0]
        return all((lm[compare_a[i]].x < lm[compare_b[i]].x) == expected[i] for i in range(len(compare_a)))