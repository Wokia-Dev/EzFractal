import json
import sys
import webbrowser
from multiprocessing import Pool

import pygame
import platform

import UI.Components.EzComplexButton
from Core import EZ
from Core.EzUtils import generate_image
from UI.Components.EzComplexButton import check_ez_complex_button_event

json_file = "/Resources/Components/launcher_components.json"


def load_popular_app():
    app_json_file = "Resources/Components/popular_app_components.json"

    with open(app_json_file, "r", encoding="utf-8") as file:
        data = json.load(file)

    nb_buttons = len(data["EzFractalButtons"])
    for i, button in enumerate(data["EzFractalButtons"]):
        generate_image(
            button["c_real"],
            button["c_imag"],
            button["max_iterations"],
            "popular_fractal_" + str(i) + ".png",
        )

    with open(app_json_file, "w") as file:
        json.dump(data, file, separators=(",", ":"))


class LauncherUI:
    def __init__(self, app, explore_app):
        self.app = app
        self.explore_app = explore_app
        self.ez_complex_buttons: list[
            UI.Components.EzComplexButton.EzComplexButton
        ] = UI.Components.EzComplexButton.loader(
            self.explore_app.working_directory + json_file, self.complex_button_content
        )
        self.ez_texts: list[UI.Components.EzText] = UI.Components.EzText.loader(
            self.explore_app.working_directory + json_file
        )

    def draw(self):
        for complex_button in self.ez_complex_buttons:
            complex_button.create_complex_button()

        for text in self.ez_texts:
            text.create_text()

    def complex_button_content(
        self, name: str, x: int, y: int, width: int, height: int
    ) -> None:
        # Draw the content of the complex button
        if name == "btnSettings":
            settings_icon = EZ.load_image("Resources/Images/settings_icon.png")
            EZ.draw_image(settings_icon, x, y)
        elif name == "btnGithub":
            github_icon = EZ.load_image("Resources/Images/github_icon.png")
            EZ.draw_image(github_icon, x, y)

        # main buttons
        elif name == "btnExplore":
            explore_icon = EZ.load_image("Resources/Images/explore_icon.png")
            EZ.draw_image(
                explore_icon, x + 20, y + (height - explore_icon.get_height()) / 2
            )
        elif name == "btnSaved":
            saved_icon = EZ.load_image("Resources/Images/saved_icon.png")
            EZ.draw_image(
                saved_icon, x + 20, y + (height - saved_icon.get_height()) / 2
            )
        elif name == "btnPopular":
            popular_icon = EZ.load_image("Resources/Images/popular_icon.png")
            EZ.draw_image(
                popular_icon, x + 20, y + (height - popular_icon.get_height()) / 2
            )
        elif name == "btnDocs":
            docs_icon = EZ.load_image("Resources/Images/docs_icon.png")
            EZ.draw_image(docs_icon, x + 20, y + (height - docs_icon.get_height()) / 2)

    def update(self):
        pass

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

        if event == "MOUSE_LEFT_BUTTON_DOWN":
            checked_complex_button = check_ez_complex_button_event(
                self.ez_complex_buttons, mouse_x, mouse_y
            )
            if checked_complex_button is not None:
                if checked_complex_button.name == "btnExplore":
                    # EZ.destroy_window()
                    self.app.application.run()
                elif checked_complex_button.name == "btnGithub":
                    try:
                        webbrowser.open("https://github.com/Wokia-Dev/EzFractal")
                    except Exception as e:
                        print("Error: ", e)
                elif checked_complex_button.name == "btnPopular":
                    load_popular_app()
                    self.app.popular_app.popular_app_ui.update_fractal_buttons()
                    self.app.popular_app.run()
                elif checked_complex_button.name == "btnSaved":
                    self.app.saved_app.saved_app_ui.update_images(
                        self.app.saved_app.saved_app_ui.get_images_count()
                    )
                    self.app.saved_app.run()
                elif checked_complex_button.name == "btnDocs":
                    try:
                        webbrowser.open("Resources/Help/help.html")
                    except FileNotFoundError:
                        print("Help file not found.")
                        print(
                            "Please make sure you have a help.html file in the help directory."
                        )
        if any(
            complex_button.check_hover(mouse_x, mouse_y)
            for complex_button in self.ez_complex_buttons
        ):
            EZ.change_cursor(pygame.SYSTEM_CURSOR_HAND)
        else:
            EZ.change_cursor(pygame.SYSTEM_CURSOR_ARROW)
