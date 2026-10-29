# Check of the stand for the 128 x 128 LED panel
# by Jeroen Verspeek
#
# Opens stand128.FCStd, puts the panel in the channel and checks that it fits,
# that the stand does not tip over, that the halves for the Ender fit together
# and that the stand fits the X2D and the halves the Ender.
#
# Run:  freecadcmd check_stand128.py   (or ./build.sh 128)
# Writes stand128_preview.FCStd (for looking at, not for printing).
###########################

import math
import os
import sys

import FreeCAD as App
import Part

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stand_lib import (PLA, TOUCH, bed_fit, centre, check, overlap, placed, preview_leds, read_params,  # noqa: E402
                       summary)

V = App.Vector
# usable print beds in mm: the Bambu Lab X2D with one nozzle, the Ender 3 v2 (see PRINTING.md)
X2D_BED = (256, 256)
ENDER_BED = (220, 200)
# Guesses, only used for the balance: the panel, and what may be fixed to its back (a Pi with its
# hat, a speaker), in the middle of the back, 20 mm behind it
PANEL_MASS = 700  # g; a 128 x 64 P1.875 module is listed at about 350 g
BACK_MASS = 250  # g
TIP_MARGIN = 15  # mm, the centre of mass stays at least this far inside the base
PREVIEW_TEXT = ("Hello", "world")  # each dot of the font 4 x 4 LEDs
LEDS = 128  # LEDs along an edge of the panel

doc = App.openDocument(os.path.join(HERE, "stand128.FCStd"))
doc.recompute()
p = read_params(doc)
SIZE, DEPTH, FIT = p["panel_size"], p["panel_depth"], p["panel_fit"]
TILT = math.radians(p["tilt"])
XBO = DEPTH + FIT + p["back_thickness"]
H = p["base_thickness"] + XBO * math.sin(TILT) + p["floor_thickness"] * math.cos(TILT)
BT = p["base_thickness"]

stand = doc.getObject("Stand").Shape
left, right = doc.getObject("LeftHalf").Shape, doc.getObject("RightHalf").Shape
letters = doc.getObjectsByLabel("Text")[0].Shape
# from the panel's frame (x backwards from its front, y up from its bottom edge, z across) to the
# stand's (x backwards from the bottom edge of the front of the panel, y up from the table)
spot = App.Placement(V(0, H, 0), App.Rotation(V(0, 0, 1), -p["tilt"]))
panel = placed(Part.makeBox(DEPTH, SIZE, SIZE, V(0, 0, -SIZE / 2)), spot)
back_mass = placed(Part.makeSphere(1, V(DEPTH + 20, SIZE / 2, 0)), spot)

check("stand: one valid solid", stand.isValid() and len(stand.Solids) == 1)
check("panel: stands in the channel without overlap", overlap(panel, stand) < TOUCH, "%.3f mm3" % overlap(panel, stand))
check("panel: rests on the floor of the channel and against its lip", panel.distToShape(stand)[0] < TOUCH)
front_top = spot.multVec(V(0, SIZE, 0))  # the top edge of the front of the panel
lean = math.degrees(math.atan2(front_top.x, front_top.y - H))
check("panel: leans back %g degrees, %g to the table" % (p["tilt"], 90 - p["tilt"]), abs(lean - p["tilt"]) < 0.01,
      "%.2f degrees" % lean)
low = stand.optimalBoundingBox().YMin
check("stand: flat on the table, nothing below it", abs(low) < 1e-6, "%.3f mm" % low)
# the channel above the plate, in the middle, where the letters are in front of it
channel = stand.common(Part.makeBox(1000, 1000, 2, V(-500, BT + 0.01, -1))).BoundBox
text_back = letters.BoundBox.XMax
check("stand: the letters stay in view in front of the channel", channel.XMin >= text_back + 2,
      "%.1f mm in front" % (channel.XMin - text_back))
check("stand: the back wall leans back no more than 45 degrees, so it prints without support", p["tilt"] <= 45)

masses = [(PANEL_MASS, centre(panel)), (BACK_MASS, centre(back_mass)), (stand.Volume * PLA, centre(stand))]
x = sum(m * at.x for m, at in masses) / sum(m for m, _ in masses)
check("stand: does not tip over", -p["base_front"] + TIP_MARGIN <= x <= p["base_back"] - TIP_MARGIN,
      "centre of mass %.0f mm behind the panel's bottom edge, base from %g to %g" % (x, -p["base_front"],
                                                                                  p["base_back"]))
# The panel pushed at its top edge, backwards: how hard before the stand tips over its back edge
top = spot.multVec(V(DEPTH, SIZE, 0))
weight = sum(m for m, _ in masses)
push = weight * (p["base_back"] - x) / top.y
print("     a push of about %.0f g backwards at the top edge of the panel tips it over" % push, flush=True)

# The halves for the Ender
check("halves: each one valid solid", all(h.isValid() and len(h.Solids) == 1 for h in (left, right)))
check("halves: fit together without overlap", overlap(left, right) < TOUCH, "%.3f mm3" % overlap(left, right))
gap = left.distToShape(right)[0]
check("halves: %g mm all round the joint for the glue" % p["joint_fit"], abs(gap - p["joint_fit"]) < 1e-3,
      "%.2f mm" % gap)
lost = stand.Volume - left.Volume - right.Volume
check("halves: together the whole stand, but for the joint", 0 < lost < 1000, "%.0f mm3 in the joint" % lost)
joint = right.BoundBox.ZMin - p["joint_fit"]
clear = min(min(abs(f.BoundBox.ZMin - joint), abs(f.BoundBox.ZMax - joint)) for f in letters.Faces)
check("halves: the joint goes between the words, clear of the letters",
      all(f.BoundBox.ZMax < joint or f.BoundBox.ZMin > joint for f in letters.Faces) and clear >= 0.5,
      "%.1f mm %s of the middle, %.1f mm from a letter" % (abs(joint), "right" if joint >= 0 else "left", clear))
tails = left.common(Part.makeBox(1000, 1000, 1000, V(-500, -1, joint + 0.01)))
check("halves: the dovetails lie in the plate only, so the halves slide together from above",
      tails.Volume > 0 and tails.BoundBox.YMax <= BT + 1e-6, "%d dovetails" % len(tails.Solids))

# Print beds: lying on the plate
for name, shape, bed, printer in (("stand", stand, X2D_BED, "the X2D"), ("left half", left, ENDER_BED, "the Ender"),
                                  ("right half", right, ENDER_BED, "the Ender")):
    lying = shape.copy()
    lying.rotate(V(), V(1, 0, 0), 90)
    box = lying.optimalBoundingBox()
    fit = bed_fit(box, bed)
    check("print: %s fits %s" % (name, printer), bool(fit), "%.1f x %.1f mm, %s" % (box.XLength, box.YLength, fit))

leds, (width, height) = preview_leds(PREVIEW_TEXT, SIZE, LEDS, 4)
check("preview: the text fits the panel", height <= LEDS and width <= LEDS, "%d x %d LEDs" % (width, height))

preview = App.newDocument("stand128_preview")
preview.addObject("Part::Feature", "Stand").Shape = stand
preview.addObject("Part::Feature", "Panel").Shape = panel
preview.addObject("Part::Feature", "LEDs").Shape = placed(Part.makeCompound(leds), spot)
preview.recompute()
preview.saveAs(os.path.join(HERE, "stand128_preview.FCStd"))

summary()
