# -*- coding: utf-8 -*-
"""
Created on Sat Dec 8 21:07:27 2018

@author: Eric Caspar modified by Quentin
"""

import math
import os
import time

import numpy as np
import pygame
import pygame.gfxdraw
from pygame.locals import *

global window
global event
global keyboard

global fps
global start
global clock
current_file_path = os.path.dirname(__file__)

"""
List of events:
"NOTHING"
"KEY_DOWN"
"KEY_UP"
"MOUSE_MOVEMENT"
"MOUSE_RIGHT_BUTTON_DOWN"
"MOUSE_LEFT_BUTTON_DOWN"
"MOUSE_RIGHT_BUTTON_UP"
"MOUSE_LEFT_BUTTON_UP"
"MOUSE_SCROLL_UP"
"MOUSE_SCROLL_DOWN"
"EXIT"
"""


def create_window(width=300, height=200, name="window", icon=None):
    """Function that initializes the graphical part and creates a window
    of given size"""
    global window
    global keyboard
    global clock
    clock = pygame.time.Clock()
    if icon is not None:
        image = load_image(icon)
    else:
        image = create_image(25, 25)
        draw_rectangle_right(0, 0, 25, 25, "FF0000", canvas=image)
    # noinspection DuplicatedCode
    keyboard = {"q": "a", ";": "m", "a": "q", "z": "w", "w": "z", "m": ","}
    pygame.init()
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption(name)
    pygame.display.set_icon(image)
    window.fill([255, 255, 255])
    pygame.display.flip()


def test_window():
    """Test if the window is open"""
    return pygame.display.get_init()


def create_image(length, height):
    """Creation of an image (Surface) that can be modified and saved"""
    if pygame.display.get_init():
        return pygame.Surface((length, height)).convert_alpha()
    return pygame.Surface((length, height))


def get_image_color(image, x, y):
    """Retrieves a color at position x and y"""
    return image.get_at((x, y))


def color_image_pixel(image, x, y, color, transparency=255):
    """Equivalent to EZ.trace_point, except that the window is no longer the default surface"""
    draw_point(x, y, color, transparency, image)


def destroy_window():
    """Function that destroys the window"""
    pygame.quit()


def __choose(canvas):
    """Internal function"""
    if canvas is None:
        surface = window
    else:
        surface = canvas
    return surface


def wait(duration_in_microseconds=1000):
    """Function that waits for a duration in microseconds"""
    pygame.time.wait(duration_in_microseconds)


def draw_point(x, y, color, transparency=255, canvas=None):
    """Draws a point with coordinates (x, y) by default the transparency is opaque and the color is black
    If a canvas (in reality a surface) is given, then the drawing is done on the canvas and not on the screen
    """
    surface = __choose(canvas)
    rgb_color = hex_to_rgb(color)
    pygame.gfxdraw.pixel(
        surface, x, y, (rgb_color[0], rgb_color[1], rgb_color[2], transparency)
    )


def dimensions(canvas=None):
    surface = __choose(canvas)
    return pygame.Surface.get_size(surface)


def draw_segment(xA, yA, xB, yB, color="000000", transparency=255, canvas=None):
    """Draws a segment [AB] of given color (black by default) by default it is aliased
    If a canvas (in reality a surface) is given, then the drawing is done on the canvas and not on the screen
    """
    color = hex_to_rgb(color)
    surface = __choose(canvas)
    if yA == yB:
        pygame.gfxdraw.hline(
            surface, xA, xB, yA, (color[0], color[1], color[2], transparency)
        )
    elif xA == xB:
        pygame.gfxdraw.vline(
            surface, xA, yA, yB, (color[0], color[1], color[2], transparency)
        )
    else:
        pygame.gfxdraw.line(
            surface, xA, yA, xB, yB, (color[0], color[1], color[2], transparency)
        )


