import math

import numpy as np
import pygame

import Core.EZ as EZ
import Core.EzUtils as EzUtils
import json

from UI.Components.EzComponent import EzComponent


def loader(file_path):
    # Load EzScrollView data from json file
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [
            EzScrollView(
                scroll_view["name"],
                scroll_view["x"],
                scroll_view["y"],
                scroll_view["width"],
                scroll_view["height"],
                scroll_view["display_height"],
                scroll_view["background_color"],
                scroll_view["scroll_bar_color"],
                scroll_view["scroll_bar_width"],
                scroll_view["offset"],
                scroll_view["offset_speed"]
            )
            for scroll_view in data["EzScrollViews"]
        ]
    except Exception as e:
        print(f"Error loading EzScrollView data from {file_path}: {e}")


class EzScrollView(EzComponent):
    """ EzScrollView class for creating scroll views """

    def __init__(
            self,
            name: str,
            x: int,
            y: int,
            width: int,
            height: int,
            display_height: int,
            background_color: str,
            scroll_bar_color: str,
            scroll_bar_width: int,
            offset: int = 0,
            offset_speed: int = 10,
            view_surface: pygame.Surface = None
    ):
        super().__init__(name, x, y, width, height)
        self.display_height = display_height
        self.background_color = background_color
        self.scroll_bar_color = scroll_bar_color
        self.scroll_bar_width = scroll_bar_width
        self.offset = offset
        self.offset_speed = offset_speed
        self.scroll_bar_height = int(self.display_height / self.height * self.display_height)
        self.view_surface = view_surface
        self.mouse_down = False

    def create_scroll_view(self, content_function: callable = None):
        # create the view surface
        self.view_surface = EZ.create_surface(self.width, self.height)

        # draw the background
        EZ.draw_rectangle_right(0, 0, self.width, self.height, self.background_color, canvas=self.view_surface)

        # draw the scroll bar
        self.draw_scroll_bar()

        # draw the content
        if content_function is not None:
            content_function(surface=self.view_surface)

    def draw_on_screen(self, screen_array: np.array, app):
        # draw the view surface on the screen
        surface_screen_array = np.asarray(pygame.surfarray.array3d(self.view_surface), dtype=np.uint8)
        max_x = app.resolution[0]
        max_y = app.resolution[1]
        menu_width = app.resolution[2]
        if self.x + self.width > max_x - menu_width:
            print("EzScrollView: x position is out of bounds")
            return None
        if self.y + self.height > max_y:
            np.copyto(screen_array[self.x:self.x + self.width, self.y:self.y + self.display_height],
                      surface_screen_array[0:self.width,
                      self.offset:max_y - self.y + self.offset - (max_y - self.y - self.display_height)])
        else:
            np.copyto(screen_array[self.x:self.x + self.width, self.y:self.y + self.height], surface_screen_array)

    def scroll_up(self, gap=None):
        if gap is None:
            if self.offset - self.offset_speed >= 0:
                self.offset -= self.offset_speed
                self.draw_scroll_bar()
            else:
                self.offset = 0
                self.draw_scroll_bar()
        else:
            if self.offset - gap >= 0:
                self.offset -= gap
                self.draw_scroll_bar()

    def scroll_down(self, height, gap=None):
        if gap is None:
            if self.offset + height + self.offset_speed <= self.height + self.y + (
                    height - self.y - self.display_height):
                self.offset += self.offset_speed
                self.draw_scroll_bar()
            else:
                self.offset = self.height + self.y + (height - self.y - self.display_height) - height
                self.draw_scroll_bar()
        else:
            if self.offset + height + gap <= self.height + self.y + (height - self.y - self.display_height):
                self.offset += gap
                self.draw_scroll_bar()

    def draw_scroll_bar(self, mouse_y=None):
        if mouse_y is None:
            # draw the scroll bar
            if self.height > self.display_height:
                # erase the scroll bar
                EZ.draw_rectangle_right(self.width - self.scroll_bar_width, 0, self.scroll_bar_width, self.height,
                                        self.background_color, canvas=self.view_surface)

                # draw the scroll bar
                EZ.draw_rectangle_right(self.width - self.scroll_bar_width,
                                        math.ceil(self.offset * (1 + self.display_height / self.height)),
                                        self.scroll_bar_width,
                                        self.scroll_bar_height,
                                        self.scroll_bar_color,
                                        canvas=self.view_surface)
        else:
            if self.height > self.display_height:
                relative_mouse_y = EzUtils.clamp(mouse_y - self.y, 0, self.display_height)
                self.offset = math.ceil(
                    relative_mouse_y * (self.height - self.display_height) / self.display_height)
                self.draw_scroll_bar()

    def check_scroll_hover(self, x, y):
        if self.x + self.width - self.scroll_bar_width <= x <= self.x + self.width:
            pos_view_surface = self.offset * (1 + self.display_height / self.height)
            max_pos_view_surface = self.height - self.scroll_bar_height
            scroll_pos = pos_view_surface * ((self.display_height - self.scroll_bar_height) / max_pos_view_surface)
            if scroll_pos <= y - self.y <= scroll_pos + self.scroll_bar_height:
                return True
        return False

    def check_hover(self, x, y):
        if self.x <= x <= self.x + self.width:
            if self.y <= y <= self.y + self.display_height:
                return True
        return False
