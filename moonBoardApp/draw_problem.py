from PIL import Image, ImageDraw
from PIL.ImageColor import colormap
import string
from moonBoardApp import STATIC_FILE_PATH
from moonboard_problems import HOLDS_CONF

def image_path(hold_setup):
    #return path of image of the specified holsets
    hold_setup = sorted(list(hold_setup))
    name = "-".join([HOLDS_CONF["configurations"][s]['shortName'].replace(" ", "_") for s in hold_setup])
    return str(STATIC_FILE_PATH.joinpath("img").joinpath(name + ".png"))

# Coordinates: x:horizontal,y vertical. (x,y)=(0,0) upper -left
# coordinate of the first and last(A,K) hold column (in pixels )
XMIN, XMAX = 61, 389
# coordinate of the first and last(18,1) hold row (in pixels)
YMIN, YMAX = 56, 612
#image size
W,H = None,None
#XY columns/rows  holds names
X_GRID_NAMES = string.ascii_uppercase[0:11]
Y_GRID_NAMES = list(range(1, 19))
#xy hold spacing
DX = (XMAX - XMIN) / 10.0
DY = (YMAX - YMIN) / 17.
# holds row/columns coordinates (in pixels)
X = {xk:int(XMIN + X_GRID_NAMES.index(xk) * DX) for xk in X_GRID_NAMES}
Y = {yk:int(YMIN + (18-yk) * DY) for yk in Y_GRID_NAMES}

def emphHold(img, xc, yc, color=colormap['black'] , width=4):
    """draw rectagle around hold position"""
    x,y = X[xc],Y[yc]
    draw = ImageDraw.Draw(img)
    for i in range(width):
        draw.rectangle([x - DX / 2 + i, y - DY / 2 + i, x + DX / 2 - i, y + DY / 2 - i], outline=color)
    return img

def draw_Problem(problem, path):
    """draw problen and save image """
    img_path=image_path(set(problem['holds_setup']))
    image = Image.open(img_path)
    colors = {
        'SH':colormap["blue"],
        'IH':colormap["blueviolet"],
        'FH':colormap["red"]
    }

    for hold_type in ['SH','IH', 'FH']:
        color = colors[hold_type]
        for h in problem.get('holds', {}).get(hold_type, {}):
            emphHold(image,h[0],int(h[1:]),color)
    image.save(path,'png')

if __name__=="__main__":
    """
    draw grid on image for testing coordinates
    """
    image = Image.open(image_path({"Hold Set A 2016"}))

    draw = ImageDraw.Draw(image)
    W,H = image.size
    for k,x in X.items():
        draw.line((x, 0,x,H), fill=colormap["red"])
    for k,y in Y.items():
        draw.line((0,y,W,y), fill=colormap["red"])
    emphHold(image,"F",12,colormap["black"] )
    image.save("test_image.png","PNG")
