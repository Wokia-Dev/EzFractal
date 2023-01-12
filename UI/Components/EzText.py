import json

import Core.EZ as EZ


def loader(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [
        EzText(text["name"], text["x"], text["y"],
               text["text"], text["color"], text["font_size"], text["font_family"],
               text["file_format"]) for text in data["EzTexts"]]


class EzText:
    """ EzText class """

    def __init__(self, name, x, y, text, color, font_size, font_family, file_format):
        self.name = name
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font_family = font_family
        self.file_format = file_format

    def create_text(self):
        current_font = EZ.load_font(self.font_size, f'Resources/Fonts/{self.font_family}.{self.file_format}')
        text_content = EZ.image_text(self.text, current_font, self.color)
        EZ.draw_image(text_content, self.x, self.y)
