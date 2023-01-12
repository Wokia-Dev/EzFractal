import Core.EZ as EZ
import json


def loader(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [
        EzButton(button["name"], button["x"], button["y"], button["width"], button["height"], button["text"],
                 button["background_color"], button["background_opacity"], button["font_size"],
                 button["font_color"], button["font_family"], button["border_radius"], button["text_margin"],
                 button["click_timer"]) for button in data["EzButtons"]]


def check_ez_button_event(button_list, mouse_x, mouse_y):
    for button in button_list:
        if button.check_hover(mouse_x, mouse_y):
            button.on_click()
            return button


class EzButton:
    """ EzButton class """

    def __init__(self, name, x, y, width, height, text, background_color, background_opacity, font_size, font_color,
                 font_family, border_radius, text_margin, click_timer):
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
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
        if self.border_radius == 0:
            EZ.draw_rectangle_right(self.x, self.y, self.width, self.height, self.background_color,
                                    transparency=self.background_opacity)
        else:
            EZ.draw_disk(self.x + self.border_radius, self.y + self.border_radius, self.border_radius,
                         self.background_color, transparency=self.background_opacity)
            EZ.draw_disk(self.x + self.border_radius, self.y + self.height - self.border_radius, self.border_radius,
                         self.background_color, transparency=self.background_opacity)
            EZ.draw_disk(self.x + self.width - self.border_radius, self.y + self.border_radius, self.border_radius,
                         self.background_color, transparency=self.background_opacity)
            EZ.draw_disk(self.x + self.width - self.border_radius, self.y + self.height - self.border_radius,
                         self.border_radius, self.background_color, transparency=self.background_opacity)

            EZ.draw_rectangle_right(self.x, self.y + self.border_radius, self.width + 1,
                                    self.height - self.border_radius - self.border_radius, self.background_color,
                                    transparency=self.background_opacity)

            EZ.draw_rectangle_right(self.x + self.border_radius, self.y,
                                    self.width - self.border_radius - self.border_radius,
                                    self.height + 1, self.background_color, transparency=self.background_opacity)
        if self.text != "":
            current_font = EZ.load_font(self.font_size, f'Resources/Fonts/{self.font_family}.otf')
            text_content = EZ.image_text(self.text, current_font, self.font_color)
            EZ.draw_image(text_content, (self.width // 2 + self.x) + self.text_margin[0],
                          (self.height // 2 + self.y) + self.text_margin[1])

    def check_hover(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.x + self.width and self.y <= mouse_y <= self.y + self.height:
            return True
        else:
            return False

    def on_click(self):
        self.background_color, self.font_color = self.font_color, self.background_color
        self.create_button()
        EZ.update()
        EZ.wait(self.click_timer)
        self.background_color, self.font_color = self.font_color, self.background_color
        self.create_button()
        EZ.update()
