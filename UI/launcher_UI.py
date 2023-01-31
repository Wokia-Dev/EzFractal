import sys

from Core import EZ

json_file = "Resources\\Components\\launcher_components.json"


class LauncherUI:
    def __init__(self, app):
        self.app = app

    def draw(self):
        pass

    def update(self):
        pass

    def run(self):
        self.draw()
        self.update()

    def check_events(self):
        # get the event from EZ
        event = EZ.get_event()
        # get mouse position
        mouse_x, mouse_y = EZ.mouse_coordinates()

        # quit the program if the user clicks the exit button
        if event == "EXIT" or event == "KEY_DOWN" and EZ.key() == "escape":
            EZ.destroy_window()
            sys.exit()

