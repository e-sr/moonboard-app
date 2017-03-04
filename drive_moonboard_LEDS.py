import sys
import os

LED_DRIVER = None
PIXELS_DRIVER = None


def _pixel_on(moonboard, row, column, color, brightness):
    pass

def _pixel_off(moonboard,row, column, color, brightness):
    pass

def init_moonboard(led_driver, pixel_driver):
    pass

def test_leds(moonboard,speed=0.2,color=None):
    """
    TEST moonboadr docsstring
    :param moonboard:
    :param speed:
    :param color:
    """
    pass

def show_problem(moonboard, holds, brightness= 100, color= None):
    """

    :param moonboard:
    :param holds:
    :param bightness:
    :param color:
    """
    pass

if __name__=="__main__":
    MOONBOARD_LEDS = init_moonboard(LED_DRIVER,PIXELS_DRIVER)
    print("Test MOONBOARD LEDS\n===========")
    print(test_leds.__doc__)
    test_leds(MOONBOARD_LEDS)

