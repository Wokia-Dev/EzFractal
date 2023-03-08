import sys
import numpy as np

import pygame

from Core import EZ
import UI.Components.EzButton
import UI.Components.EzScrollView
import UI.Components.EzFractalButton
import main as launcher
from UI.Components.EzButton import check_ez_button_event

json_file = "/Resources/Components/popular_app_components.json"


class PopularUI:
    def __init__(self, popular_app, app):
        self.popular_app = popular_app
        self.app = app
        self.ez_buttons: list[
            UI.Components.EzButton.EzButton
        ] = UI.Components.EzButton.loader(self.app.working_directory + json_file)
        self.ez_scrollViews: list[
            UI.Components.EzScrollView.EzScrollView
        ] = UI.Components.EzScrollView.loader(self.app.working_directory + json_file)
        self.ez_fractal_buttons = None

    def update_fractal_buttons(self):
        # update the fractal buttons
        self.ez_fractal_buttons: list[
            UI.Components.EzFractalButton.EzFractalButton
        ] = UI.Components.EzFractalButton.loader(self.app.working_directory + json_file)

    def scroll_view_content(self, surface: pygame.Surface):
        for button in self.ez_fractal_buttons:
            button.create_fractal_button(surface)

    def draw(self):
        # draw the buttons
        for button in self.ez_buttons:
            button.create_button()

        # draw the scroll view
        for scrollView in self.ez_scrollViews:
            scrollView.create_scroll_view(self.scroll_view_content)

    def run(self):
        self.draw()
        self.update()

    def update(self):
        # update the scroll view
        for scrollView in self.ez_scrollViews:
            scrollView.draw_on_screen(self.popular_app.screen_array, self.popular_app)

    def check_events(self):
        # get the event from EZ
        event = EZ.get_event()
        # get mouse position
        mouse_x, mouse_y = EZ.mouse_coordinates()

        # quit the program if the user clicks the exit button
        if event == "EXIT" or event == "KEY_DOWN" and EZ.key() == "escape":
            EZ.destroy_window()
            sys.exit()

        # check if the user clicks the mouse
        if event == "MOUSE_LEFT_BUTTON_DOWN":
            # check if the user clicked a button or toggle
            checked_ez_button = check_ez_button_event(self.ez_buttons, mouse_x, mouse_y)

            # button check
            if checked_ez_button is not None:
                # help button -> open help.html
                if checked_ez_button.name == "btnReturn":
                    launcher.Launcher.run(self.popular_app.launcher, from_return=True)
                checked_ez_button.create_button()

            # scroll view check
            for scrollView in self.ez_scrollViews:
                if scrollView.check_scroll_hover(mouse_x, mouse_y):
                    scrollView.mouse_down = True
                if scrollView.name == "scrollView":
                    for button in self.ez_fractal_buttons:
                        # open explore app with the clicked fractal
                        if scrollView.check_custom_hover(
                            mouse_x,
                            mouse_y,
                            button.x,
                            button.y,
                            button.width,
                            button.height,
                        ):
                            self.popular_app.application.explore_app_ui.params[
                                0
                            ] = button.c_real
                            self.popular_app.application.explore_app_ui.params[
                                1
                            ] = button.c_imaginary
                            self.popular_app.application.fractal.c = np.complex(
                                button.c_real, button.c_imaginary
                            )
                            self.popular_app.application.fractal.reset()
                            self.popular_app.application.run()

        if event == "MOUSE_LEFT_BUTTON_UP":
            for scrollView in self.ez_scrollViews:
                scrollView.mouse_down = False

        if event == "MOUSE_SCROLL_UP":
            for scrollView in self.ez_scrollViews:
                if scrollView.check_hover(mouse_x, mouse_y):
                    scrollView.scroll_up()

        if event == "MOUSE_SCROLL_DOWN":
            for scrollView in self.ez_scrollViews:
                if scrollView.check_hover(mouse_x, mouse_y):
                    scrollView.scroll_down(self.popular_app.resolution[1])

        # check hover and change cursor
        if (
            any(button.check_hover(mouse_x, mouse_y) for button in self.ez_buttons)
            or any(
                scrollView.check_scroll_hover(mouse_x, mouse_y)
                for scrollView in self.ez_scrollViews
            )
            or any(
                scrollView.check_custom_hover(
                    mouse_x, mouse_y, button.x, button.y, button.width, button.height
                )
                for scrollView in self.ez_scrollViews
                for button in self.ez_fractal_buttons
            )
        ):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for scrollView in self.ez_scrollViews:
            if scrollView.mouse_down:
                scrollView.draw_scroll_bar(mouse_y)

        self.update()
