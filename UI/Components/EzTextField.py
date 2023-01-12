import Core.EZ as EZ
import json
import pygame
import Core.EzUtils as EzUtils
import UI.home


def loader(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [
        EzTextField(
            text_field["name"],
            text_field["x"],
            text_field["y"],
            text_field["width"],
            text_field["height"],
            text_field["text"],
            text_field["text_margin"],
            text_field["background_color"],
            text_field["border_color"],
            text_field["font_color"],
            text_field["font_size"],
            text_field["font_family"],
            text_field["font_file_format"],
            text_field["border_width"],
            text_field["value"],
            text_field["input_value"],
            text_field["params"],
            text_field["character_list"],
        )
        for text_field in data["EzTextFields"]
    ]


class EzTextField:
    """EzTextField class"""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        text_margin,
        background_color: str,
        border_color: str,
        font_color: str,
        font_size: int,
        font_family: str,
        font_file_format: str,
        border_width: int,
        value: str,
        input_value: float,
        params: int,
        character_list=None,
    ):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = str(input_value)
        self.text_margin = text_margin
        self.background_color = background_color
        self.border_color = border_color
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family
        self.font_file_format = font_file_format
        self.border_width = border_width
        self.value = value
        self.input_value = input_value
        self.params = params
        self.character_list = character_list

    def create_text_field(self):
        EZ.draw_rectangle_right(
            self.x, self.y, self.width, self.height, self.border_color
        )
        EZ.draw_rectangle_right(
            self.x + self.border_width,
            self.y + self.border_width,
            self.width - self.border_width * 2,
            self.height - self.border_width * 2,
            self.background_color,
        )
        if self.text != "":
            current_font = EZ.load_font(
                self.font_size,
                f"Resources/Fonts/{self.font_family}.{self.font_file_format}",
            )
            text_content = EZ.image_text(self.text, current_font, self.font_color)
            EZ.draw_image(
                text_content,
                (self.width // 2 + self.x) + self.text_margin[0],
                (self.height // 2 + self.y) + self.text_margin[1],
            )

    def update_text(self, text, text_margin):
        self.text = text
        current_font = EZ.load_font(
            self.font_size,
            f"Resources/Fonts/{self.font_family}.{self.font_file_format}",
        )
        text_content = EZ.image_text(self.text, current_font, self.font_color)
        EZ.draw_image(
            text_content,
            (self.width // 2 + self.x) + text_margin[0],
            (self.height // 2 + self.y) + text_margin[1],
        )

    def check_hover(self, mouse_x, mouse_y):
        if (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        ):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_IBEAM)
            return True
        EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return False

    def on_hover(self, key, home_screen):
        key = key.replace("[", "").replace("]", "")
        if key not in self.character_list:
            return
        if key == "backspace":
            if len(self.value) > 0:
                self.text_margin[0] += 5
                self.value = self.value[:-1]
        elif key == "return" or key == "enter":
            if self.value != "" and EzUtils.is_float(self.value):
                self.input_value = float(self.value)
                home_screen.params[self.params] = self.input_value
        else:
            self.value += key
            self.text_margin[0] -= 5

        self.update_text(self.value, self.text_margin)
