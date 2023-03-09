import configparser
import json
import os

import numpy as np
import pygame

import Core.EZ as EZ
import UI.explore_UI
import main
from Core import EzUtils
from Core.EzUtils import render_julia

# parameters
# secondary parameters
caption = "EZ Fractal-Explore"

# main parameters
width, height, menu_width = 700, 400, 200
config = configparser.ConfigParser(inline_comment_prefixes=("#", ";"))
config.read("CONFIG.ini")


class EzFractal:
    def __init__(self, app):
        self.app = app
        self.mouse_pos = np.array([0, 0])
        self.zoom = 2.8 / height
        self.offset = np.array([0.7 * width, height]) // 2
        self.max_iter = config.getint("PARAMETERS", "max_iteration")
        self.c = -1.0 + 0.0j
        self.zoom_gap = config.getfloat("PARAMETERS", "zoom_factor")
        self.offset_gap = config.getint("PARAMETERS", "move_gap")
        self.saturation = config.getfloat("STYLE", "saturation")
        self.lightness = config.getfloat("STYLE", "lightness")

        # load parameters from config file
        load()

    def scroll_up(self, mouse_x: int, mouse_y: int):
        # The point at the center of the zoom is the current mouse position
        center_x = (mouse_x - self.offset[0]) * self.zoom
        center_y = (mouse_y - self.offset[1]) * self.zoom

        # zoom in
        self.zoom *= self.zoom_gap

        # Recalculate the offset to keep the mouse position at the center of the zoom
        self.offset[0] = mouse_x - (center_x / self.zoom)
        self.offset[1] = mouse_y - (center_y / self.zoom)

    def scroll_down(self, mouse_x: int, mouse_y: int):
        # The point at the center of the zoom is the current mouse position
        center_x = (mouse_x - self.offset[0]) * self.zoom
        center_y = (mouse_y - self.offset[1]) * self.zoom

        # zoom out
        self.zoom *= 1 / self.zoom_gap

        # Recalculate the offset to keep the mouse position at the center of the zoom
        self.offset[0] = mouse_x - (center_x / self.zoom)
        self.offset[1] = mouse_y - (center_y / self.zoom)

    def move(self, direction: str):
        if direction == config.get("CONTROLS", "move_up"):
            self.offset[1] += self.offset_gap
        elif direction == config.get("CONTROLS", "move_down"):
            self.offset[1] -= self.offset_gap
        elif direction == config.get("CONTROLS", "move_left"):
            self.offset[0] += self.offset_gap
        elif direction == config.get("CONTROLS", "move_right"):
            self.offset[0] -= self.offset_gap

    def reset(self):
        self.zoom = 2.8 / height
        self.offset = np.array([0.7 * width, height]) // 2

    def calculate(self):
        # update c value and max iterations
        self.c = (
            self.app.explore_app_ui.params[0] + self.app.explore_app_ui.params[1] * 1j
        )
        self.max_iter = self.app.explore_app_ui.params[2]

        # update zoom and offset
        self.zoom_gap = self.app.explore_app_ui.params[3]
        self.offset_gap = self.app.explore_app_ui.params[4]

    def update(self):
        # update the screen array with the new parameters
        self.calculate()
        # render the fractal and update the screen array
        if self.app.explore_app_ui.toggleMandelbrot:
            self.app.screen_array = EzUtils.render_mandelbrot(
                self.app.screen_array,
                self.max_iter,
                self.zoom,
                self.offset,
                width,
                height,
                menu_width,
                self.saturation,
                self.lightness,
            )
        else:
            if self.app.explore_app_ui.toggleMouse:
                # define the complex number based on the mouse position, zoom and offset
                self.c = (self.mouse_pos[0] - self.offset[0]) * self.zoom + (
                    self.mouse_pos[1] - self.offset[1]
                ) * self.zoom * 1j
                self.app.explore_app_ui.update_text_fields(0, self.c.real)
                self.app.explore_app_ui.update_text_fields(1, self.c.imag)

                # render the fractal and update the screen array
                self.app.screen_array = render_julia(
                    self.app.screen_array,
                    self.c,
                    self.max_iter,
                    self.zoom,
                    self.offset,
                    width,
                    height,
                    menu_width,
                    self.saturation,
                    self.lightness,
                )
            else:
                self.app.screen_array = render_julia(
                    self.app.screen_array,
                    self.c,
                    self.max_iter,
                    self.zoom,
                    self.offset,
                    width,
                    height,
                    menu_width,
                    self.saturation,
                    self.lightness,
                )

    def save_image(self, file_path: str, zoom_factor: int = 15):
        EZ.change_cursor(pygame.SYSTEM_CURSOR_WAIT)
        # save the screen array as a large image

        image_array = np.full(
            (int((width - menu_width) * zoom_factor), int(height * zoom_factor), 3),
            [0, 0, 255],
            dtype=np.uint8,
        )

        custom_offset = np.array(
            [self.offset[0] * zoom_factor, self.offset[1] * zoom_factor]
        )
        if self.app.explore_app_ui.toggleMandelbrot:
            image_array = EzUtils.render_mandelbrot(
                image_array,
                self.max_iter,
                self.zoom * (1 / zoom_factor),
                custom_offset,
                int((width - menu_width) * zoom_factor),
                int(height * zoom_factor),
                saturation=self.saturation,
                lightness=self.lightness,
            )
        else:
            image_array = EzUtils.render_julia(
                image_array,
                self.c,
                self.max_iter,
                self.zoom * (1 / zoom_factor),
                custom_offset,
                int((width - menu_width) * zoom_factor),
                int(height * zoom_factor),
                saturation=self.saturation,
                lightness=self.lightness,
            )

        image_surface = pygame.surfarray.make_surface(image_array)
        pygame.image.save(image_surface, file_path)

    def draw(self):
        EZ.draw_array(self.app.screen_array)

    def run(self):
        self.update()
        self.draw()


