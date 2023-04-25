import Core.EZ as EZ
import json

from UI.Components.EzComponent import EzComponent


def loader(file_path):
    # Load EzToggle data from json file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            EzToggle(
                toggle["name"],
                toggle["x"],
                toggle["y"],
                toggle["width"],
                toggle["height"],
                toggle["background_off_color"],
                toggle["background_on_color"],
                toggle["circle_color"],
                toggle["current_state"],
            )
            for toggle in data["EzToggles"]
        ]
    except Exception as e:
        print(f"Error loading EzToggle data from {file_path}: {e}")


def check_ez_toggle_event(toggle_list, mouse_x, mouse_y):
    # Check if mouse is hovering over any toggle
    for toggle in toggle_list:
        if toggle.check_hover(mouse_x, mouse_y):
            toggle.on_click()
            return toggle


class EzToggle(EzComponent):
    """EzToggle class"""

    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        width: int,
        height: int,
        background_off_color: str,
        background_on_color: str,
        circle_color: str,
        current_state: bool,
    ):
        super().__init__(name, x, -y, width, height)
        self.background_off_color = background_off_color
        self.background_on_color = background_on_color
        self.circle_color = circle_color
        self.current_state = current_state

    def create_toggle(self):
        # Draw toggle

        # Calculate radius
        radius = int(self.height / 2)
        # draw with active state
        if self.current_state:
            # Draw first disk
            EZ.draw_disk(
                self.x + radius, abs(self.y - radius), radius, self.background_on_color
            )
            # Draw second disk
            EZ.draw_disk(
                self.x + self.width - radius,
                abs(self.y - radius),
                radius,
                self.background_on_color,
            )
            # Draw rectangle
            EZ.draw_rectangle_right(
                self.x + radius,
                0 - self.y,
                self.width - self.height,
                self.height,
                self.background_on_color,
            )

            # Draw circle at the end
            EZ.draw_disk(
                self.x + self.width - radius,
                abs(self.y - radius),
                int(radius * 0.85),
                self.circle_color,
            )

        # draw with inactive state
        else:
            # Draw first disk
            EZ.draw_disk(
                self.x + radius, abs(self.y - radius), radius, self.background_off_color
            )
            # Draw second disk
            EZ.draw_disk(
                self.x + self.width - radius,
                abs(self.y - radius),
                radius,
                self.background_off_color,
            )
            # Draw rectangle
            EZ.draw_rectangle_right(
                self.x + radius,
                0 - self.y,
                self.width - self.height,
                self.height,
                self.background_off_color,
            )

            # Draw circle at the start
            EZ.draw_disk(
                self.x + radius,
                abs(self.y - radius),
                int(radius * 0.85),
                self.circle_color,
            )

    def check_hover(self, mouse_x, mouse_y) -> bool:
        # Check if mouse is hovering over toggle
        return (
            self.x <= mouse_x <= self.x + self.width
            and abs(self.y) <= mouse_y <= abs(self.y) + self.height
        )

    def on_click(self):
        # change state and redraw toggle on click
        self.current_state = not self.current_state
        self.create_toggle()
