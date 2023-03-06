import os
import subprocess
import sys

import pygame

from Core import EZ
import UI.Components.EzButton
import UI.Components.EzText
import UI.Components.EzToggle
import UI.Components.EzTextField
from UI.Components.EzButton import check_ez_button_event
import main as launcher

# parameters
json_file = "Resources\\Components\\export_app_components.json"


class ExportUI:
    def __init__(self, app):
        self.app = app
        self.ez_texts: list[UI.Components.EzText.EzText] = UI.Components.EzText.loader(
            json_file
        )
        self.ez_buttons: list[
            UI.Components.EzButton.EzButton
        ] = UI.Components.EzButton.loader(json_file)
        self.ez_textFields: list[
            UI.Components.EzTextField.EzTextField
        ] = UI.Components.EzTextField.loader(json_file)
        self.params: list[float] = [self.ez_textFields[0].input_value]

    def draw(self):
        # draw the texts
        for text in self.ez_texts:
            text.create_text()

        # draw the buttons
        for button in self.ez_buttons:
            button.create_button()

        # draw the text fields
        for textField in self.ez_textFields:
            textField.create_text_field()

    def update(self):
        EZ.update()

    def run(self):
        self.draw()
        self.update()

    def check_events(self):
        event = EZ.get_event()

        mouse_x, mouse_y = EZ.mouse_coordinates()

        if event == "EXIT" or event == "KEY_DOWN" and EZ.key() == "ESCAPE":
            EZ.destroy_window()
            sys.exit()

        # check if the user clicks the mouse
        if event == "MOUSE_LEFT_BUTTON_DOWN":
            # check if the user clicked a button or toggle
            checked_ez_button = check_ez_button_event(self.ez_buttons, mouse_x, mouse_y)
            # button check
            if checked_ez_button is not None:
                # help button -> open help.html
                if checked_ez_button.name == "btnOpenFolder":
                    os.startfile(
                        os.path.join(os.getcwd(), "Resources\\Images\\Saved_fractals\\")
                    )
                if checked_ez_button.name == "btnExport":
                    with open(
                        os.path.join(
                            os.getcwd(), "Resources\\Images\\Saved_fractals\\count.txt"
                        ),
                        "r",
                    ) as f:
                        index = int(f.read())
                        f.close()
                    with open(
                        os.path.join(
                            os.getcwd(), "Resources\\Images\\Saved_fractals\\count.txt"
                        ),
                        "w",
                    ) as f:
                        f.write(str(index + 1))
                        f.close()
                    self.app.application.fractal.save_image(
                        (
                            os.path.join(
                                os.getcwd(),
                                "Resources\\Images\\Saved_fractals\\"
                                + f"image{index}.png",
                            )
                        ),
                        self.params[0],
                    )
                if checked_ez_button.name == "btnReturn":
                    self.app.application.run()
                checked_ez_button.create_button()

        if event == "KEY_DOWN":
            key = EZ.key()
            # text field check
            for textField in self.ez_textFields:
                if textField.check_hover(mouse_x, mouse_y):
                    textField.on_hover(key, self)
                    textField.create_text_field()

        # check hover and change cursor
        if any(button.check_hover(mouse_x, mouse_y) for button in self.ez_buttons):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_HAND)
        elif any(
            textField.check_hover(mouse_x, mouse_y) for textField in self.ez_textFields
        ):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_IBEAM)
        else:
            EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)

        self.update()