def draw_rectangle_right(
    xA, yA, length, height, color="000000", zoom=1, transparency=255, canvas=None
):
    """Draws a rectangle with vertical or horizontal sides, black by default.
    If a canvas is given, the drawing is done on the canvas instead of on the screen.
    """
    rgb = hex_to_rgb(color)
    surface = __choose(canvas)
    new_surface = pygame.Surface((length * zoom, height * zoom))
    new_surface.set_alpha(transparency)
    new_surface.fill(pygame.Color(rgb[0], rgb[1], rgb[2]))
    surface.blit(
        new_surface, (int(float(xA) * float(zoom)), int(float(yA) * float(zoom)))
    )


def draw_triangle(
    xA, yA, xB, yB, xC, yC, color="000000", zoom=1, transparency=255, canvas=None
):
    """Draws a triangle with the given vertices and color. The default color is black.
    If a canvas is given, the drawing is done on the canvas instead of on the screen.
    """
    rgb_color = hex_to_rgb(color)
    surface = __choose(canvas)
    pygame.gfxdraw.filled_trigon(
        surface,
        int(float(xA) * float(zoom)),
        int(float(yA) * float(zoom)),
        int(float(xB) * float(zoom)),
        int(float(yB) * float(zoom)),
        int(float(xC) * float(zoom)),
        int(float(yC) * float(zoom)),
        pygame.Color(rgb_color[0], rgb_color[1], rgb_color[2], transparency),
    )


def draw_disk(x, y, radius, color="000000", zoom=1, transparency=255, canvas=None):
    """Draws a disk with the given center, radius, and color. The default color is black.
    If a canvas is given, the drawing is done on the canvas instead of on the screen.
    """
    rgb_color = hex_to_rgb(color)
    surface = __choose(canvas)
    pygame.gfxdraw.filled_circle(
        surface,
        int(float(x) * float(zoom)),
        int(float(y) * float(zoom)),
        int(float(radius) * float(zoom)),
        pygame.Color(rgb_color[0], rgb_color[1], rgb_color[2], transparency),
    )


def draw_circle(x, y, radius, color="000000", transparency=255, canvas=None):
    """Draws a circle with the given center, radius, and color. The default color is black.
    If a canvas is given, the drawing is done on the canvas instead of on the screen.
    """
    rgb_color = hex_to_rgb(color)
    surface = __choose(canvas)
    pygame.gfxdraw.aacircle(
        surface,
        x,
        y,
        radius,
        pygame.Color(rgb_color[0], rgb_color[1], rgb_color[2], transparency),
    )


def __draw_quarter_sector1(x, y, r1, r2, angle1, angle2, color, t, canvas=None):
    mini = int(math.cos(angle2) * r1)
    maxi = int(math.cos(angle1) * r2)
    angle2_mod = math.fmod(angle2, 2 * math.pi)
    for i in range(mini, maxi + 1):
        if i == 0:
            if (angle2 > 0 and angle2_mod > math.pi / 2 - 0.00001) or (
                angle2 < 0 and angle2_mod < -3 * math.pi / 2 + 0.00001
            ):
                draw_rectangle_right(x, y - r1, x, y - r2, color, t, canvas)
        else:
            if i < r1:
                hmin = int(max(math.sqrt(abs(r1 * r1 - i * i)), math.tan(angle1) * i))
            else:
                hmin = int(math.tan(angle1) * i)
            if angle2_mod in (math.pi / 2, -3 * math.pi / 2):
                hmax = int(math.sqrt(abs(r2 * r2 - i * i)))
            else:
                hmax = int(min(math.sqrt(abs(r2 * r2 - i * i)), math.tan(angle2) * i))
            draw_rectangle_right(x + i, y - hmin, x + i, y - hmax, color, t, canvas)


