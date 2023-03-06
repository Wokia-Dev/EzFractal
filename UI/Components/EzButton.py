import pygame

import Core.EZ as EZ
import json

from UI.Components.EzComponent import EzComponent


def loader(file_path: str):
    # Load EzButton data from json file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # return a list of EzButton objects
        return [
            EzButton(
                button["name"],
                button["x"],
                button["y"],
                button["width"],
                button["height"],
                button["text"],
                button["background_color"],
                button["background_opacity"],
                button["font_size"],
                button["font_color"],
                button["font_family"],
                button["border_radius"],
                button["text_margin"],
                button["click_timer"],
            )
            for button in data["EzButtons"]
        ]
    except Exception as e:
        print(f"Error loading EzButton data from {file_path}: {e}")


def check_ez_button_event(button_list: list, mouse_x: int, mouse_y: int):
    # Check if mouse is hovering over any button
    for button in button_list:
        if button.check_hover(mouse_x, mouse_y):
            button.on_click()
            return button


def draw_border_radius(
        x: int, y: int, width: int, height: int, border_radius: int, background_color: str, background_opacity: int,
        canvas: pygame.Surface = None
):
    # draw rounded rectangle
    # draw top left corner
    EZ.draw_disk(
        x + border_radius,
        y + border_radius,
        border_radius,
        background_color,
        transparency=background_opacity,
        canvas=canvas if canvas else None,
    )
    # draw top right corner
    EZ.draw_disk(
        x + border_radius,
        y + height - border_radius,
        border_radius,
        background_color,
        transparency=background_opacity,
        canvas=canvas if canvas else None,
    )
    # draw bottom left corner
    EZ.draw_disk(
        x + width - border_radius,
        y + border_radius,
        border_radius,
        background_color,
        transparency=background_opacity,
        canvas=canvas if canvas else None,
    )
    # draw bottom right corner
    EZ.draw_disk(
        x + width - border_radius,
        y + height - border_radius,
        border_radius,
        background_color,
        transparency=background_opacity,
        canvas=canvas if canvas else None,
    )

    # draw top and bottom borders
    EZ.draw_rectangle_right(
        x,
        y + border_radius,
        width + 1,
        height - border_radius - border_radius,
        background_color,
        transparency=background_opacity,
        canvas=canvas if canvas else None,
    )

    # draw left and right borders
    EZ.draw_rectangle_right(
        x + border_radius,
        y,
        width - border_radius - border_radius,
        height + 1,
        background_color,
        transparency=background_opacity,
        canvas=canvas if canvas else None,
    )


class EzButton(EzComponent):
    """EzButton class for creating buttons"""

    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            width: int,
            height: int,
            text: str,
            background_color: str,
            background_opacity: int,
            font_size: int,
            font_color: str,
            font_family: str,
            border_radius: int,
            text_margin: list[int],
            click_timer: int,
    ):
        super().__init__(name, x, y, width, height)
        self.text = text
        self.background_color = background_color
        self.background_opacity = background_opacity
        self.font_size = font_size
        self.font_color = font_color
        self.font_family = font_family
        self.border_radius = border_radius
        self.text_margin = text_margin
        self.click_timer = click_timer

    # Create button
    def create_button(self):
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
        # Draw text
        if self.text != "":
            # load font
            current_font = EZ.load_font(
                self.font_size, f"Resources/Fonts/{self.font_family}.otf"
            )
            # convert text to image
            text_content = EZ.image_text(self.text, current_font, self.font_color)
            # draw text
            EZ.draw_image(
                text_content,
                self.x + (self.width - text_content.get_width()) // 2,
                self.y + (self.height - text_content.get_height()) // 2,
            )

    def check_hover(self, mouse_x: int, mouse_y: int) -> bool:
        # Check if mouse is hovering over button
        return (
                self.x <= mouse_x <= self.x + self.width
                and self.y <= mouse_y <= self.y + self.height
        )

    def on_click(self):
        # Change button color when clicked
        self.background_color, self.font_color = self.font_color, self.background_color
        self.create_button()
        EZ.update()
        EZ.wait(self.click_timer)
        self.background_color, self.font_color = self.font_color, self.background_color
        self.create_button()
        EZ.update()
