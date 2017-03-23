from PIL import Image, ImageDraw ,ImageColor
from  PIL.ImageColor import colormap as colormap
import string


def image_path(hold_set):
    #return path of image of the specified holsets
    img_path=["static/img/A+B+O.png","static/img/A+B.png",
              "static/img/A+O.png","static/img/A.png",
              "static/img/B+O.png","static/img/B.png",
              "static/img/O.png"]
    hold_sets=[{"Hold Set A 2016","Hold Set B 2016","Original School Holds 2016"},{"Hold Set A 2016", "Hold Set B 2016"},
               {"Hold Set A 2016", "Original School Holds 2016"},{"Hold Set A 2016"},
               {"Hold Set B 2016", "Original School Holds 2016"},{"Hold Set B 2016"},
               {"Original School Holds 2016"}]
    return img_path[hold_sets.index(hold_set)]


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
    image = Image.open(image_path(set(problem['hold_sets'])))
    colors = {
        'SH':colormap["blue"],
        'IH':colormap["blueviolet"],
        'FH':colormap["red"]
    }

    for hold_type in ['SH','IH', 'FH']:
        color = colors[hold_type]
        for h in problem.get('holds', {}).get(hold_type, {}):
            print(h)
            emphHold(image,h[0],int(h[1:]),color)
    image.save(path,'png')

if __name__=="__main__":
    problem = {"name": "Herm",
               "hold_sets": ["Hold Set A 2016", "Hold Set B 2016"],
               "grade_val": "g",
               "class": ["Problems", "17653+17671", "7a", "2stars", "Andrew", "Scott", ""],
               "grade": "7a", "author": "Andrew Scott",
               "holds": {"SH": ["F5", "G4"], "FH": ["E18"], "IH": ["B8", "E11", "B13", "G13"]}
               }

image = Image.open(image_path({"Hold Set A 2016"}))

draw = ImageDraw.Draw(image)
W,H = image.size
for k,x in X.items():
    draw.line((x, 0,x,H), fill=colormap["red"])
for k,y in Y.items():
    draw.line((0,y,W,y), fill=colormap["red"])
emphHold(image,"F",12,colormap["black"] )

image.save("test_image.png","PNG")

draw_Problem(problem,'test_problem.png')