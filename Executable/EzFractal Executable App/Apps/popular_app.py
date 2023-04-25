import numpy as np
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
        self.screen_array = np.full((width, height, 3), [255, 255, 255], dtype=np.uint8)
        self.popular_app_ui = PopularUI(self, self.application)

    def run(self, from_return: bool = False):
        EZ.create_window(self.resolution[0], self.resolution[1], caption,
                         self.application.working_directory + "/Resources/Images/icon.png")
        EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.popular_app_ui.run()
        while True:
            EZ.draw_array(self.screen_array)
            self.popular_app_ui.run()
            self.popular_app_ui.check_events()
            EZ.update()
