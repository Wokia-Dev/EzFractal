import sys

import pygame

from Core import EZ
import UI.Components.EzButton
import main as launcher
from UI.Components.EzButton import check_ez_button_event

json_file = "Resources\\Components\\popular_app_components.json"


class PopularUI:
    def __init__(self, app):
        self.app = app
        self.ez_buttons: list[UI.Components.EzButton] = UI.Components.EzButton.loader(
            json_file
        )

    def draw(self):
        for button in self.ez_buttons:
            button.create_button()

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

        # check if the user clicks the mouse
        if event == "MOUSE_LEFT_BUTTON_DOWN":
            # check if the user clicked a button or toggle
            checked_ez_button = check_ez_button_event(self.ez_buttons, mouse_x, mouse_y)

            # button check
            if checked_ez_button is not None:
                # help button -> open help.html
                if checked_ez_button.name == "btnReturn":
                    launcher.Launcher.run(self.app.launcher, from_return=True)
                checked_ez_button.create_button()

        # check hover and change cursor
        if any(button.check_hover(mouse_x, mouse_y) for button in self.ez_buttons):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
