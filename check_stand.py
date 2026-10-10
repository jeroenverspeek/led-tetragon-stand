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
# ports at the top: where it is, is in the Params (see PANEL.md). The Pi is 85 mm long; behind
# the LED board its board lies 22 mm and the hat's 33 mm (measured); about 3 mm of solder
# stands under the Pi and about 9 mm of parts on the hat (guess).
PI_LENGTH = 85
HAT_FRONT = 33 - 1.6 - 12  # behind the frame, which is 12 mm behind the LED board
# The panel: the LEDs on their board, and behind it the frame, five bars of the full depth: four
# round the edge and one up the middle. Their widths and the holes in them are in the Params.
LED_BOARD = 2
# What stands out from the back of the panel near the holder, seen from the back: u from the
# left, v from the top, both from the edges; x behind the back of the frame. See PANEL.md.
# The power connector, 18 x 8 round its middle 39 mm from the left and 80 mm from the top, with
# its plug in reaches 20 mm behind the LED board; its cable leaves it on the top side, so it
# bends up under the plate of the speaker holder.
POWER_PLUG = ((30, 48), (76, 84), 20 - 12)
# HUB75 IN, 26 x 10, 30 mm from the left and 39 mm from the bottom to its middle; the header stays
# within the frame, the plug on it sticks out further than the power plug (guess: 12 mm and 2 mm
# round the header). Its ribbon leaves the plug upwards and bends over the micro:bit holder to the
# hat, so it needs room between the two.
HUB75_HEADER = ((30, 56), (192 - 39 - 5, 192 - 39 + 5))
HUB75_IN_PLUG = ((28, 58), (HUB75_HEADER[1][0] - 2, HUB75_HEADER[1][1] + 2), 12)
RIBBON_ROOM = 4  # mm at least between the micro:bit holder and the top of that plug
# The micro:bit's USB plug with its sleeve, straight: 40 mm long (measured), about 11 x 8 (guess),
# in the middle of its USB edge, towards the Pi
MICROBIT_PLUG = (40, 11, 8)
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


def back(us, vs, xs):
    """A box on the back of the panel: u from the left and v from the top as seen from the back,
    x behind the back of the frame."""
    return Part.makeBox(xs[1] - xs[0], vs[1] - vs[0], us[1] - us[0],
                        V(DEPTH + xs[0], SIZE - vs[1], SIZE / 2 - us[1]))


def hole(u, v):
    """An M3 hole in a bar of the frame."""
    return Part.makeCylinder(1.5, DEPTH - LED_BOARD, V(LED_BOARD, SIZE - v, SIZE / 2 - u), V(1, 0, 0))


FRAME = DEPTH - LED_BOARD
bw, mw = p["frame_bar_width"], p["middle_bar_width"]
frame = back((0, bw), (0, SIZE), (-FRAME, 0))
for bar in (back((SIZE - bw, SIZE), (0, SIZE), (-FRAME, 0)), back((0, SIZE), (0, bw), (-FRAME, 0)),
            back((0, SIZE), (SIZE - bw, SIZE), (-FRAME, 0)),
            back(((SIZE - mw) / 2, (SIZE + mw) / 2), (0, SIZE), (-FRAME, 0))):
    frame = frame.fuse(bar)
# 4 holes up the middle bar, evenly spaced; at the left and right 2 in the corners and 1 in the middle
holes = [(SIZE / 2, p["bar_hole_top"] + i * (SIZE - 2 * p["bar_hole_top"]) / 3) for i in range(4)]
for u, v in ((p["side_hole_left"], p["side_hole_top"]), (p["side_mid_hole_left"], p["side_mid_hole_top"]),
             (p["side_hole_left"], SIZE - p["side_hole_top"])):
    holes += [(u, v), (SIZE - u, v)]
for u, v in holes:
    frame = frame.cut(hole(u, v))
