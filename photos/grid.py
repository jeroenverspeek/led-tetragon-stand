# Measuring grid for a flattened photo
# by Jeroen Verspeek
#
# Cuts a region out of a photo that has been flattened to a known square
# (such as panel_back_flat.jpg: the back of the panel, 192 x 192 mm, made
# with the Genius Scan app), enlarges it and draws a grid over it: a line
# every millimetre, a thicker one with its number every 5 mm. Positions are
# measured from the left and the top edge of the photo, as seen in it.
#
# Run:  python3 grid.py photo.jpg out.png left right top bottom [size]
#       left, right, top, bottom: the region in mm; size: the edge of the
#       square the photo shows, in mm (default 192)
# Example, the power connector:  python3 grid.py panel_back_flat.jpg power.png 36 64 72 92
###########################

import sys

from PIL import Image, ImageDraw

ENLARGE = 4

if len(sys.argv) not in (7, 8):
    sys.exit("usage: python3 grid.py photo.jpg out.png left right top bottom [size]")
source, out = sys.argv[1], sys.argv[2]
left, right, top, bottom = map(float, sys.argv[3:7])
size = float(sys.argv[7]) if len(sys.argv) == 8 else 192.0

photo = Image.open(source).convert("RGB")
if abs(photo.size[0] / photo.size[1] - 1) > 0.01:
    print("note: the photo is %d x %d pixels, not square; measuring each way on its own scale" % photo.size)
per_mm_x, per_mm_y = photo.size[0] / size, photo.size[1] / size
region = photo.crop((round(left * per_mm_x), round(top * per_mm_y), round(right * per_mm_x), round(bottom * per_mm_y)))
region = region.resize((region.size[0] * ENLARGE, region.size[1] * ENLARGE), Image.LANCZOS)
draw = ImageDraw.Draw(region)
for mm in range(int(left), int(right) + 1):
    x = (mm - left) * per_mm_x * ENLARGE
    fifth = mm % 5 == 0
    draw.line([(x, 0), (x, region.size[1])], fill=(0, 255, 255) if fifth else (0, 120, 120), width=2 if fifth else 1)
    if fifth:
        draw.text((x + 3, 3), str(mm), fill=(255, 255, 0))
for mm in range(int(top), int(bottom) + 1):
    y = (mm - top) * per_mm_y * ENLARGE
    fifth = mm % 5 == 0
    draw.line([(0, y), (region.size[0], y)], fill=(255, 0, 255) if fifth else (120, 0, 120), width=2 if fifth else 1)
    if fifth:
        draw.text((3, y + 3), str(mm), fill=(255, 255, 0))
region.save(out)
print("%s: %d x %d pixels, %.1f pixels per mm" % (out, region.size[0], region.size[1], per_mm_x * ENLARGE))
