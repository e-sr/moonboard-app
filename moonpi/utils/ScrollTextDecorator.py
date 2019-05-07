from BiblioPixelAnimations.matrix.Text import ScrollText
from bibliopixel.colors import COLORS
from bibliopixel.layout import font


class ScrollTextDecorator(ScrollText):
    COLOR_DEFAULTS = (('bgcolor', COLORS.Off), ('color', COLORS.Blue))

    def __init__(self, layout, text='ScrollText', xPos=0, yPos=0,
                 font_name=font.default_font, font_scale=1, **kwds):
        super().__init__(layout, text, xPos, yPos, font_name, font_scale, **kwds)
