# -*- coding: utf-8 -*-
import eventlet
from bibliopixel import LEDStrip, colors
from bibliopixel.drivers.WS2801 import  DriverWS2801
from bibliopixel.drivers.dummy_driver import DriverDummy
from moonboard_problems import HOLDS_CONF

BRIGHTNESS = 100

def init_pixels(type, npixels=200):
    try:
        if type == "spi" or type == "raspberry":
            LED_DRIVER = DriverWS2801(npixels)
        else:
            raise ValueError("device type has not in {}".format(str(['spi','raspberry'])))
    except ImportError as e:
        print("Not able to initialize the driver. Error{}".format(str(e.message)))
        print("Use bibliopixel.drivers.dummy_driver")
        LED_DRIVER = DriverDummy(npixels)

    return LEDStrip(LED_DRIVER, masterBrightness=BRIGHTNESS)

def _coordinate_to_p_number(hold_coord, offset = 2):
    x_grid_name = HOLDS_CONF['grid_name']['horizontal']

    #split coordinate in x and y grid names
    x_grid_name, y_grid_name = hold_coord[0], int(hold_coord[1:])
    x = x_grid_name.index(x_grid_name)
    y=y_grid_name-1
    u= (1-(-1)**x)/2
    return offset + (x*18 + ((1-2*u)*y - u)%18)%50

def clear_problem(pixels):
    pixels.all_off()
    pixels.update()

def show_problem(pixels, holds, hold_colors = {} , brightness=BRIGHTNESS):
    """show problem on moonboardpixels"""
    clear_problem(pixels)
    color = {k:hold_colors.get(k,(255,0,0)) for k in ['SH','IH','FH']}

    for hold in holds['SH']:
        pixels.set(_coordinate_to_p_number(hold), color['SH'])

    for hold in holds['IH']:
        pixels.set(_coordinate_to_p_number(hold), color['IH'])

    for hold in holds['FH']:
        pixels.set(_coordinate_to_p_number(hold), color['FH'])
    pixels.setMasterBrightness(brightness)
    pixels.update()

def test_leds(pixels, log_func , time = 10.0, color = colors.Red):
    """"""
    npixels = pixels.numLEDs
    log_func({'progress': 0,'report': 'start test'})
    npixelsON = 10
    p=0
    for p in range(npixels+npixelsON):
        if p>=1:
            pixels.setOff(p - npixelsON)
        if p <= npixels:
            pixels.set(p, color)
        pixels.update()
        eventlet.sleep(time/npixels)
        log_func({'progress': int(p*100/(npixels+npixelsON)), 'report': "Test running...\nLed number {}.".format(p)})

    log_func({'progress': 100, 'report': "Test finish...\nLed number {}.",'done':True})

if __name__=="__main__":
    print("Test MOONBOARD LEDS\n===========")
    print(test_leds.__doc__)
    def f(s):
        print(s)
    pixels = init_pixels('spi')
    test_leds(pixels, f)
