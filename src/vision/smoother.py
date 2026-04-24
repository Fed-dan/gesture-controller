class CoordinateSmoother:
    def __init__(self, alpha: float = 0.5):
        self.alpha = alpha
        self.prev = (-1, -1)
    def smooth(self, x: float, y: float) -> tuple[float, float]:
        if self.prev == (-1, -1):
            self.prev = (x, y)
            return (x, y)

        self.prev = smooth = (self.alpha * x + (1-self.alpha) * self.prev[0], self.alpha * y + (1-self.alpha) * self.prev[1])
        return smooth
