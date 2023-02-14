import sys
import webbrowser

import numpy as np

import Core.EZ as EZ
import UI.Components.EzButton
import UI.Components.EzText
import UI.Components.EzToggle
import UI.Components.EzTextField
import main as launcher
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
        self.keyPressed: list[bool] = [
            False,
            False,
            False,
            False,
            False,
            False,
        ]  # up, down, left, right and shift
        self.keyList: list[str] = ["up", "down", "left", "right", "left shift", "left ctrl"]
        self.toggleMandelbrot: bool = False
        self.toggleMouse: bool = False
        self.toggleFPS: bool = True
        self.ez_buttons: list[UI.Components.EzButton.EzButton] = UI.Components.EzButton.loader(
            json_file
        )
        self.ez_texts: list[UI.Components.EzText.EzText] = UI.Components.EzText.loader(
            json_file
        )
        self.ez_toggles: list[UI.Components.EzToggle.EzToggle] = UI.Components.EzToggle.loader(
            json_file
        )
        self.ez_textFields: list[
            UI.Components.EzTextField.EzTextField
        ] = UI.Components.EzTextField.loader(json_file)
        self.params: list[float] = [
            self.ez_textFields[0].input_value,
            self.ez_textFields[1].input_value,
            self.ez_textFields[2].input_value,
            self.ez_textFields[3].input_value,
            self.ez_textFields[4].input_value,
        ]

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
        menu_screen_array = EZ.get_screen_array(
            self.app.resolution[0] - self.app.resolution[2]
        )
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
            # check if the user clicked a button or toggle
            checked_ez_button = check_ez_button_event(self.ez_buttons, mouse_x, mouse_y)
            checked_ez_toggle = check_ez_toggle_event(self.ez_toggles, mouse_x, mouse_y)
            # toggle check
            if checked_ez_toggle is not None:
                if checked_ez_toggle.name == "toggleMandelbrot":
                    self.toggleMandelbrot = not self.toggleMandelbrot
                    self.app.fractal.reset()
                    self.app.fractal.offset[0] += 75
                if checked_ez_toggle.name == "toggleMouseMode":
                    self.toggleMouse = not self.toggleMouse
                    self.app.fractal.reset()
                    if not self.toggleMouse:
                        for i in range(len(self.ez_textFields)):
                            self.update_text_fields(i, self.ez_textFields[i].value)
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
                if checked_ez_button.name == "btnReturn":
                    launcher.Launcher.run(self.app.launcher, from_return=True)
                checked_ez_button.create_button()

        # check if the user presses a key
        if event == "KEY_DOWN":
            key = EZ.key()
            # text field check
            for textField in self.ez_textFields:
                if textField.check_hover(mouse_x, mouse_y):
                    if key == "m":
                        textField.on_hover(".", self)
                    if key == "6" and self.keyPressed[4]:
                        textField.on_hover("-", self)
                    else:
                        textField.on_hover(key, self)
                    textField.create_text_field()

            # check reset key
            if key == "r":
                self.app.fractal.reset()
                for i in range(len(self.ez_textFields)):
                    self.update_text_fields(i, self.ez_textFields[i].value)
                if self.toggleMandelbrot:
                    self.app.fractal.offset[0] += 75

            # check arrow keys
            for i in range(len(self.keyList)):
                if key == self.keyList[i]:
                    self.keyPressed[i] = True

            # check crtl + s
            if key == "s" and self.keyPressed[5]:
                self.app.launcher.export_app.run()

        if event == "KEY_UP":
            key = EZ.key()
            # check arrow keys
            for i in range(len(self.keyList)):
                if key == self.keyList[i]:
                    self.keyPressed[i] = False

        if event == "MOUSE_MOVEMENT":
            self.app.fractal.mouse_pos = np.array([mouse_x, mouse_y])

        # check if the user scrolls
        if event == "MOUSE_SCROLL_UP":
            self.app.fractal.scroll_up(mouse_x, mouse_y)

        if event == "MOUSE_SCROLL_DOWN":
            self.app.fractal.scroll_down(mouse_x, mouse_y)

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

        # move the fractal with the arrow keys
        for i in range(len(self.keyList)):
            if self.keyPressed[i]:
                self.app.fractal.move(self.keyList[i])

        self.update()

    def draw_return_button(self):
        for button in self.ez_buttons:
            if button.name == "btnReturn":
                button.create_button()

    def update_text_fields(self, index: int, value: str):
        self.ez_textFields[index].erase()
        self.ez_textFields[index].draw_text(str(value))
        self.update()