def __draw_quarter_sector2(x, y, r1, r2, angle1, angle2, color, t, canvas=None):
    mini = int(math.cos(angle2) * r2)
    maxi = int(math.cos(angle1) * r1)
    angle1_mod = math.fmod(angle1, 2 * math.pi)
    for i in range(mini, maxi + 1):
        if i == 0:
            if (angle1 > 0 and angle1_mod < math.pi / 2 + 0.00001) or (
                angle1 < 0 and angle1_mod < -3 * math.pi / 2 + 0.00001
            ):
                draw_rectangle_right(x, y - r1, x, y - r2, color, t, canvas)
        else:
            if i > -r1:
                hmin = int(max(math.sqrt(abs(r1 * r1 - i * i)), math.tan(angle2) * i))
            else:
                hmin = int(math.tan(angle2) * i)
            if angle1_mod in (math.pi / 2, -3 * math.pi / 2):
                hmax = int(math.sqrt(abs(r2 * r2 - i * i)))
            else:
                hmax = int(min(math.sqrt(abs(r2 * r2 - i * i)), math.tan(angle1) * i))
            draw_rectangle_right(x + i, y - hmin, x + i, y - hmax, color, t, canvas)


def __draw_quarter_sector3(x, y, r1, r2, angle1, angle2, color, t, canvas=None):
    mini = int(math.cos(angle1) * r2)
    maxi = int(math.cos(angle2) * r1)
    angle2_mod = math.fmod(angle2, 2 * math.pi)
    for i in range(mini, maxi + 1):
        if i == 0:
            if (angle2 > 0 and angle2_mod > 3 * math.pi / 2 - 0.00001) or (
                angle2 < 0 and angle2_mod > -math.pi / 2 - 0.00001
            ):
                draw_rectangle_right(x, y + r1, x, y + r2, color, t, canvas)
        else:
            # noinspection DuplicatedCode
            if i > -r1:
                hmin = int(
                    max(math.sqrt(abs(r1 * r1 - i * i)), math.tan(angle1) * (-i))
                )
            else:
                hmin = int(math.tan(angle1) * (-i))
            if angle2_mod in (-math.pi / 2, 3 * math.pi / 2):
                hmax = int((math.sqrt(abs(r2 * r2 - i * i))))
            else:
                hmax = int(
                    min(math.sqrt(abs(r2 * r2 - i * i)), math.tan(angle2) * (-i))
                )
            draw_rectangle_right(x + i, y + hmin, x + i, y + hmax, color, t, canvas)


def __draw_quarter_sector4(x, y, r1, r2, angle1, angle2, color, t, canvas=None):
    mini = int(math.cos(angle1) * r1)
    maxi = int(math.cos(angle2) * r2)
    angle1_mod = math.fmod(angle1, 2 * math.pi)
    for i in range(mini, maxi + 1):
        if i == 0 and r1 != 0:
            if (angle1 > 0 and angle1_mod < 3 * math.pi / 2 + 0.00001) or (
                angle1 < 0 and angle1_mod < -math.pi / 2 + 0.00001
            ):
                draw_rectangle_right(x, y + r1, x, y + r2, color, t, canvas)
        else:
            if i < r1:
                hmin = int(max(math.sqrt(abs(r1 * r1 - i * i)), -math.tan(angle2) * i))
            else:
                hmin = -int(math.tan(angle2) * i)
            if angle1_mod in (-math.pi / 2, 3 * math.pi / 2):
                hmax = int((math.sqrt(abs(r2 * r2 - i * i))))
            else:
                hmax = int(
                    min(math.sqrt(abs(r2 * r2 - i * i)), math.tan(angle1) * (-i))
                )
            draw_rectangle_right(x + i, y + hmin, x + i, y + hmax, color, t, canvas)


