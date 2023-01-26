import sys
import webbrowser

import numpy as np

import Core.EZ as EZ
import UI.Components.EzButton
import UI.Components.EzText
import UI.Components.EzToggle
import UI.Components.EzTextField
from UI.Components.EzButton import check_ez_button_event
from UI.Components.EzToggle import check_ez_toggle_event
from UI.Components import *

import pygame

# parameters
json_file = "Resources\\Components\\components.json"


class HomeScreen:
    """HomeScreen class displays the home screen of the program"""

    def __init__(self, app):
        self.app = app
        self.toggleMandelbrot: bool = False
        self.toggleMouse: bool = False
        self.toggleFPS: bool = True
        self.params: list[float] = [-1, 0, 200, 1.2, 20]
        self.ez_buttons: list[UI.Components.EzButton] = UI.Components.EzButton.loader(
            json_file
        )
        self.ez_texts: list[UI.Components.EzText] = UI.Components.EzText.loader(
            json_file
        )
        self.ez_toggles: list[UI.Components.EzToggle] = UI.Components.EzToggle.loader(
            json_file
        )
        self.ez_textFields: list[
            UI.Components.EzTextField
        ] = UI.Components.EzTextField.loader(json_file)

    def draw(self):

        # draw the buttons
        for button in self.ez_buttons:
            button.create_button()

        # draw the texts
        for text in self.ez_texts:
            text.create_text()

        # draw the toggles
        for toggle in self.ez_toggles:
            toggle.create_toggle()

        # draw the text fields
        for textField in self.ez_textFields:
            textField.create_text_field()

    def run(self):
        self.draw()
        self.update()

    def update(self):
        # get the screen array of the menu and copy it to the main screen array
        menu_screen_array = EZ.get_screen_array(self.app.resolution[0] - self.app.resolution[2])
        np.copyto(self.app.screen_array[-self.app.resolution[2]:], menu_screen_array)

    def check_events(self):
        # get the event from EZ
        event = EZ.get_event()
        # get mouse coordinates
        mouse_x, mouse_y = EZ.mouse_coordinates()

        # quit the program if the user clicks the exit button
        if event == "EXIT" or event == "KEY_DOWN" and EZ.key() == "escape":
            EZ.destroy_window()
            sys.exit()

        # check if the user clicks the mouse
        if event == "MOUSE_LEFT_BUTTON_DOWN":
            # get the mouse coordinates
            mouse_x, mouse_y = EZ.mouse_coordinates()
            # check if the user clicked a button or toggle
            checked_ez_button = check_ez_button_event(self.ez_buttons, mouse_x, mouse_y)
            checked_ez_toggle = check_ez_toggle_event(self.ez_toggles, mouse_x, mouse_y)
            # toggle check
            if checked_ez_toggle is not None:
                if checked_ez_toggle.name == "toggleMandelbrot":
                    self.toggleMandelbrot = not self.toggleMandelbrot
                if checked_ez_toggle.name == "toggleMouseMode":
                    self.toggleMouse = not self.toggleMouse
                if checked_ez_toggle.name == "toggleFPS":
                    self.toggleFPS = not self.toggleFPS
                checked_ez_toggle.create_toggle()

            # button check
            if checked_ez_button is not None:
                # help button -> open help.html
                if checked_ez_button.name == "btnHelp":
                    try:
                        webbrowser.open("Resources\\Help\\help.html")
                    except FileNotFoundError:
                        print("Help file not found.")
                        print(
                            "Please make sure you have a help.html file in the help directory."
                        )
                checked_ez_button.create_button()
            self.update()

        # check if the user presses a key
        if event == "KEY_DOWN":
            # get mouse coordinates
            mouse_x, mouse_y = EZ.mouse_coordinates()

            # text field check
            for textField in self.ez_textFields:
                if textField.check_hover(mouse_x, mouse_y):
                    if EZ.key() == "m":
                        textField.on_hover('.', self)
                    else:
                        textField.on_hover(EZ.key(), self)
                    textField.create_text_field()
            self.update()

        if event == "MOUSE_MOVEMENT":
            self.app.fractal.mouse_pos = EZ.mouse_coordinates()

        # check hover and change cursor
        if any(
            button.check_hover(mouse_x, mouse_y) for button in self.ez_buttons
        ) or any(toggle.check_hover(mouse_x, mouse_y) for toggle in self.ez_toggles):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif any(
            textField.check_hover(mouse_x, mouse_y) for textField in self.ez_textFields
        ):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
