import pyautogui

class MouseController:
    def __init__(self, duration: float = 0.05):
        self.screen_w, self.screen_h = pyautogui.size()
        self.duration = duration

    def move(self, x: float, y: float) -> None:
        x = max(0.0, min(1.0, x))
        y = max(0.0, min(1.0, y))

        pyautogui.moveTo(x * self.screen_w,
                         y * self.screen_h,
                         duration=self.duration)

    def click(self) -> None:
        pyautogui.click()