def draw_angular_sector(
    x, y, r1, r2, angle1, angle2, color, transparency=255, canvas=None
):
    """Draw an angular sector delimited by two radius, be careful the function is slow
    If you give a canvas then the drawing is done on the canvas and not on the screen"""
    mini, maxi = min(angle1, angle2), max(angle1, angle2)
    function = [
        __draw_quarter_sector1,
        __draw_quarter_sector2,
        __draw_quarter_sector3,
        __draw_quarter_sector4,
    ]
    if maxi - mini >= 360:
        __draw_quarter_sector1(
            x, y, r1, r2, 0, math.pi / 2, color, transparency, canvas
        )
        __draw_quarter_sector2(
            x, y, r1, r2, math.pi / 2, math.pi, color, transparency, canvas
        )
        __draw_quarter_sector3(
            x, y, r1, r2, math.pi, 3 * math.pi / 2, color, transparency, canvas
        )
        __draw_quarter_sector4(
            x, y, r1, r2, 3 * math.pi / 2, 2 * math.pi, color, transparency, canvas
        )
    else:
        start_angular = mini // 90
        start_angle = mini
        while True:
            if maxi < start_angular * 90 + 90:
                function[start_angular % 4](
                    x,
                    y,
                    r1,
                    r2,
                    math.radians(start_angle),
                    math.radians(maxi),
                    color,
                    transparency,
                    canvas,
                )
                return
            function[start_angular % 4](
                x,
                y,
                r1,
                r2,
                math.radians(start_angle),
                math.radians(start_angular * 90 + 90),
                color,
                transparency,
                canvas,
            )
            start_angle = start_angular * 90 + 90
            start_angular += 1


def draw_arc(x, y, r, angle1, angle2, color="000000", transparency=255, canvas=None):
    """Draws a circle arc, with a given center and between two given angles in degrees
    If a canvas is given, the drawing is done on the canvas instead of on the screen"""
    rgb_color = hex_to_rgb(color)
    surface = __choose(canvas)
    mini, maxi = min(-angle1, -angle2), max(-angle1, -angle2)
    pygame.gfxdraw.arc(
        surface,
        x,
        y,
        r,
        mini,
        maxi,
        (rgb_color[0], rgb_color[1], rgb_color[2], transparency),
    )


def draw_ellipse(
    x,
    y,
    horizontal_radius,
    vertical_radius,
    color="000000",
    transparency=255,
    canvas=None,
):
    """Draws an ellipse (oval) with center (x, y) and given horizontal and vertical radius.
    The ellipse is straight"""
    rgb_color = hex_to_rgb(color)
    surface = __choose(canvas)
    pygame.gfxdraw.aaellipse(
        surface,
        x,
        y,
        horizontal_radius,
        vertical_radius,
        (rgb_color[0], rgb_color[1], rgb_color[2], transparency),
    )


def draw_filled_ellipse(
    x, y, horizontal_radius, vertical_radius, color, transparency=255, canvas=None
):
    """Draws the interior of an ellipse (oval) with center (x, y) and given horizontal and vertical radius.
    The ellipse is straight"""
    rgb = hex_to_rgb(color)
    surface = __choose(canvas)
    pygame.gfxdraw.filled_ellipse(
        surface,
        x,
        y,
        horizontal_radius,
        vertical_radius,
        (rgb[0], rgb[1], rgb[2], transparency),
    )


def load_image(path, local=True):
    """Loads an image from the given path"""
    if not local:
        path = os.path.join(current_file_path, path)

    if pygame.display.get_init:
        return pygame.image.load(path)
    return pygame.image.load(path)


def load_image_as_matrix(path, local=True):
    """Loads an image from the given path and returns a matrix of tuples (r, v, b)"""
    if not local:
        path = os.path.join(current_file_path, path)

    if pygame.display.get_init:
        image = pygame.image.load(path).convert_alpha()
    else:
        image = pygame.image.load(path)
    l, h = dimensions(image)
    tab = [l * [0] for _ in range(h)]
    for row in range(h):
        for column in range(l):
            tab[row][column] = get_image_color(image, column, row)
    return tab


def save_image(image, path, local=True):
    """Saves an image at the given path"""
    if not local:
        path = os.path.join(current_file_path, path)
    pygame.image.save(image, path)


def save_image_matrix(mat, path, local=True):
    """Saves an image given as a matrix at the given path"""
    if not local:
        path = os.path.join(current_file_path, path)
    image = create_image(len(mat[0]), len(mat))
    for row, item in enumerate(mat):
        for column in range(len(mat[0])):
            color_image_pixel(image, column, row, item[column][0], item[column][1])
    save_image(image, path)


