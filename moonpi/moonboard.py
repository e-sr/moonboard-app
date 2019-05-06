# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from bibliopixel.colors import COLORS
from bibliopixel import Matrix
from bibliopixel.drivers.PiWS281X import PiWS281X
from bibliopixel.drivers.dummy_driver import DriverDummy

from moonpi.problems.moonboard_problems import HOLDS_CONF


class MoonBoard:
    DEFAULT_COLOR = COLORS.Green
    HOLDS = HOLDS_CONF["grid_name"]["xy"]
    COORDS = [
        # Top panel
        [137, 138, 149, 150, 161, 162, 173, 174, 186, 186, 197],
        [136, 139, 148, 151, 160, 163, 172, 175, 184, 187, 196],
        [135, 140, 147, 152, 159, 164, 171, 176, 183, 188, 195],
        [134, 141, 146, 153, 158, 165, 170, 177, 182, 189, 194],
        [133, 142, 145, 154, 157, 166, 169, 178, 181, 190, 193],
        [132, 143, 144, 155, 156, 167, 168, 179, 180, 191, 192],
        # Middle panel
        [131, 120, 119, 108, 107, 96, 95, 84, 83, 72, 71],
        [130, 121, 118, 109, 106, 97, 94, 85, 82, 73, 70],
        [129, 122, 117, 110, 105, 98, 93, 86, 81, 74, 69],
        [128, 123, 116, 111, 104, 99, 92, 87, 80, 75, 68],
        [127, 124, 115, 112, 103, 100, 91, 88, 79, 76, 67],
        [126, 125, 114, 113, 102, 101, 90, 89, 78, 77, 66],
        # Bottom panel
        [5, 6, 17, 18, 29, 30, 41, 42, 53, 54, 65],
        [4, 7, 16, 19, 28, 31, 40, 43, 52, 55, 64],
        [3, 8, 15, 20, 27, 32, 39, 44, 51, 56, 63],
        [2, 9, 14, 21, 26, 33, 38, 45, 50, 57, 62],
        [1, 10, 13, 22, 25, 34, 37, 46, 49, 58, 61],
        [0, 11, 12, 23, 24, 35, 36, 47, 48, 59, 60],
    ]

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
                             coord_map=self.COORDS
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

    def show_problem(self, holds, hold_colors={}):
        self.clear()
        color = {k: hold_colors.get(k, self.DEFAULT_COLOR) for k in ['SH', 'IH', 'FH']}

        for hold in holds['SH']:
            self.set_hold(hold, color['SH'])

        for hold in holds['IH']:
            self.set_hold(hold, color['IH'])

        for hold in holds['FH']:
            self.set_hold(hold, color['FH'])

        self.layout.push_to_driver()

    def run_animation(self, animation, run_options={}, **kwds):
        self.stop_animation()
        self.animation = animation(self.layout, **kwds)
        self.animation.run(**run_options)

    def stop_animation(self):
        if self.animation is not None:
            self.animation.stop()
