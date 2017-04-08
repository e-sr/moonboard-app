import eventlet
from bibliopixel import LEDStrip, colors
#from bibliopixel.drivers.WS2801 import  DriverWS2801
from bibliopixel.drivers.dummy_driver import DriverDummy
from draw_problem import X_GRID_NAMES
from moonboard_problems import N_HOLDS


LED_DRIVER = DriverDummy(N_HOLDS)
#LED_DRIVER = DriverWS2801(N_HOLDS)
#LED_DRIVER = DriverWS2801(50)
BRIGHTNESS = 100
HOLD_COLORS = {
    'SH': colors.Red,
    'IH': colors.Red,
    'FH': colors.Red
}
MOONBOARD_LEDS = LEDStrip(LED_DRIVER, masterBrightness=BRIGHTNESS)

def _coordinate_to_p_number(hold_coord):
    #split coordinate in x and y grid names
    x_grid_name, y_grid_name = hold_coord[0], int(hold_coord[1:])
    x = X_GRID_NAMES.index(x_grid_name)
    y=y_grid_name-1
    u= (1-(-1)**x)/2
    return (x*18 + ((1-2*u)*y - u)%18)%50

def clear_problem():
    MOONBOARD_LEDS.all_off()
    MOONBOARD_LEDS.update()

def show_problem(holds, hold_colors=HOLD_COLORS, brightness=BRIGHTNESS):

    clear_problem()
    color = {k:v for k,v in hold_colors.items()}

    for hold in holds['SH']:
        MOONBOARD_LEDS.set(_coordinate_to_p_number(hold), color['SH'])

    for hold in holds['IH']:
        MOONBOARD_LEDS.set(_coordinate_to_p_number(hold), color['IH'])

    for hold in holds['FH']:
        MOONBOARD_LEDS.set(_coordinate_to_p_number(hold), color['FH'])
    MOONBOARD_LEDS.setMasterBrightness(brightness)
    MOONBOARD_LEDS.update()

def test_leds(log_func , time = 10.0, color=colors.Red):
    """"""
    log_func({'progress': 0,'report': 'start test'})
    p=0
    for p in range(N_HOLDS):
        if p>=1:
            MOONBOARD_LEDS.setOff(p - 1)
        MOONBOARD_LEDS.set(p, color)
        MOONBOARD_LEDS.update()
        eventlet.sleep(time/N_HOLDS)
        log_func({'progress': int(p*100/N_HOLDS), 'report': "Test running...\nLed number {}.".format(p)})
    log_func({'progress': int(p*100/N_HOLDS), 'report': "Test finish...\nLed number {}.",'done':True})

if __name__=="__main__":
    print("Test MOONBOARD LEDS\n===========")
    print(test_leds.__doc__)

