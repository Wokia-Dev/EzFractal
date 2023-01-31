import sys

from Apps import main
import Core.EZ as EZ
from UI.launcher_UI import LauncherUI

# parameters
# secondary parameters
caption = "EZ Fractal Launcher"

# main parameters
width, height = 700, 400


class Launcher:
    def __init__(self):
        self.resolution = width, height
        self.launcher_ui = LauncherUI(self)

    def run(self, from_return: bool = False):
        if from_return:
            EZ.destroy_window()

        EZ.create_window(self.resolution[0], self.resolution[1], caption)
        application = main.Application(self)
        self.launcher_ui.run()
        while True:
            EZ.update()
            self.launcher_ui.check_events()

            EZ.update()


if __name__ == "__main__":
    launcher = Launcher()
    launcher.run()
