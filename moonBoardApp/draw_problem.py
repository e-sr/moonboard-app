from __future__ import division
from __future__ import absolute_import
from builtins import str
from builtins import range
from past.utils import old_div
from PIL import Image, ImageDraw
from PIL.ImageColor import colormap
from .moonboard_problems import HOLDS_CONF

# Coordinates: x:horizontal,y vertical. (x,y)=(0,0) upper -left
# coordinate of the first and last(A,K) hold column (in pixels )
XMIN, XMAX = 61, 389
# coordinate of the first and last(18,1) hold row (in pixels)
YMIN, YMAX = 56, 612
# image size
W, H = None, None
# xy hold spacing
DX = (XMAX - XMIN) / 10.0
DY = (YMAX - YMIN) / 17.

# XY columns/rows  holds names
X_GRID_NAMES = HOLDS_CONF['grid_name']['horizontal']
Y_GRID_NAMES = HOLDS_CONF['grid_name']['vertical']

# holds row/columns coordinates (in pixels)
X = {xk: int(XMIN + X_GRID_NAMES.index(xk) * DX) for xk in X_GRID_NAMES}
Y = {yk: int(YMIN + (18 - yk) * DY) for yk in Y_GRID_NAMES}


def background_image_path(image_folder_path, hold_setup_key):
    # return path of image of the specified holsets
    hold_setup = sorted(list(HOLDS_CONF['setup'][hold_setup_key]))
    name = "-".join([HOLDS_CONF["configurations"][s]['shortName'].replace(" ", "_") for s in hold_setup])
    return str(image_folder_path.joinpath(name + ".png"))


def emphHold(img, xc, yc, color=colormap['black'], width=4):
    """draw rectagle around hold position"""
    x, y = X[xc], Y[yc]
    draw = ImageDraw.Draw(img)
    for i in range(width):
        draw.rectangle([x - old_div(DX, 2) + i, y - old_div(DY, 2) + i, x + old_div(DX, 2) - i, y + old_div(DY, 2) - i], outline=color)
    return img


def draw_Problem(problem, background_img_path, out_path, hold_colors={}):
    """draw problen and save image """
    bg_image = Image.open(background_img_path)

    colors = {k: hold_colors.get(k, (255, 0, 0)) for k in ['SH', 'IH', 'FH']}

    for hold_type in ['SH', 'IH', 'FH']:
        color = colors[hold_type]
        for h in problem.get('holds', {}).get(hold_type, {}):
            emphHold(bg_image, h[0], int(h[1:]), color)
    bg_image.save(str(out_path), 'png')


if __name__ == "__main__":
    """
    draw grid on image for testing coordinates
    """
    from pathlib import Path

    image = Image.open(background_image_path(Path("static/img"), 1))

    draw = ImageDraw.Draw(image)
    W, H = image.size
    for k, x in list(X.items()):
        draw.line((x, 0, x, H), fill=colormap["red"])
    for k, y in list(Y.items()):
        draw.line((0, y, W, y), fill=colormap["red"])
    for c in range(1, 19):
        emphHold(image, "F", c, colormap["black"])
    for r in X_GRID_NAMES:
        emphHold(image, r, 10, colormap["red"])

    image.save("test_image.png", "PNG")
