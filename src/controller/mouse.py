import pyautogui

class MouseController:
    def __init__(self, duration: float = 0.1, sensitivity: float = 0.5):
        self.screen_w, self.screen_h = pyautogui.size()
        self.duration = duration
        self.sensitivity = sensitivity  # < 1.0 = меньше движения

    def move(self, x: float, y: float):
        screen_x = x * self.screen_w * self.sensitivity
        screen_y = y * self.screen_h * self.sensitivity
        pyautogui.moveTo(screen_x, screen_y, duration=self.duration)
        
    def click(self) -> None:
        pyautogui.click()
