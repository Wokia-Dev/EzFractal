import sys
import numpy as np

import pygame

from Core import EZ
import UI.Components.EzButton
from UI.Components.EzFractalButton import EzFractalButton
import UI.Components.EzScrollView
import main as launcher
from UI.Components.EzButton import check_ez_button_event

json_file = "Resources\\Components\\popular_app_components.json"
special_button = EzFractalButton("btnS", 0, 0, 275, 110, 10, "D9D9D9", 255, "0000000", 17, "SF-Pro-Text-Regular", -1.123456789, 0.123456789, 200, 7, "Resources\\Images\\image2.png")
special_button2 = EzFractalButton("btnS", 0, 170, 275, 110, 10, "D9D9D9", 255, "0000000", 17, "SF-Pro-Text-Regular", -1.123456789, 0.123456789, 200, 7, "Resources\\Images\\image2.png")


class PopularUI:
    def __init__(self, app):
        self.app = app
        self.ez_buttons: list[
            UI.Components.EzButton.EzButton
        ] = UI.Components.EzButton.loader(json_file)
        self.ez_scrollViews: list[
            UI.Components.EzScrollView.EzScrollView
        ] = UI.Components.EzScrollView.loader(json_file)

    def scroll_view_content(self, surface: pygame.Surface):
            special_button.create_fractal_button(surface)
            special_button2.create_fractal_button(surface)

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
            scrollView.draw_on_screen(self.app.screen_array, self.app)

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
                    launcher.Launcher.run(self.app.launcher, from_return=True)
                checked_ez_button.create_button()

            # scroll view check
            for scrollView in self.ez_scrollViews:
                if scrollView.check_scroll_hover(mouse_x, mouse_y):
                    scrollView.mouse_down = True
                if scrollView.name == "scrollView":
                    test = scrollView.check_custom_hover(mouse_x, mouse_y, special_button.x, special_button.y, special_button.width, special_button.height)
                    
                    test2 = scrollView.check_custom_hover(mouse_x, mouse_y, special_button2.x, special_button2.y, special_button2.width, special_button2.height)
                    print(test, test2)

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
                    scrollView.scroll_down(self.app.resolution[1])

        # check hover and change cursor
        if any(
            button.check_hover(mouse_x, mouse_y) for button in self.ez_buttons
        ) or any(
            scrollView.check_scroll_hover(mouse_x, mouse_y)
            for scrollView in self.ez_scrollViews
        ):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)

        for scrollView in self.ez_scrollViews:
            if scrollView.mouse_down:
                scrollView.draw_scroll_bar(mouse_y)

        self.update()
