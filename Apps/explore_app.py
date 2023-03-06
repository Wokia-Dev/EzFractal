import numba
import numpy as np
import pygame

import Core.EZ as EZ
import UI.home_UI
import main
from Core import EzUtils
from Core.EzUtils import iter_gradient_generator, render_julia

# parameters
# secondary parameters
caption = "EZ Fractal-Explore"

# main parameters
width, height, menu_width = 700, 400, 200


class EzFractal:
    def __init__(self, app):
        self.app = app
        self.mouse_pos = np.array([0, 0])
        self.zoom = 2.8 / height
        self.offset = np.array([0.7 * width, height]) // 2
        self.max_iter = 200
        self.c = -1.0 + 0.0j
        self.zoom_gap = 1.2
        self.offset_gap = 20
        self.saturation = 0.8
        self.lightness = 0.5

    @staticmethod
    @numba.njit(fastmath=True, parallel=True)
    def render_mandelbrot(screen_array: np.array, max_iter: int, zoom: float, offset: np.array, saturation: float = 0.8,
                          lightness: float = 0.5):
        # foreach pixel in the screen array using numba parallel
        for x in numba.prange(width - menu_width):
            for y in numba.prange(height):
                # define the complex number based on the pixel coordinates, zoom and offset
                c = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
                # define the initial value of z and the number of iterations
                z = 0
                num_iter = 0
                # iterate the function until the number is diverging or the max iterations is reached
                for i in range(max_iter):
                    # julia set formula
                    z = z ** 2 + c
                    if z.real ** 2 + z.imag ** 2 > 4:
                        # if the number is diverging break the loop
                        break
                    num_iter += 1

                # define the color based on the number of iterations and set the pixel color in the screen array
                screen_array[x, y] = iter_gradient_generator(num_iter, max_iter, saturation, lightness)
                # return the screen array
        return screen_array

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
        if direction == "up":
            self.offset[1] += self.offset_gap
        elif direction == "down":
            self.offset[1] -= self.offset_gap
        elif direction == "left":
            self.offset[0] += self.offset_gap
        elif direction == "right":
            self.offset[0] -= self.offset_gap

    def reset(self):
        self.zoom = 2.8 / height
        self.offset = np.array([0.7 * width, height]) // 2

    def calculate(self):
        # update c value and max iterations
        self.c = self.app.home_screen.params[0] + self.app.home_screen.params[1] * 1j
        self.max_iter = self.app.home_screen.params[2]

        # update zoom and offset
        self.zoom_gap = self.app.home_screen.params[3]
        self.offset_gap = self.app.home_screen.params[4]

    def update(self):
        # update the screen array with the new parameters
        self.calculate()
        # render the fractal and update the screen array
        if self.app.home_screen.toggleMandelbrot:
            self.app.screen_array = self.render_mandelbrot(
                self.app.screen_array, self.max_iter, self.zoom, self.offset
            )
        else:
            if self.app.home_screen.toggleMouse:
                # define the complex number based on the mouse position, zoom and offset
                c = (self.mouse_pos[0] - self.offset[0]) * self.zoom + (
                        self.mouse_pos[1] - self.offset[1]
                ) * self.zoom * 1j
                self.app.home_screen.update_text_fields(0, c.real)
                self.app.home_screen.update_text_fields(1, c.imag)

                # render the fractal and update the screen array
                self.app.screen_array = render_julia(
                    self.app.screen_array, c, self.max_iter, self.zoom, self.offset,
                    width, height, menu_width
                )
            else:
                self.app.screen_array = render_julia(
                    self.app.screen_array, self.c, self.max_iter, self.zoom, self.offset,
                    width, height, menu_width
                )

    def save_image(self, file_path: str, zoom_factor: int = 15):
        EZ.change_cursor(pygame.SYSTEM_CURSOR_WAIT)
        # save the screen array as a large image
        image_array = np.full(((width - menu_width) * zoom_factor, height * zoom_factor, 3), [0, 0, 255],
                              dtype=np.uint8)
        custom_offset = np.array([self.offset[0] * zoom_factor, self.offset[1] * zoom_factor])
        image_array = EzUtils.render_julia(image_array, self.c, self.max_iter, self.zoom * (1 / zoom_factor),
                                           custom_offset, (width - menu_width) * zoom_factor, height * zoom_factor)
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
        self.home_screen = UI.home_UI.HomeScreen(self)
        self.resolution = width, height, menu_width
        self.screen_array = np.full((width, height, 3), [0, 0, 255], dtype=np.uint8)

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
        self.home_screen.run()
        while True:
            self.home_screen.draw_return_button()
            EZ.update()
            self.check_events()
            self.home_screen.check_events()
            self.toggle_fps(self.home_screen.toggleFPS)
            EZ.tick(60)
            self.fractal.run()
