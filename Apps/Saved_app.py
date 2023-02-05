import pygame

from Core import EZ
from UI.saved_UI import SavedUI

# parameters
# secondary parameters
caption = "EZ Fractal-Saved"

# main parameters
width, height = 700, 400


class Saved_App:
    def __init__(self, launcher, app):
        self.resolution = width, height
        self.launcher = launcher
        self.application = app
        self.saved_app_ui = SavedUI(self)

    def run(self, from_return: bool = False):
        EZ.create_window(self.resolution[0], self.resolution[1], caption)
        EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.saved_app_ui.run()
        while True:
            EZ.update()
            self.saved_app_ui.check_events()
