# -*- coding: utf-8 -*-
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
    x_grid_names = HOLDS_CONF['grid_name']['horizontal']
    #split coordinate in x and y grid names
    x_grid_name, y_grid_name = hold_coord[0], int(hold_coord[1:])
    x = x_grid_names.index(x_grid_name)
    y=y_grid_name-1
    u= (1-(-1)**x)/2
    return offset + (x*18 + ((1-2*u)*y - u)%18)

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

def test_leds(pixels, log_func , sleep_func, delay = 20.0, color = colors.Red):
    """"""
    npixels = pixels.numLEDs
    log_func({'progress': 0,'report': 'start test'})
    npixelsON = 18
    p=0
    for p in range(npixels+npixelsON):
        if p>=1:
            pixels.setOff(p - npixelsON)
        if p <= npixels:
            pixels.set(p, color)
        pixels.update()
        sleep_func(float(delay)/npixels)
        log_func({'progress': int(p*100/(npixels+npixelsON)), 'report': "Test running...\nLed number {}.".format(p)})

    log_func({'progress': 100, 'report': "Test finish...\nLed number {}.",'done':True})

if __name__=="__main__":
    print("Test MOONBOARD LEDS\n===========")
    import argparse
    import time
    parser = argparse.ArgumentParser(description='Test led system')
    parser.add_argument('--delay',  type=float, default=10.0,
                        help='Delay of progress.')
    parser.add_argument('--on', type=int, default=0,
                        help='number of leds on starting from 0')

    args = parser.parse_args()
    pixels = init_pixels('spi')
    if not args.on:
        print("Start Led Test.")
        def f(s):
            print(s)
        test_leds(pixels=pixels, log_func=f, sleep_func=time.sleep, delay= args.delay)
    else:
        print("Turn on (red) first {} leds.".format(args.on))
        clear_problem(pixels)
        for i in range(args.on):
            pixels.set(i,colors.Red)
        pixels.update()
        print("Wait for {} before turn off leds.".format(args.duration))
        time.sleep(args.duration)
        clear_problem(pixels)





