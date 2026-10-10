# Check of the stand for the LED tetragon
# by Jeroen Verspeek
#
# Opens stand.FCStd, puts the panel in the cradle and the cradle on the base at
# a few angles, and checks that nothing overlaps, that the parts touch where
# they should, that the stand does not tip over and that every part fits the
# print bed.
#
# Run:  freecadcmd check_stand.py   (or ./build.sh)
# Writes stand_preview.FCStd (for looking at, not for printing).
###########################

import math
import os

import FreeCAD as App
import Part

HERE = os.path.dirname(os.path.abspath(__file__))
V = App.Vector
BED = (220, 200)  # usable print bed in mm
TOUCH = 1e-6

ANGLES = (60, 75, 90)  # panel to the table, in degrees, from leaning far back to upright
PREVIEW_ANGLE = 75
# Guesses, only used for the balance and the preview
PANEL_MASS = 400  # g, panel with its factory frame
PI_MASS = 120  # g, Pi with hat, distance holders and cables
# The Pi with its hat on the back of the frame, in portrait, on the vertical middle bar, its USB
# ports at the top. Seen from the back it reaches from 90 mm off the left edge to 40 mm off the
# right edge (measured); seen from the front that is from 6 mm right of the middle to 40 mm off
# the left edge. Up the panel the Pi reaches to 40 mm under the top and the hat sticks out below
# it to 39 mm above the bottom (measured). The Pi is 85 mm long. Behind the LED board the Pi's
# board lies 22 mm and the hat's 33 mm (measured); about 3 mm of solder stands under the Pi and
# about 9 mm of parts on the hat (guess). The frame behind the LED board is 12 mm.
PI_ACROSS = (-96 + 40, 96 - 90)  # z, from the middle; the panel is 192 mm
PI_TOP = 192 - 40
PI_BOTTOM = PI_TOP - 85
HAT_BOTTOM = 39
PI_BACK = 33 + 9  # behind the LED board
PI_FRONT = 22 - 3
HAT_FRONT = 33 - 1.6
# The panel's power connector, seen from the back 39 mm off the left edge and 80 mm under the top
# (measured); it sticks out, so the holder must stay well above it
POWER_AT = (96 - 39, 192 - 80)  # z, y
SPEAKER_MASS = 74  # g
MICROBIT_MASS = 10  # g, with the end of its cable
PLA = 1.24 / 1000  # g/mm3; a printed part weighs less, so the stand is lighter than this
TIP_MARGIN = 15  # mm, the centre of mass stays at least this far inside the base
# Shown on the panel in the preview, in a 5 x 7 font, each dot of it 2 x 2 LEDs
PREVIEW_TEXT = ("Hello", "world")
FONT = {
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "w": ("00000", "00000", "10001", "10001", "10101", "10101", "01010"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
}
LEDS = 64  # LEDs along an edge of the panel

doc = App.openDocument(os.path.join(HERE, "stand.FCStd"))
doc.recompute()
params = doc.getObject("Params")
p = {}  # every parameter by its alias, in mm
row = 1
while params.getContents("A%d" % row):
    alias = params.getContents("A%d" % row).lstrip("'")
    p[alias] = getattr(params, alias).Value
    row += 1
SIZE, DEPTH, FIT = p["panel_size"], p["panel_depth"], p["panel_fit"]
HW = SIZE / 2 + FIT
XBO = DEPTH + FIT + p["back_thickness"]
PIVOT = V(XBO - p["hinge_radius"], p["hinge_radius"] - p["floor_thickness"], 0)  # in the cradle
OUT = HW + p["ear_thickness"]
CI = OUT + p["ring_height"]
PH = p["base_thickness"] + p["base_gap"] + p["hinge_radius"]  # height of the hinge axis above the table

cradle = doc.getObject("Cradle").Shape
base = doc.getObject("Base").Shape
holder = doc.getObject("Holder").Shape

failures = []


def check(name, ok, detail=""):
    print("%-4s %s %s" % ("ok" if ok else "FAIL", name, detail), flush=True)
    if not ok:
        failures.append(name)


def placed(shape, placement):
    copy = shape.copy()
    copy.Placement = placement.multiply(copy.Placement)
    return copy


def centre(shape):
    """Centre of mass of a solid or of a compound of solids."""
    solids = shape.Solids
    return sum((solid.CenterOfMass * solid.Volume for solid in solids), V()) / sum(solid.Volume for solid in solids)


def overlap(a, b):
    return a.common(b).Volume if a.BoundBox.intersect(b.BoundBox) else 0.0


def bed_fit(box):
    """How the part fits the bed lying as modelled: 'straight', 'turned N degrees' or ''."""
    for degrees in range(0, 91):
        turn = math.radians(degrees)
        if (box.XLength * math.cos(turn) + box.YLength * math.sin(turn) <= BED[0]
                and box.XLength * math.sin(turn) + box.YLength * math.cos(turn) <= BED[1]):
            return "straight" if degrees == 0 else "turned %d degrees" % degrees
    return ""


def on_base(angle):
    """Where the cradle (in the panel's frame: x backwards from the front of the panel, y up from
    its bottom edge, z across) goes on the base (x backwards from the hinge, y across, z up)
    with the panel at `angle` degrees to the table."""
    return (App.Placement(V(0, 0, PH), App.Rotation(V(0, 1, 0), 90 - angle))
            .multiply(App.Placement(V(), App.Rotation(V(1, 0, 0), 90)))
            .multiply(App.Placement(-PIVOT, App.Rotation())))


panel = Part.makeBox(DEPTH, SIZE, SIZE, V(0, 0, -SIZE / 2))
led_board = DEPTH - 12  # back of the LED board
pi = Part.makeCompound([
    Part.makeBox(PI_BACK - PI_FRONT, PI_TOP - PI_BOTTOM, PI_ACROSS[1] - PI_ACROSS[0],
                 V(led_board + PI_FRONT, PI_BOTTOM, PI_ACROSS[0])),  # the Pi with the hat on it
    Part.makeBox(PI_BACK - HAT_FRONT, PI_BOTTOM - HAT_BOTTOM, PI_ACROSS[1] - PI_ACROSS[0],
                 V(led_board + HAT_FRONT, HAT_BOTTOM, PI_ACROSS[0]))])  # the hat below the Pi
# A countersunk screw, along z from the top of its head: a 90 degree head on a plain shank
screw = Part.makeCone(p["screw_head_d"] / 2, p["bolt_d"] / 2 - 0.2, (p["screw_head_d"] - p["bolt_d"] + 0.4) / 2).fuse(
    Part.makeCylinder(p["bolt_d"] / 2 - 0.2, p["bolt_length"])).removeSplitter()
# How far a head sinks below the surface of the cheek
head_sink = (p["countersink_d"] - p["screw_head_d"]) / 2
CO = CI + p["cheek_thickness"]  # outside of a cheek
screws = [placed(screw, App.Placement(V(0, CO - head_sink, PH), App.Rotation(V(1, 0, 0), 90))),
          placed(screw, App.Placement(V(0, -CO + head_sink, PH), App.Rotation(V(1, 0, 0), -90)))]

# The panel in the cradle
check("panel: stands in the cradle without overlap", overlap(panel, cradle) < TOUCH,
      "%.3f mm3" % overlap(panel, cradle))
check("panel: rests on the floor of the cradle and against its lip", panel.distToShape(cradle)[0] < TOUCH)
check("panel: the back wall stays clear of the Pi and its hat", pi.distToShape(cradle)[0] >= 2,
      "%.1f mm" % pi.distToShape(cradle)[0])

# The holder on the back of the panel, and the speaker and micro:bit in it
li = p["speaker_length"] + 2 * p["speaker_fit"]
hi = p["speaker_height"] + 2 * p["speaker_fit"]
lo, ho = li + 2 * p["holder_wall"], hi + 2 * p["holder_wall"]
xp = DEPTH + p["holder_plate"]
xf = xp + p["microbit_thickness"] + p["microbit_fit"] + p["holder_wall"]  # floor of the cup
yc = SIZE - ho / 2
speaker = Part.makeBox(p["speaker_depth"], p["speaker_height"], p["speaker_length"] - p["speaker_height"],
                       V(xf, yc - p["speaker_height"] / 2, SIZE / 2 - lo / 2 - (li - hi) / 2))
for z in (SIZE / 2 - lo / 2 - (li - hi) / 2, SIZE / 2 - lo / 2 + (li - hi) / 2):
    speaker = speaker.fuse(Part.makeCylinder(p["speaker_height"] / 2, p["speaker_depth"], V(xf, yc, z), V(1, 0, 0)))
speaker = speaker.removeSplitter()
microbit = Part.makeBox(p["microbit_thickness"], p["microbit_height"], p["microbit_width"],
                        V(xp + p["microbit_fit"] / 2, yc - p["microbit_height"] / 2, SIZE / 2 - lo + p["holder_wall"]))
fitted = (holder, speaker, microbit)
check("holder: the speaker fits its cup, under the lips", overlap(holder, speaker) < TOUCH,
      "%.3f mm3" % overlap(holder, speaker))
check("holder: the micro:bit fits its pocket", overlap(holder, microbit) < TOUCH)
box = holder.optimalBoundingBox()
check("holder: within the edges of the panel, so it is not seen from the front",
      box.ZMax <= SIZE / 2 + 1e-6 and box.YMax <= SIZE + 1e-6 and box.XMin >= DEPTH - p["rib_depth"] - 1e-6)
check("holder: clear of the Pi and its hat", all(a.distToShape(pi)[0] >= 1 for a in fitted),
      "%.1f mm" % min(a.distToShape(pi)[0] for a in fitted))
check("holder: well above the power connector", box.YMin - POWER_AT[1] >= 20, "%.0f mm" % (box.YMin - POWER_AT[1]))
check("holder: the ribs lie beside the bar, not on it",
      overlap(holder, Part.makeBox(DEPTH, SIZE, p["bar_width"], V(0, 0, -p["bar_width"] / 2))) < TOUCH)
sticks_out = max(a.optimalBoundingBox().XMax for a in fitted) - DEPTH
print("     the holder with the speaker sticks out %.0f mm behind the frame, the Pi %.0f mm"
      % (sticks_out, pi.optimalBoundingBox().XMax - DEPTH), flush=True)

# The hinge
check("hinge: the ring is no wider than the round under the cradle, so it clears the base",
      p["ring_d"] / 2 <= p["hinge_radius"], "ring %g mm, round %g mm" % (p["ring_d"], 2 * p["hinge_radius"]))
ring_face = Part.makeCylinder(p["ring_d"] / 2 - 0.01, 0.5, PIVOT + V(0, 0, OUT - 0.5)).cut(
    Part.makeCylinder(p["bolt_d"] / 2 + 0.01, 0.5, PIVOT + V(0, 0, OUT - 0.5)))
check("hinge: the ring lies wholly on the ear", abs(cradle.common(ring_face).Volume - ring_face.Volume) < 1e-3)
check("hinge: wall left behind the nut", p["ear_thickness"] - p["nut_depth"] >= 2,
      "%.1f mm" % (p["ear_thickness"] - p["nut_depth"]))
# The screw runs from its head, sunk into the cheek, through the cheek and ear into the nut.
# Its end, measured from the inside of the ear outwards, must not reach the panel and must
# leave most of the nut in use.
check("hinge: the screw heads sink no deeper than flush", 0 <= head_sink <= 0.5, "%.1f mm deep" % head_sink)
check("hinge: cheek left under the countersink", p["cheek_thickness"] - (p["countersink_d"] - p["bolt_d"]) / 2 >= 1.5,
      "%.1f mm" % (p["cheek_thickness"] - (p["countersink_d"] - p["bolt_d"]) / 2))
bolt_end = p["cheek_thickness"] - head_sink + p["ring_height"] + p["ear_thickness"] - p["bolt_length"]
check("hinge: an M5 x %g screw does not reach the panel" % p["bolt_length"], bolt_end >= 0,
      "ends %.1f mm inside the ear" % bolt_end)
check("hinge: and goes through at least 3 mm of the nut", p["nut_depth"] - bolt_end >= 3,
      "%.1f mm" % (p["nut_depth"] - bolt_end))
for i, s in enumerate(screws):
    check("hinge: screw %d sits in its cheek without overlap" % (i + 1), overlap(s, base) < TOUCH)

# At each angle
text_back = -p["base_front"] + p["text_margin"] + p["text_size"]  # roughly the back of the letters
for angle in ANGLES:
    spot = on_base(angle)
    c, pn, pp = placed(cradle, spot), placed(panel, spot), placed(pi, spot)
    check("%d degrees: cradle clear of the base" % angle, overlap(c, base) < TOUCH, "%.3f mm3" % overlap(c, base))
    check("%d degrees: the rings touch the cheeks" % angle, c.distToShape(base)[0] < TOUCH)
    low = c.optimalBoundingBox().ZMin - p["base_thickness"]
    check("%d degrees: cradle above the plate" % angle, low >= p["base_gap"] - 1e-3, "%.2f mm" % low)
    check("%d degrees: panel and Pi clear of the base and screws" % angle,
          all(overlap(a, b) < TOUCH for a in (pn, pp) for b in [base] + screws))
    check("%d degrees: screws clear of the cradle" % angle, all(overlap(s, c) < TOUCH for s in screws))
    on = [placed(a, spot) for a in fitted]
    check("%d degrees: holder, speaker and micro:bit clear of the base" % angle,
          all(overlap(a, base) < TOUCH for a in on))
    front = c.optimalBoundingBox().XMin
    check("%d degrees: the letters on the base stay in view in front of the cradle" % angle, front >= text_back + 2,
          "%.1f mm in front" % (front - text_back))
    masses = [(PANEL_MASS, centre(pn)), (PI_MASS, centre(pp)), (c.Volume * PLA, centre(c)),
              (base.Volume * PLA, centre(base)), (on[0].Volume * PLA, centre(on[0])),
              (SPEAKER_MASS, centre(on[1])), (MICROBIT_MASS, centre(on[2]))]
    total = sum(m for m, _ in masses)
    x = sum(m * at.x for m, at in masses) / total
    check("%d degrees: the stand does not tip over" % angle,
          -p["base_front"] + TIP_MARGIN <= x <= p["base_back"] - TIP_MARGIN,
          "centre of mass %.0f mm %s the hinge, base from %g to %g" % (abs(x), "behind" if x >= 0 else "in front of",
                                                                       -p["base_front"], p["base_back"]))
# Upright, the panel with its Pi must still lean back, or it would fall forward out of the cradle
upright = [(PANEL_MASS, centre(panel)), (PI_MASS, centre(pi)), (SPEAKER_MASS, centre(speaker)),
           (MICROBIT_MASS, centre(microbit)), (holder.Volume * PLA, centre(holder))]
lean = sum(m * at.x for m, at in upright) / sum(m for m, _ in upright)
check("upright, the panel still leans on the back wall", lean > 0, "centre of mass %.1f mm behind its front" % lean)

# Print bed
cradle_lying = cradle.copy()
cradle_lying.rotate(V(), V(1, 0, 0), 90)  # on its floor
holder_standing = holder.copy()
holder_standing.rotate(V(), V(0, 1, 0), 90)  # on the rim of its cup
for name, shape in (("cradle", cradle_lying), ("base", base), ("holder", holder_standing)):
    box = shape.optimalBoundingBox()
    fit = bed_fit(box)
    check("print: %s fits the bed" % name, bool(fit), "%.1f x %.1f mm, %s" % (box.XLength, box.YLength, fit))

# The lit LEDs for the preview: PREVIEW_TEXT in the middle of the panel, in the panel's frame
pitch = SIZE / LEDS
# each line as 7 rows of font dots, one empty font column between the letters
lines = [[" ".join(FONT[ch][row] for ch in line) for row in range(7)] for line in PREVIEW_TEXT]
height = 2 * (7 * len(lines) + 2 * (len(lines) - 1))  # in LEDs, 2 empty font rows between the lines
width = 2 * max(len(rows[0]) for rows in lines)
check("preview: the text fits the panel", height <= LEDS and width <= LEDS, "%d x %d LEDs" % (width, height))
leds = []
for n, rows in enumerate(lines):
    for row, dots in enumerate(rows):
        for col, dot in enumerate(dots):
            for dy in range(2 if dot == "1" else 0):
                for dx in range(2):
                    left = (LEDS - 2 * len(dots)) // 2 + 2 * col + dx  # LEDs from the left
                    top = (LEDS - height) // 2 + 2 * (9 * n + row) + dy  # LEDs from the top
                    leds.append(Part.makeBox(0.4, 0.8 * pitch, 0.8 * pitch,
                                             V(-0.4, SIZE - (top + 0.9) * pitch, -SIZE / 2 + (left + 0.1) * pitch)))

# preview document
preview = App.newDocument("stand_preview")
spot = on_base(PREVIEW_ANGLE)
preview.addObject("Part::Feature", "Base").Shape = base
preview.addObject("Part::Feature", "Cradle").Shape = placed(cradle, spot)
preview.addObject("Part::Feature", "Panel").Shape = placed(panel, spot)
preview.addObject("Part::Feature", "Pi_outline").Shape = placed(pi, spot)
preview.addObject("Part::Feature", "LEDs").Shape = placed(Part.makeCompound(leds), spot)
preview.addObject("Part::Feature", "Holder").Shape = placed(holder, spot)
preview.addObject("Part::Feature", "Speaker").Shape = placed(speaker, spot)
preview.addObject("Part::Feature", "Microbit").Shape = placed(microbit, spot)
for i, s in enumerate(screws):
    preview.addObject("Part::Feature", "Screw%d" % (i + 1)).Shape = s
preview.recompute()
preview.saveAs(os.path.join(HERE, "stand_preview.FCStd"))

print("%d checks failed" % len(failures) if failures else "all checks passed", flush=True)