class Application:
    def __init__(self, launcher: main.Launcher):
        self.launcher = launcher
        self.fractal = EzFractal(self)
        self.resolution = width, height, menu_width
        self.screen_array = np.full((width, height, 3), [0, 0, 255], dtype=np.uint8)
        self.working_directory = os.getcwd()
        self.explore_app_ui = UI.explore_UI.ExploreUI(self)

    def check_events(self):
        pass

    @staticmethod
    def toggle_fps(toggle: bool):
        if toggle:
            EZ.update_caption(caption + " | FPS = " + str(EZ.get_fps()))
        else:
            EZ.update_caption(caption)

    def run(self):
        EZ.create_window(self.resolution[0], self.resolution[1], caption)
        self.explore_app_ui.run()
        while True:
            self.explore_app_ui.draw_return_button()
            EZ.update()
            self.check_events()
            self.explore_app_ui.check_events()
            self.toggle_fps(self.explore_app_ui.toggleFPS)
            EZ.tick(60)
            self.fractal.run()


def load():
    with open(
        os.getcwd() + "/Resources/Components/components.json", "r+", encoding="utf-8"
    ) as f:
        data = json.load(f)
        f.seek(0)
        f.truncate()

        # update move gap
        data["EzTextFields"][4]["text"], data["EzTextFields"][4]["value"] = config.get(
            "PARAMETERS", "move_gap"
        )
        data["EzTextFields"][4]["input_value"] = config.getint("PARAMETERS", "move_gap")

        # update zoom factor
        data["EzTextFields"][3]["text"] = config.get("PARAMETERS", "zoom_factor")
        data["EzTextFields"][3]["value"] = config.get("PARAMETERS", "zoom_factor")
        data["EzTextFields"][3]["input_value"] = config.getfloat(
            "PARAMETERS", "zoom_factor"
        )

        # update max iterations
        data["EzTextFields"][2]["text"] = config.get("PARAMETERS", "max_iteration")
        data["EzTextFields"][2]["value"] = config.get("PARAMETERS", "max_iteration")
        data["EzTextFields"][2]["input_value"] = config.getint(
            "PARAMETERS", "max_iteration"
        )

        json.dump(data, f)
