import numpy as np
import Core.EZ as EZ
import UI.home

# parameters
# secondary parameters
caption = "EZ Fractal"

# main parameters
width, height = 700, 400
screen_array = np.full((width, height, 3), [255, 255, 255], dtype=np.uint8)


class EzFractal:
    def __init__(self, app):
        self.app = app

    def calculate(self):
        pass

    def update(self):
        # change the screen_array
        pass

    def draw(self):
        EZ.draw_array(screen_array)
        application.home_screen.run()

    def run(self):
        self.update()
        self.draw()


class Application:
    def __init__(self):
        self.fractal = EzFractal(self)
        self.home_screen = UI.home.HomeScreen(self)
        self.resolution = width, height

    def check_events(self):
        pass

    def toggle_fps(self, toggle):
        if toggle:
            EZ.update_caption(caption + " | FPS = " + str(EZ.get_fps()))
        else:
            EZ.update_caption(caption)

    def run(self):
        EZ.create_window(self.resolution[0], self.resolution[1], caption)
        self.home_screen.run()
        while True:
            EZ.update()
            self.check_events()
            self.home_screen.check_events()
            self.toggle_fps(self.home_screen.toggleFPS)
            EZ.tick(60)
            print(self.home_screen.params)
            self.fractal.run()


if __name__ == "__main__":
    application = Application()
    application.run()
