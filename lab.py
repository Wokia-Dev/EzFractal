import math
import numba

import numpy as np
import matplotlib.pyplot as plt
import Core.EZ as EZ

"""
def mandelbrot(h, w, maxit=100):
    y, x = np.ogrid[-1.4:1.4:h * 1j, -2:0.8:w * 1j]
    print("x" + str(x) + "y" + str(y))
    c = x + y * 1j
    z = c
    diverge = np.zeros(z.shape)

    for i in range(maxit):
        z = z ** 2 + c
        diverge = z * np.conj(z) > 2 ** 2  # who is diverging
        z[diverge] = 2  # avoid diverging too much

    return diverge


plt.imshow(mandelbrot(400, 400), cmap="gray")
plt.show()
"""

width, height = 500, 400


def fractal():
    screen_array = np.full((width, height, 3), [0, 0, 0], dtype=np.uint8)
    max_iter = 200
    EZ.create_window(width, height, "EZ Fractal")
    EZ.fps_settings(60)
    zoom = 2.2 / height
    offset = np.array([1.3 * width, height]) // 2
    axis = 0
    mouse_x, mouse_y = 0, 0

    while True:
        EZ.tick(60)
        event = EZ.get_event()

        if event == "EXIT":
            EZ.destroy_window()
            break
        if event == "KEY_DOWN":
            down_key = EZ.key()
            if down_key == "left ctrl":
                axis = 1
            if down_key == "left shift":
                axis = 2
            if down_key == "left alt":
                max_iter += 10

        if event == "KEY_UP":
            up_key = EZ.key()
            if up_key == "left ctrl" or up_key == "left shift":
                axis = 0
        if event == "MOUSE_MOVEMENT":
            mouse_x, mouse_y = EZ.mouse_coordinates()
        if event == "MOUSE_SCROLL_DOWN":
            if axis == 1:
                # The point at the center of the zoom is the current mouse position
                center_x = (mouse_x - offset[0]) * zoom
                center_y = (mouse_y - offset[1]) * zoom
                zoom /= 1.2
                # Recalculate the offset to keep the mouse position at the center of the zoom
                offset[0] = mouse_x - (center_x / zoom)
                offset[1] = mouse_y - (center_y / zoom)
            elif axis == 2:
                offset[1] += 20
            else:
                offset[0] -= 20
        if event == "MOUSE_SCROLL_UP":
            if axis == 1:
                # The point at the center of the zoom is the current mouse position
                center_x = (mouse_x - offset[0]) * zoom
                center_y = (mouse_y - offset[1]) * zoom
                zoom *= 1.2
                # Recalculate the offset to keep the mouse position at the center of the zoom
                offset[0] = mouse_x - (center_x / zoom)
                offset[1] = mouse_y - (center_y / zoom)
            elif axis == 2:
                offset[1] -= 20
            else:
                offset[0] += 20

        screen_array = render_juila(screen_array, zoom, offset, -0.8 + 0.156j, max_iter)
        EZ.draw_array(screen_array)
        EZ.update_caption("FPS:" + str(EZ.get_fps()))

        EZ.update()

    EZ.wait_action()


@numba.njit(fastmath=True, parallel=True)
def render(screen_array, zoom, offset, max_iterations=200):
    for x in numba.prange(width):
        for y in range(height):
            c = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
            z = 0
            num_iter = 0
            for i in range(max_iterations):
                z = z ** 2 + c
                if z.real ** 2 + z.imag ** 2 > 4:
                    break
                num_iter += 1
            color = int(255 * num_iter / max_iterations)
            screen_array[x, y] = [color, color, color]
    return screen_array


@numba.njit(fastmath=True, parallel=True)
def render_juila(screen_array, zoom, offset, c, max_iterations=200):
    for x in numba.prange(width):
        for y in numba.prange(height):
            z = (x - offset[0]) * zoom + 1j * (y - offset[1]) * zoom
            num_iter = 0
            for i in range(max_iterations):
                z = z ** 2 + c
                if z.real ** 2 + z.imag ** 2 > 4:
                    break
                num_iter += 1
            r, g, b = 0, 0, 0
            if num_iter == max_iterations:
                r, g, b = 0, 0, 0
            elif num_iter < max_iterations / 3:
                r, g, b = int(255 * (num_iter / (max_iterations / 3))), 0, 255
            elif num_iter < 2 * max_iterations / 3:
                r, g, b = 255, int(255 * (1 - ((num_iter - max_iterations / 3) / (max_iterations / 3)))), 255
            else:
                r, g, b = 255, 255, int(255 * ((num_iter - 2 * max_iterations / 3) / (max_iterations / 3)))

            screen_array[x, y] = [r, g, b]
    return screen_array


fractal()
