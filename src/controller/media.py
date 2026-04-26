import pyautogui


class MediaController:
    PLAY_PAUSE_KEY = "playpause"
    NEXT_TRACK_KEY = "nexttrack"
    PREV_TRACK_KEY = "prevtrack"

    def play_pause(self) -> None:
        pyautogui.press(self.PLAY_PAUSE_KEY)

    def next_track(self) -> None:
        pyautogui.press(self.NEXT_TRACK_KEY)

    def prev_track(self) -> None:
        pyautogui.press(self.PREV_TRACK_KEY)