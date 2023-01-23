import json
import Core.EZ as EZ


def loader(file_path):
    # Load EzText data from json file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            EzText(
                text["name"],
                text["x"],
                text["y"],
                text["text"],
                text["color"],
                text["font_size"],
                text["font_family"],
                text["file_format"],
            )
            for text in data["EzTexts"]
        ]
    except Exception as e:
        print(f"Error loading EzText data from {file_path}: {e}")


class EzText:
    """ EzText class for creating text """

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        text: str,
        color: str,
        font_size: int,
        font_family: str,
        file_format: str,
    ):
        self.name = name
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.font_size = font_size
        self.font_family = font_family
        self.file_format = file_format

    def create_text(self):
        # load font
        current_font = EZ.load_font(
            self.font_size, f"Resources/Fonts/{self.font_family}.{self.file_format}"
        )
        # convert text to image and draw it
        text_content = EZ.image_text(self.text, current_font, self.color)
        EZ.draw_image(text_content, self.x, self.y)
