# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from bibliopixel.colors import COLORS
from bibliopixel import Matrix, Rotation
from bibliopixel.drivers.PiWS281X import PiWS281X
from bibliopixel.drivers.dummy_driver import DriverDummy

from moonpi.problems.moonboard_problems import HOLDS_CONF

BRIGHTNESS = 100


class MoonBoard:
    DEFAULT_COLOR = COLORS.Green
    HOLDS = HOLDS_CONF["grid_name"]["xy"]

    def __init__(self, num_pixels=198):
        try:
            driver = PiWS281X(num_pixels)
        except (ImportError, ValueError) as e:
            print("Not able to initialize the driver. Error{}".format(e))
            print("Use bibliopixel.drivers.dummy_driver")
            driver = DriverDummy(num_pixels)

        self.layout = Matrix(driver,
                             width=11,
                             height=18,
                             brightness=BRIGHTNESS,
                             rotation=Rotation.ROTATE_0,
                             vert_flip=True
                             )
        self.animation = None

    def clear(self):
        self.stop_animation()
        self.layout.all_off()
        self.layout.push_to_driver()

    def set_hold(self, hold, color=DEFAULT_COLOR):
        x_grid_names = HOLDS_CONF['grid_name']['horizontal']
        x_grid_name, y_grid_name = hold[0], int(hold[1:])
        x = x_grid_names.index(x_grid_name)
        y = 18 - y_grid_name
        self.layout.set(x, y, color)

    def show_hold(self, hold, color=DEFAULT_COLOR):
        self.set_hold(hold, color)
        self.layout.push_to_driver()

    def show_problem(self, holds, hold_colors={}, brightness=BRIGHTNESS):
        print(holds)
        self.clear()
        color = {k: hold_colors.get(k, self.DEFAULT_COLOR) for k in ['SH', 'IH', 'FH']}

        for hold in holds['SH']:
            self.set_hold(hold, color['SH'])

        for hold in holds['IH']:
            self.set_hold(hold, color['IH'])

        for hold in holds['FH']:
            self.set_hold(hold, color['FH'])

        self.layout.set_brightness(brightness)
        self.layout.push_to_driver()

    def run_animation(self, animation, run_options={}, **kwds):
        self.stop_animation()
        self.animation = animation(self.layout, **kwds)
        self.animation.run(**run_options)

    def stop_animation(self):
        if self.animation is not None:
            self.animation.stop()