def draw_image(
    image,
    x,
    y,
    transparency=255,
    canvas=None,
    border_radius=0,
    border_color="000000",
    border_width=0,
):
    """Draws an image at the given position. Note that if you apply transparency, the image must not be transparent
    itself. By default, the image is drawn on the graphics window, but it can be placed in a canvas (surface)
    """
    surface = __choose(canvas)
    if transparency < 255:
        image2 = pygame.Surface(image.get_size())
        image2.set_alpha(transparency)
        image2.blit(image, (0, 0))
        surface.blit(image2, (x, y))
    else:
        surface.blit(image, (x, y))


def transform_image(image, angle=0, zoom=1.0):
    """Transforms an image with a rotation and/or zoom to give a new image"""
    return pygame.transform.rotozoom(image, angle, zoom)


def select_part_of_image(image, x, y, w, h):
    """
    Selects a part of the preloaded image.
    Note that modifying the selected image also modifies the original image, so there is no memory creation.
    However, you can use the transformation function on it or display it.
    """
    return image.subsurface(Rect(x, y, w, h))


def get_event():
    """Gets an event
    List of events:
    "NOTHING"
    "KEY_DOWN"
    "KEY_UP"
    "MOUSE_MOVEMENT"
    "MOUSE_RIGHT_BUTTON_DOWN"
    "MOUSE_LEFT_BUTTON_DOWN"
    "MOUSE_RIGHT_BUTTON_UP"
    "MOUSE_LEFT_BUTTON_UP"
    "MOUSE_SCROLL_UP"
    "MOUSE_SCROLL_DOWN"
    "EXIT"
    """
    global event
    event = pygame.event.poll()
    if event == pygame.NOEVENT:
        return "NOTHING"
    if event.type == pygame.KEYDOWN:
        return "KEY_DOWN"
    if event.type == pygame.KEYUP:
        return "KEY_UP"
    if event.type == pygame.MOUSEMOTION:
        return "MOUSE_MOVEMENT"
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 1:
            return "MOUSE_LEFT_BUTTON_DOWN"
        if event.button == 3:
            return "MOUSE_RIGHT_BUTTON_DOWN"
        if event.button == 4:
            return "MOUSE_SCROLL_UP"
        if event.button == 5:
            return "MOUSE_SCROLL_DOWN"
        return "NOTHING"
    if event.type == pygame.MOUSEBUTTONUP:
        if event.button == 1:
            return "MOUSE_LEFT_BUTTON_UP"
        if event.button == 3:
            return "MOUSE_RIGHT_BUTTON_UP"
        if event.button == 4:
            return "MOUSE_SCROLL_UP"
        if event.button == 5:
            return "MOUSE_SCROLL_DOWN"
        return "NOTHING"
    if event.type == pygame.QUIT:
        return "EXIT"
    return "NOTHING"


def mouse_x():
    """Gives the x-coordinate of the mouse at the time the event is retrieved"""
    return event.pos[0]


def mouse_y():
    """Gives the y-coordinate of the mouse at the time the event is retrieved"""
    return event.pos[1]


def mouse_coordinates():
    """Gives the coordinates of the mouse"""
    return pygame.mouse.get_pos()


def key():
    """Gives the key pressed at the time the event is retrieved as a string"""
    character = pygame.key.name(event.key)
    return keyboard.get(character, character)


def get_key_pressed():
    """Get the key that was pressed and print it to the console. Returns 1 if the right mouse button is pressed,
    which can be used to exit the program."""
    if pygame.display.get_init():
        while True:
            current_event = get_event()
            if current_event == "KEY_DOWN":
                print(key())
            elif current_event == "MOUSE_RIGHT_BUTTON_DOWN":
                return 1
            else:
                create_window(400, 400)
                while True:
                    current_event = get_event()
                    if current_event == "KEY_DOWN":
                        print(key())
                    elif current_event == "MOUSE_RIGHT_BUTTON_DOWN":
                        destroy_window()
                        return 1


