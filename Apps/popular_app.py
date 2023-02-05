import pygame

from Core import EZ
from UI.popular_UI import PopularUI

# parameters
# secondary parameters
caption = "EZ Fractal-Popular"

# main parameters
width, height = 700, 400


class Popular_App:
    def __init__(self, launcher, app):
        self.resolution = width, height
        self.launcher = launcher
        self.application = app
        self.popular_app_ui = PopularUI(self)

    def run(self, from_return: bool = False):
        EZ.create_window(self.resolution[0], self.resolution[1], caption)
        EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.popular_app_ui.run()
        while True:
            EZ.update()
            self.popular_app_ui.check_events()

