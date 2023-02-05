import json

import Core.EZ as EZ
from UI.Components.EzButton import draw_border_radius
from UI.Components.EzComponent import EzComponent


def loader(file_path, content: callable):
    # Load EzComplexButton data from json file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # return a list of EzComplexButton objects
        return [
            EzComplexButton(
                button["name"],
                button["x"],
                button["y"],
                button["width"],
                button["height"],
                button["background_color"],
                button["background_opacity"],
                button["border_radius"],
                content
            )
            for button in data["EzComplexButtons"]
        ]
    except Exception as e:
        print(f"Error loading EzComplexButton data from {file_path}: {e}")


def check_ez_complex_button_event(button_list, mouse_x, mouse_y):
    # Check if mouse is hovering over any button
    for button in button_list:
        if button.check_hover(mouse_x, mouse_y):
            return button


class EzComplexButton(EzComponent):
    """ EzComplexButton class for creating complex buttons """

    def __init__(self,
                 name: str,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 background_color: str,
                 background_opacity: int,
                 border_radius: int,
                 content: callable):
        super().__init__(name, x, y, width, height)
        self.background_color = background_color
        self.background_opacity = background_opacity
        self.border_radius = border_radius
        self.content = content

    # Create button
    def create_complex_button(self):
        # Draw button
        if self.border_radius == 0:
            # draw simple rectangle if border radius is 0
            EZ.draw_rectangle_right(
                self.x,
                self.y,
                self.width,
                self.height,
                self.background_color,
                transparency=self.background_opacity,
            )
        else:
            # draw rounded rectangle if border radius is not 0
            draw_border_radius(
                self.x,
                self.y,
                self.width,
                self.height,
                self.border_radius,
                self.background_color,
                self.background_opacity,
            )

        self.content(self.name, self.x, self.y, self.width, self.height)

    def check_hover(self, mouse_x, mouse_y) -> bool:
        # Check if mouse is hovering over button
        return (
                self.x <= mouse_x <= self.x + self.width
                and self.y <= mouse_y <= self.y + self.height
        )
