import sys

from Apps import main
import Core.EZ as EZ


def run(return_to_main=False):
    if return_to_main:
        EZ.destroy_window()
    EZ.create_window(800, 600, "Fractal")
    EZ.draw_rectangle_right(50, 50, 200, 200, "FF00FF")
    application = main.Application()
    while True:
        event = EZ.get_event()
        if event == "EXIT" or event == "KEY_DOWN" and EZ.key() == "escape":
            EZ.destroy_window()
            sys.exit()
        if event == "MOUSE_LEFT_BUTTON_DOWN":
            mouse_x, mouse_y = EZ.mouse_coordinates()
            print(mouse_x, mouse_y)
            if 50 < mouse_x < 250 and 50 < mouse_y < 250:
                application.run()

        EZ.update()
        EZ.tick(60)


if __name__ == "__main__":
    run()
