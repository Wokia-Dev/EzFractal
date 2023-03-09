import pygame

import Core.EZ as EZ
from Apps import explore_app, export_app
from Apps.Saved_app import Saved_App
from Apps.popular_app import Popular_App
from UI.launcher_UI import LauncherUI

# parameters
# secondary parameters
caption = "EZ Fractal-Launcher"

# main parameters
width, height = 700, 400


class Launcher:
    def __init__(self):
        self.resolution = width, height
        self.application = explore_app.Application(self)
        self.launcher_ui = LauncherUI(self, self.application)
        self.popular_app = Popular_App(self, self.application)
        self.saved_app = Saved_App(self, self.application)
        self.export_app = export_app.Export_App(self, self.application)

    def run(self, from_return: bool = False):
        EZ.create_window(self.resolution[0], self.resolution[1], caption,
                         self.application.working_directory + "/Resources/Images/icon.png")
        EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.launcher_ui.run()
        # application.run()
        while True:
            EZ.update()
            self.launcher_ui.check_events()


if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()