def save_window():
    """Returns an image (surface) of the screen"""
    return window.copy()


def load_music(path=None, local=True):
    """Loads a music that can be played with the music on function"""
    if not local:
        path = os.path.join(current_file_path, path)
    if path is not None:
        pygame.mixer.music.load(path)


def music_on(nb_loops=-1):
    """Plays the previously loaded music"""
    pygame.mixer.music.play(nb_loops)


def music_pause():
    """pauses the music"""
    pygame.mixer.music.pause()


def music_end_break():
    """Ends the music pause"""
    pygame.mixer.music.unpause()


def stop_music():
    """Stop the music"""
    pygame.mixer.music.stop()


def music_volume(volume=0.5):
    """Set a volume to the music"""
    pygame.mixer.music.set_volume(volume)


def load_sound(path=None, local=True):
    """Loads a sound that can be played after"""
    if not local:
        path = os.path.join(current_file_path, path)
    if path is not None:
        return pygame.mixer.Sound(path)


def play_sound(sound=None):
    """Plays the given sound"""
    sound.play()


def wait_action():
    """Waits for an action from the user"""
    wait_state = True
    valid_events = [
        "MOUSE_LEFT_BUTTON_DOWN",
        "MOUSE_RIGHT_BUTTON_DOWN",
        "KEY_DOWN",
        "EXIT",
    ]
    while wait_state:
        current_event = get_event()
        wait_state = current_event not in valid_events


def update():
    """Updating the screen."""
    pygame.display.flip()


def get_time():
    """Gives the duration in seconds."""
    return time.time()


def load_font(size=40, font_name=None, local=True):
    """Defines the size and font name."""
    if font_name is not None and not local:
        font_name = os.path.join(current_file_path, font_name)
    return pygame.font.Font(font_name, size)


def image_text(text, font, color="000000", antialiasing=True, tuple_background=None):
    """Returns an image containing the text to be displayed."""
    rgb_color = hex_to_rgb(color)
    return font.render(
        text, antialiasing, (rgb_color[0], rgb_color[1], rgb_color[2]), tuple_background
    )


def fps_settings(n=60):
    """
    The setting gives the maximum number of frames per second.
    """
    global fps
    global start
    fps = n
    start = pygame.time.Clock()


def next_frame():
    """
    Wait for the necessary time to have the requested number of frames per second between two calls.
    """
    start.tick(fps)


def draw_array(array, canvas=None):
    """
    Draws an array of pixels on the screen.
    """
    pygame.surfarray.blit_array(__choose(canvas), array)


def get_screen_array(start_width, surface=None):
    """
    Returns an array of pixels of the screen.
    """
    if surface:
        return np.asarray(pygame.surfarray.array3d(surface), dtype=np.uint8)[
            start_width:
        ]
    if start_width:
        return np.asarray(pygame.surfarray.array3d(window), dtype=np.uint8)[
            start_width:
        ]
    if not start_width:
        if surface:
            return np.asarray(pygame.surfarray.array3d(surface), dtype=np.uint8)
        return np.asarray(pygame.surfarray.array3d(window), dtype=np.uint8)


def get_fps():
    """
    Returns the number of frames per second.
    """
    return int(clock.get_fps())


def tick(n=60):
    """
    Returns the number of milliseconds since the last call to tick.
    """
    clock.tick(n)


def update_caption(caption):
    """
    Updates the caption of the window.
    """
    pygame.display.set_caption(caption)


def array3d(texture):
    """
    Returns a 3D array of the texture.
    """
    return pygame.surfarray.array3d(texture)


def change_cursor(cursor):
    """
    Changes the cursor.
    """
    pygame.mouse.set_cursor(cursor)


def create_surface(width, height):
    """
    Creates a surface.
    """
    return pygame.Surface((width, height))


def hex_to_rgb(hexa):
    return tuple(int(hexa[i : i + 2], 16) for i in (0, 2, 4))
