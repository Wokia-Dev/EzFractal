import Core.EZ as EZ
import json


def loader(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return [
        EzToggle(toggle["name"], toggle["x"], toggle["y"], toggle["width"], toggle["height"],
                 toggle["background_off_color"], toggle["background_on_color"], toggle["circle_color"],
                 toggle["current_state"]) for toggle in data["EzToggles"]]


def check_ez_toggle_event(toggle_list, mouse_x, mouse_y):
    for toggle in toggle_list:
        if toggle.check_hover(mouse_x, mouse_y):
            toggle.on_click()
            return toggle


class EzToggle:
    """ EzToggle class """

    def __init__(self, name, x: int, y: int, width: int, height: int, background_off_color, background_on_color,
                 circle_color, current_state):
        self.name = name
        self.x = x
        self.y = -y
        self.width = width
        self.height = height
        self.background_off_color = background_off_color
        self.background_on_color = background_on_color
        self.circle_color = circle_color
        self.current_state = current_state

    def create_toggle(self):
        radius = int(self.height / 2)
        if self.current_state:
            # Draw background
            EZ.draw_disk(self.x + radius, abs(self.y - radius), radius, self.background_on_color)
            EZ.draw_disk(self.x + self.width - radius, abs(self.y - radius), radius, self.background_on_color)
            EZ.draw_rectangle_right(self.x + radius, 0 - self.y, self.width - self.height, self.height,
                                    self.background_on_color)

            # Draw circle
            EZ.draw_disk(self.x + self.width - radius, abs(self.y - radius), int(radius * 0.85), self.circle_color)

        else:
            # Draw background
            EZ.draw_disk(self.x + radius, abs(self.y - radius), radius, self.background_off_color)
            EZ.draw_disk(self.x + self.width - radius, abs(self.y - radius), radius, self.background_off_color)
            EZ.draw_rectangle_right(self.x + radius, 0 - self.y, self.width - self.height, self.height,
                                    self.background_off_color)

            # Draw circle
            EZ.draw_disk(self.x + radius, abs(self.y - radius), int(radius * 0.85), self.circle_color)

    def check_hover(self, mouse_x, mouse_y):
        if self.x <= mouse_x <= self.x + self.width and abs(self.y) <= mouse_y <= abs(self.y) + self.height:
            return True
        else:
            return False

    def on_click(self):
        self.current_state = not self.current_state
        self.create_toggle()
