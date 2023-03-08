import os
from typing import List, Union

import numba
import numpy as np
from numpy import uint8
import pygame


def is_float(element: any) -> bool:
    if element is None:
        return False
    try:
        float(element)
        return True
    except ValueError:
        return False


def clamp(
    value: Union[float, int], min_value: Union[float, int], max_value: Union[float, int]
) -> Union[float, int]:
    return max(min(value, max_value), min_value)


@numba.njit(fastmath=True)
def iter_gradient_generator(
    num_iter: int, max_iter: int, saturation: float = 0.8, lightness: float = 0.5
) -> list[int]:
    if num_iter == max_iter:
        return [0, 0, 0]
    else:
        h = num_iter / max_iter
        c = (1 - np.abs(2 * lightness - 1)) * saturation
        x = c * (1 - np.abs((h * 6) % 2 - 1))
        m = lightness - c / 2
        if 0 <= h < 1 / 6:
            r, g, b = c + m, x + m, m
        elif 1 / 6 <= h < 1 / 3:
            r, g, b = x + m, c + m, m
        elif 1 / 3 <= h < 1 / 2:
            r, g, b = m, c + m, x + m
        elif 1 / 2 <= h < 2 / 3:
            r, g, b = m, x + m, c + m
        elif 2 / 3 <= h < 5 / 6:
            r, g, b = x + m, m, c + m
        else:
            r, g, b = c + m, m, x + m
    return [int(r * 255), int(g * 255), int(b * 255)]


@numba.njit(fastmath=True, parallel=True)
def render_julia(
    screen_array: np.array,
    c: complex,
    max_iter: int,
    zoom: float,
    offset: np.array,
    width: int,
    height: int,
    menu_width: int = 0,
    saturation: float = 0.8,
    lightness: float = 0.5,
):
    # foreach pixel in the screen array using numba parallel
    for x in numba.prange(width - menu_width):
        for y in numba.prange(height):
            # define the complex number based on the pixel coordinates, zoom and offset
            z = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
            # number of iterations
            num_iter = 0

            # iterate the function until the number is diverging or the max iterations is reached
            for i in range(max_iter):
                # julia set formula
                z = z**2 + c
                if z.real**2 + z.imag**2 > 4:
                    # exit the loop if the number is diverging
                    break
                num_iter += 1

            # define the color based on the number of iterations and set the pixel color in the screen array
            screen_array[x, y] = iter_gradient_generator(
                num_iter, max_iter, saturation, lightness
            )
    # return the screen array
    return screen_array


@numba.njit(fastmath=True, parallel=True)
def render_mandelbrot(
    screen_array: np.array,
    max_iter: int,
    zoom: float,
    offset: np.array,
    width: int,
    height: int,
    menu_width: int = 0,
    saturation: float = 0.8,
    lightness: float = 0.5,
):
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
                z = z**2 + c
                if z.real**2 + z.imag**2 > 4:
                    # if the number is diverging break the loop
                    break
                num_iter += 1

            # define the color based on the number of iterations and set the pixel color in the screen array
            screen_array[x, y] = iter_gradient_generator(
                num_iter, max_iter, saturation, lightness
            )
            # return the screen array
    return screen_array


def generate_image(
    c_real: float, c_imaginary: float, max_iter: int, image_name: str
) -> None:
    path = "/Resources/Images/Popular_fractals/"
    surface = pygame.Surface((500, 400))
    screen_array = np.zeros((500, 400, 3), dtype=np.uint8)
    c = c_real + c_imaginary * 1j
    screen_array = render_julia(
        screen_array, c, max_iter, 0.007, np.array([250, 200]), 500, 400
    )
    pygame.surfarray.blit_array(surface, screen_array)
    pygame.image.save(surface, os.getcwd() + path + image_name)
    pygame.quit()
