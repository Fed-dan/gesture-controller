import pyautogui

class MouseController:
    def __init__(self):
        self.screen_w, self.screen_h = pyautogui.size()

    def move(self, x: float, y: float):
        pyautogui.moveTo(x * self.screen_w, y * self.screen_h, duration=0.1)  # плавное движение
