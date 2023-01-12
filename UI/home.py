import Core.EZ as EZ
import UI.Components.EzButton
import UI.Components.EzText
import UI.Components.EzToggle
from UI.Components.EzButton import check_ez_button_event
from UI.Components.EzToggle import check_ez_toggle_event
from UI.Components import *

# parameters
json_file = "Resources\\Components\\components.json"


class HomeScreen:
    def __init__(self, app):
        self.app = app
        self.toggleMandelbrot = False
        self.toggleMouse = False
        self.toggleFPS = True
        self.ez_buttons = UI.Components.EzButton.loader(json_file)
        self.ez_texts = UI.Components.EzText.loader(json_file)
        self.ez_toggles = UI.Components.EzToggle.loader(json_file)

    def draw(self):
        EZ.draw_rectangle_right(0, 0, 500, 400, "0000FF")

        for button in self.ez_buttons:
            button.create_button()

        for text in self.ez_texts:
            text.create_text()

        for toggle in self.ez_toggles:
            toggle.create_toggle()

    def run(self):
        self.draw()

    def check_events(self):
        event = EZ.get_event()
        if event == "EXIT" or event == "KEY_DOWN" and EZ.key() == "escape":
            EZ.destroy_window()
        if event == "MOUSE_LEFT_BUTTON_DOWN":
            mouse_x, mouse_y = EZ.mouse_coordinates()
            checked_ez_button = check_ez_button_event(self.ez_buttons, mouse_x, mouse_y)
            checked_ez_toggle = check_ez_toggle_event(self.ez_toggles, mouse_x, mouse_y)
            if checked_ez_toggle is not None:
                if checked_ez_toggle.name == "toggleMandelbrot":
                    self.toggleMandelbrot = not self.toggleMandelbrot
                if checked_ez_toggle.name == "toggleMouseMode":
                    self.toggleMouse = not self.toggleMouse
                if checked_ez_toggle.name == "toggleFPS":
                    self.toggleFPS = not self.toggleFPS
