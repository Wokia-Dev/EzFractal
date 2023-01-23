import Core.EZ as EZ
import Core.EzUtils as EzUtils
import json
import pygame
import UI.home


def loader(file_path):
    # Load EzTextField data from json file
    try:
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
    except Exception as e:
        print(f"Error loading EzTextField data from {file_path}: {e}")


class EzTextField:
    """EzTextField class for creating text fields"""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        width: int,
        height: int,
        text: str,
        text_margin: list[int],
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
        # draw text field

        # draw border
        EZ.draw_rectangle_right(
            self.x, self.y, self.width, self.height, self.border_color
        )
        # draw background
        EZ.draw_rectangle_right(
            self.x + self.border_width,
            self.y + self.border_width,
            self.width - self.border_width * 2,
            self.height - self.border_width * 2,
            self.background_color,
        )
        # draw text
        if self.text != "":
            # load font
            current_font = EZ.load_font(
                self.font_size,
                f"Resources/Fonts/{self.font_family}.{self.font_file_format}",
            )
            # convert text to image and draw it
            text_content = EZ.image_text(self.text, current_font, self.font_color)
            EZ.draw_image(
                text_content,
                (self.width // 2 + self.x) + self.text_margin[0],
                (self.height // 2 + self.y) + self.text_margin[1],
            )

    def update_text(self, text, text_margin, invalid_input=False):
        # update text
        self.text = text
        # load font
        current_font = EZ.load_font(
            self.font_size,
            f"Resources/Fonts/{self.font_family}.{self.font_file_format}",
        )
        # convert text to image and draw it
        text_content = EZ.image_text(self.text, current_font, "FF00FF")
        EZ.draw_image(
            text_content,
            (self.width // 2 + self.x) + text_margin[0],
            (self.height // 2 + self.y) + text_margin[1],
        )

    def check_hover(self, mouse_x, mouse_y) -> bool:
        # check if mouse is hovering over text field
        return (
            self.x <= mouse_x <= self.x + self.width
            and self.y <= mouse_y <= self.y + self.height
        )

    def on_hover(self, key, home_screen):
        # handle key input when mouse is hovering over text field

        # remove brackets from key
        key = key.replace("[", "").replace("]", "")
        # check if key is valid
        if key not in self.character_list:
            return
        # remove last character if backspace is pressed
        if key == "backspace":
            if len(self.value) > 0:
                self.text_margin[0] += 5
                self.value = self.value[:-1]
                self.update_text(self.value, self.text_margin)
        # replace value with input value if enter or return is pressed and value is a float
        elif key in ("return", "enter"):
            if self.value != "" and EzUtils.is_float(self.value):
                self.input_value = float(self.value)
                home_screen.params[self.params] = self.input_value
                # change color and update text
                self.update_text(self.value, self.text_margin)
                self.font_color = "000000"
            else:
                # change color in red and update text
                self.font_color = "FF0000"
                self.update_text(self.value, self.text_margin, True)
        # add character to value
        else:
            self.value += key
            self.text_margin[0] -= 5
            # change color and update text
            self.font_color = "000000"
            self.update_text(self.value, self.text_margin)