panel = Part.makeBox(LED_BOARD, SIZE, SIZE, V(0, 0, -SIZE / 2)).fuse(frame).removeSplitter()
power_plug = back(*POWER_PLUG[:2], (-FRAME, POWER_PLUG[2]))
hub75_plug = back(*HUB75_IN_PLUG[:2], (-FRAME, HUB75_IN_PLUG[2]))

pi_us = (p["pi_from_left"], SIZE - p["pi_from_right"])
pi = Part.makeCompound([
    back(pi_us, (p["pi_from_top"], p["pi_from_top"] + PI_LENGTH), (p["pi_gap"], p["pi_depth"])),  # Pi and hat
    back(pi_us, (p["pi_from_top"] + PI_LENGTH, SIZE - p["hat_from_bottom"]), (HAT_FRONT, p["pi_depth"]))])  # hat
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
for name, plug in (("power plug", power_plug), ("HUB75 IN plug", hub75_plug)):
    check("panel: the back wall stays clear of the %s" % name, plug.distToShape(cradle)[0] >= 1,
          "%.1f mm" % plug.distToShape(cradle)[0])

# The holder on the back of the panel, with the speaker and the micro:bit in it
sl, st, sh = p["speaker_left"], p["speaker_top"], p["speaker_height"]
speaker_x = (p["holder_plate"], p["holder_plate"] + p["speaker_depth"])
speaker = back((sl + sh / 2, sl + p["speaker_length"] - sh / 2), (st, st + sh), speaker_x)
for u in (sl + sh / 2, sl + p["speaker_length"] - sh / 2):
    speaker = speaker.fuse(Part.makeCylinder(sh / 2, p["speaker_depth"], V(DEPTH + speaker_x[0], SIZE - st - sh / 2,
                                                                           SIZE / 2 - u), V(1, 0, 0)))
speaker = speaker.removeSplitter()
mf = p["microbit_fit"] / 2
microbit = back((p["microbit_left"] + mf, p["microbit_left"] + mf + p["microbit_height"]),
                (p["microbit_top"] + mf, p["microbit_top"] + mf + p["microbit_width"]),
                (p["holder_plate"] + mf, p["holder_plate"] + mf + p["microbit_thickness"]))
fitted = (holder, speaker, microbit)
masses_on_back = [holder.Volume * PLA, SPEAKER_MASS, MICROBIT_MASS]
check("holder: the speaker fits its cup, under the lips", overlap(holder, speaker) < TOUCH,
      "%.3f mm3" % overlap(holder, speaker))
check("holder: the micro:bit fits its pocket", overlap(holder, microbit) < TOUCH)
box = holder.optimalBoundingBox()
check("holder: within the edges of the panel, so it is not seen from the front",
      box.ZMax <= SIZE / 2 + 1e-6 and box.YMax <= SIZE + 1e-6)
check("holder: clear of the Pi and its hat", holder.distToShape(pi)[0] >= 1 - 1e-6, "%.1f mm" % holder.distToShape(pi)[0])
check("holder: the speaker clear of the Pi, even modelled with straight sides", speaker.distToShape(pi)[0] >= 0.5,
      "%.1f mm" % speaker.distToShape(pi)[0])
cable_u = sl + p["speaker_cable_at"]
sleeve = back((cable_u - p["cable_slot"] / 2, cable_u + p["cable_slot"] / 2),
              (st + sh, st + sh + p["speaker_cable_room"]), speaker_x)
check("holder: %g mm free below the speaker for its cable" % p["speaker_cable_room"],
      all(overlap(sleeve, a) < TOUCH for a in (holder, panel, power_plug)),
      "%.1f mm above the power plug" % sleeve.distToShape(power_plug)[0])
plug_v = p["microbit_top"] + mf + p["microbit_width"] / 2
plug_x = p["holder_plate"] + mf + p["microbit_thickness"] / 2
plug_u = p["microbit_left"] + mf + p["microbit_height"]
microbit_plug = back((plug_u, plug_u + MICROBIT_PLUG[0]), (plug_v - MICROBIT_PLUG[1] / 2, plug_v + MICROBIT_PLUG[1] / 2),
                     (plug_x - MICROBIT_PLUG[2] / 2, plug_x + MICROBIT_PLUG[2] / 2))
