import os

class AppController:
    def launch(self, app_path: str):
        os.startfile(app_path)