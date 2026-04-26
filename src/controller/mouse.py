import pyautogui

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

    def move(self, x: float, y: float) -> None:
        x = max(0.0, min(1.0, x))
        y = max(0.0, min(1.0, y))

        pyautogui.moveTo(x * self.screen_w,
                         y * self.screen_h,
                         duration=0.05)

    def click(self) -> None:
        pyautogui.click()
