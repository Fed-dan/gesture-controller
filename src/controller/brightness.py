import screen_brightness_control as sbc

class BrightnessController:

    def __init__(self, inc_step: int = 10, dec_step: int = 10):
        self.inc_step = inc_step
        self.dec_step = dec_step

    def set_brightness(self, brightness: float) -> None:
        clamped = max(0.0, min(1.0, brightness))
        sbc.set_brightness(int(clamped * 100))
        print(f"setting brightness: {clamped}")

    def increase(self) -> None:
        current = sbc.get_brightness()[0]
        sbc.set_brightness(min(100, current + self.inc_step))

    def decrease(self) -> None:
        current = sbc.get_brightness()[0]
        sbc.set_brightness(max(0, current - self.dec_step))