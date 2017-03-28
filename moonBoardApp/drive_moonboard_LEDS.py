import eventlet
from bibliopixel import LEDStrip, colors
#from bibliopixel.drivers.WS2801 import  DriverWS2801
from bibliopixel.drivers.dummy_driver import DriverDummy
def _pixel_on(moonboard, row, column, color, brightness):
    pass

def _pixel_off(moonboard,row, column, color, brightness):
    pass

def init_moonboard(led_driver, pixels):
    pass


def test_leds(moonboard, log_func ,speed=0.2):
    """
    TEST moonboadr docsstring
    :param moonboard:
    :param speed:
    :param color:
    """
    log_func({'progress': 0,'report': 'start test'})
    steps = range(1, )
    for i in steps:
        eventlet.sleep(2)
        log_func({'progress': int(i*100/len(steps)), 'report': "Iteration {}.".format(i)})

    log_func({'progress': int(i*100/len(steps)), 'report': 'test finish','done':True})

def show_problem(moonboard, holds, brightness= 100, color= None):
    """

    :param moonboard:
    :param holds:
    :param bightness:
    :param color:
    """
    pass

LED_DRIVER = DriverDummy(200)
#LED_DRIVER = DriverWS2801(50)
PIXELS = LEDStrip(LED_DRIVER, masterBrightness=100)
MOONBOARD_LEDS = init_moonboard(LED_DRIVER,PIXELS)

if __name__=="__main__":
    #MOONBOARD_LEDS = init_moonboard(LED_DRIVER,PIXELS_DRIVER)
    print("Test MOONBOARD LEDS\n===========")
    print(test_leds.__doc__)

    x = 0
    LL=51
    while(True):
        for  p in range(LL):
            if p > x-10 and p < x:
                PIXELS.set(p, colors.hue2rgb((x * 8) % 256))
            else:
                PIXELS.set(p, colors.Black)

        PIXELS.update()
        #time.sleep(0.1)
        x=(x+1)%LL
