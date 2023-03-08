import os
import sys

import pygame

import UI.Components.EzButton
import main as launcher
from Core import EZ, EzUtils
from UI.Components.EzButton import check_ez_button_event

json_file = "/Resources/Components/saved_app_components.json"
gallery_path = "/Resources/Images/Saved_fractals"


class SavedUI:
    def __init__(self, saved_app, app):
        self.saved_app = saved_app
        self.app = app
        self.ez_buttons: list[UI.Components.EzButton] = UI.Components.EzButton.loader(
            self.app.working_directory + json_file
        )
        self.ez_scrollViews: list[
            UI.Components.EzScrollView
        ] = UI.Components.EzScrollView.loader(self.app.working_directory + json_file)
        self.images = []
        self.update_images(self.get_images_count())

    def get_images_count(self):
        return EzUtils.clamp(
            len(
                [
                    file
                    for file in os.listdir(self.app.working_directory + gallery_path)
                    if file.endswith(".png") and any(char.isdigit() for char in file)
                ]
            ),
            0,
            12,
        )

    # update the images list
    def update_images(self, count: int):
        self.images = []
        for index_img in range(count):
            image = EZ.load_image(f"{self.app.working_directory + gallery_path}/image{index_img}.png")
            image = pygame.transform.scale(image, (175, 140))
            self.images.append(image)

    def scroll_view_content(self, surface: pygame.Surface):
        y = 0
        minus = 0
        # draw the images
        for i in range(self.get_images_count()):
            x = 185 * i - minus
            if x >= 555:
                x = 0
                y = y + 150
                minus = 185 * i
            EZ.draw_image(self.images[i], x, y, canvas=surface)

    def draw(self):
        # draw the buttons
        for button in self.ez_buttons:
            button.create_button()

        # draw the scroll view
        for scrollView in self.ez_scrollViews:
            scrollView.create_scroll_view(self.scroll_view_content)

    def update(self):
        # update the scroll view
        for scrollView in self.ez_scrollViews:
            scrollView.draw_on_screen(self.saved_app.screen_array, self.saved_app)

    def run(self):
        self.draw()
        self.update()

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
                    launcher.Launcher.run(self.saved_app.launcher, from_return=True)
                checked_ez_button.create_button()

            # scroll view check
            for scrollView in self.ez_scrollViews:
                if scrollView.check_scroll_hover(mouse_x, mouse_y):
                    scrollView.mouse_down = True

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
                    scrollView.scroll_down(self.saved_app.resolution[1])

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