check("holder: the micro:bit's USB plug goes out through its slot", overlap(microbit_plug, holder) < TOUCH)
reach = plug_u + MICROBIT_PLUG[0] - p["pi_from_left"]
print("     the micro:bit's USB plug, straight, %s" % ("reaches %.1f mm under the edge of the Pi; an angled plug "
                                                     "stays clear" % reach if reach > 0 else
                                                     "stays %.1f mm clear of the Pi" % -reach), flush=True)
check("holder: stays out of the frame, so the power cable can run up under it", box.XMin >= DEPTH - 1e-6)
for name, plug in (("power plug", power_plug), ("HUB75 IN plug", hub75_plug)):
    gap = min(a.distToShape(plug)[0] for a in fitted)
    check("holder: clear of the %s" % name, gap >= 1, "%.1f mm" % gap)
room = HUB75_IN_PLUG[1][0] - (SIZE - box.YMin)
check("holder: room for the HUB75 ribbon to bend up over it", room >= RIBBON_ROOM, "%.1f mm" % room)
above_power = holder.common(back(POWER_PLUG[0], (0, POWER_PLUG[1][0]), (-FRAME, 60)))
room = POWER_PLUG[1][0] - (SIZE - above_power.optimalBoundingBox().YMin)
check("holder: room for the power cable to bend up under it", room >= 8, "%.1f mm" % room)
check("holder: on the back of the frame, not in a bar", overlap(holder, panel) < TOUCH)
microbit_part = holder.common(back((0, SIZE / 2), (p["microbit_top"] - 5, SIZE), (-FRAME, 60)))
print("     the speaker sticks out %.0f mm behind the frame, the micro:bit %.0f mm, the Pi %.0f mm"
      % (max(box.XMax, speaker.optimalBoundingBox().XMax) - DEPTH,
         microbit_part.optimalBoundingBox().XMax - DEPTH, pi.optimalBoundingBox().XMax - DEPTH), flush=True)

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
              (base.Volume * PLA, centre(base))] + [(m, centre(a)) for m, a in zip(masses_on_back, on)]
    total = sum(m for m, _ in masses)
    x = sum(m * at.x for m, at in masses) / total
    check("%d degrees: the stand does not tip over" % angle,
          -p["base_front"] + TIP_MARGIN <= x <= p["base_back"] - TIP_MARGIN,
          "centre of mass %.0f mm %s the hinge, base from %g to %g" % (abs(x), "behind" if x >= 0 else "in front of",
                                                                       -p["base_front"], p["base_back"]))
# Upright, the panel with its Pi must still lean back, or it would fall forward out of the cradle
upright = ([(PANEL_MASS, centre(panel)), (PI_MASS, centre(pi))]
           + [(m, centre(a)) for m, a in zip(masses_on_back, fitted)])
lean = sum(m * at.x for m, at in upright) / sum(m for m, _ in upright)
check("upright, the panel still leans on the back wall", lean > 0, "centre of mass %.1f mm behind its front" % lean)

# Print bed
cradle_lying = cradle.copy()
cradle_lying.rotate(V(), V(1, 0, 0), 90)  # on its floor
holder_lying = holder.copy()
holder_lying.rotate(V(), V(0, 1, 0), -90)  # on its plate
for name, shape in (("cradle", cradle_lying), ("base", base), ("holder", holder_lying)):
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
preview.addObject("Part::Feature", "PowerPlug").Shape = placed(power_plug, spot)
preview.addObject("Part::Feature", "Hub75Plug").Shape = placed(hub75_plug, spot)
preview.addObject("Part::Feature", "MicrobitPlug").Shape = placed(microbit_plug, spot)
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
