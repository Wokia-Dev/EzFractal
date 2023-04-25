import json

import pygame

import Core.EZ as EZ
from UI.Components.EzButton import draw_border_radius
from UI.Components.EzComponent import EzComponent


def loader(file_path: str):
    # Load EzFractalButton data from json file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # return a list of EzFractalButton objects
        return [
            EzFractalButton(
                button["name"],
                button["x"],
                button["y"],
                button["width"],
                button["height"],
                button["border_radius"],
                button["background_color"],
                button["background_opacity"],
                button["font_color"],
                button["font_size"],
                button["font_family"],
                button["c_real"],
                button["c_imag"],
                button["max_iterations"],
                button["max_length"],
                button["image_path"],
                button["file_format"],
            )
            for button in data["EzFractalButtons"]
        ]
    except Exception as e:
        print(f"Error loading EzFractalButton data from {file_path}: {e}")


class EzFractalButton(EzComponent):
    """EzFractalButton class for creating fractal buttons"""

    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            width: int,
            height: int,
            border_radius: int,
            background_color: str,
            background_opacity: int,
            font_color: str,
            font_size: int,
            font_family: str,
            c_real: float,
            c_imaginary: float,
            max_iterations: int,
            max_length: int,
            image_path: str,
            file_format: str = "otf",
    ):
        super().__init__(name, x, y, width, height)
        self.border_radius = border_radius
        self.background_color = background_color
        self.background_opacity = background_opacity
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family
        self.c_real = c_real
        self.c_imaginary = c_imaginary
        self.max_iterations = max_iterations
        self.max_length = max_length
        self.image_path = image_path
        self.file_format = file_format
        self.image_loaded = EZ.transform_image(EZ.load_image(self.image_path), zoom=0.275)

    # Create button
    def create_fractal_button(self, surface: pygame.Surface):
        # Draw background
        if self.border_radius == 0:
            # draw simple rectangle if border radius is 0
            EZ.draw_rectangle_right(
                self.x,
                self.y,
                self.width,
                self.height - 1,
                self.background_color,
                transparency=self.background_opacity,
                canvas=surface,
            )
        else:
            # draw rounded rectangle if border radius is not 0
            draw_border_radius(
                self.x,
                self.y,
                self.width,
                self.height - 1,
                self.border_radius,
                self.background_color,
                self.background_opacity,
                canvas=surface,
            )

        # Draw image
        try:
            EZ.draw_image(
                self.image_loaded, self.x, self.y, self.background_opacity, canvas=surface
            )

        except FileNotFoundError:
            print(f"Error loading image from {self.image_path}")

        # Draw text
        font_loaded = EZ.load_font(self.font_size, f"Resources/Fonts/{self.font_family}.{self.file_format}")
        # refortmat c_real and c_imaginary
        c_real_formatted = (
            str(self.c_real)[: self.max_length]
            if len(str(self.c_real)) > self.max_length
            else str(self.c_real)
        )
        c_imaginary_formatted = (
            str(self.c_imaginary)[: self.max_length]
            if len(str(self.c_imaginary)) > self.max_length
            else str(self.c_imaginary)
        )

        c_real_text = EZ.image_text(
            f"c(real): {c_real_formatted}", font_loaded, self.font_color
        )
        c_imaginary_text = EZ.image_text(
            f"c(img): {c_imaginary_formatted}", font_loaded, self.font_color
        )
        max_iter_text = EZ.image_text(
            f"max iter: {self.max_iterations}", font_loaded, self.font_color
        )

        # Draw text
        texts_height = (
                c_real_text.get_height()
                + c_imaginary_text.get_height()
                + max_iter_text.get_height()
        )
        texts_height_spacing = (self.height - texts_height) / 2
        EZ.draw_image(c_real_text, self.x + 140, self.y + 20, canvas=surface)
        EZ.draw_image(
            c_imaginary_text,
            self.x + 140,
            self.y + 20 + texts_height_spacing,
            canvas=surface,
        )
        EZ.draw_image(
            max_iter_text,
            self.x + 140,
            self.y + 20 + texts_height_spacing * 2,
            canvas=surface,
        )

    def check_hover(
            self,
            x: int,
            y: int,
            scroll_view_x,
            scroll_view_y,
            scroll_offset,
            display_height,
            scroll_view_height,
    ):
        # check x position
        if self.x + scroll_view_x <= x <= self.x + self.width + scroll_view_x:
            # get the position of the scroll bar in the scroll view
            pos_view_surface = scroll_offset * (1 + display_height / scroll_view_height)
            # get the maximum position of the scroll bar in the scroll view
            max_pos_view_surface = scroll_view_height - self.height
            # get the position of the scroll bar on the screen
            scroll_pos = pos_view_surface * (
                    (display_height - self.height) / max_pos_view_surface
            )
            if scroll_pos <= y - self.y - scroll_view_y <= scroll_pos + self.height:
                return True
        return False
