# Parts for the stand of the LED tetragon
# by Jeroen Verspeek
#
# The tetragon is a single LED panel (64 x 64, P3, 192 x 192 mm) on its factory
# frame. The Raspberry Pi with its hat is fixed to the vertical middle bar on
# the back of that frame, in portrait. The stand holds the panel leaning back
# at an angle that is set by hand and held by friction.
#
# Cradle: a channel over the full width that the bottom edge of the panel
# stands in: a floor, a low lip in front and a back wall that reaches a little
# way up the back of the frame, well below the Pi. Leaning back, the panel
# rests on the floor and against the back wall by its own weight. At both ends
# a side plate (ear) carries the hinge: a hole for the bolt, a pocket for its
# nut on the inside and a raised ring round the hole on the outside. The
# corner under the back wall is rounded round the hinge axis, so at any angle
# the cradle stays clear of the base. Prints lying on its floor.
#
# Base: a plate on the table with an upright cheek at both ends. A countersunk
# screw goes from outside through each cheek into the nut in the ear, its head
# sunk flush into the cheek. Tightening it presses the cheek against the ring
# on the ear, and that friction holds the angle. The name is sunk into the
# plate in front of the panel.
#
# Holder: the USB speaker and the micro:bit on the back of the panel, in the
# left half seen from the back, beside the Pi; one part on three screws: the
# top left corner hole, the top hole of the middle bar and the middle hole of
# the left bar. At the top a plate with a cup for the rounded back of the
# speaker, grille facing backwards, held by a lip along both long sides, with
# a slot in the bottom for its cable. The plate bridges the frame, so the
# power cable can run up under it. A strip down the left bar joins it to the
# pocket for the micro:bit, upright and parallel to the panel, between the
# power connector and HUB75 IN. The micro:bit slides in from the side edge of
# the panel; its USB plug, pointing to the Pi through a slot, holds it there.
# Prints lying on its plate.
#
# Needed: 1 x Base, 1 x Cradle, 1 x Holder; 2 x M5 x 12 countersunk screw,
# 2 x M5 nut, 3 x M3 x 10 screw.
#
# Run:  freecadcmd build_stand.py   (or ./build.sh)
# Writes stand.FCStd (parametric: change values in the Params spreadsheet)
# and an .stl per part for the slicer.
###########################

import math
import os

import Draft
import FreeCAD as App
import MeshPart
import Part
import Sketcher

HERE = os.path.dirname(os.path.abspath(__file__))
V = App.Vector

# Text on the base, and the font for it: the first file that exists (as on the cube's stand)
TEXT = "Led Tetragon"
FONTS = [os.path.expanduser("~/.fonts/segoescb.ttf"), "/run/media/jeroen/OS/Windows/Fonts/segoescb.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]

# alias, value in mm, meaning
PARAMS = [
    ("panel_size", 192, "Edge of the LED panel (64 x P3)"),
    ("panel_depth", 14, "Panel with its factory frame, front of the LEDs to back of the frame: 2 mm LEDs and board, "
                        "12 mm frame (measured)"),
    ("panel_fit", 0.5, "Play round the panel in the cradle: behind it and at both sides"),
    ("lip_height", 1, "Height of the lip in front of the panel; it covers this much of the bottom row of LEDs. "
                      "More than 0"),
    ("lip_thickness", 2, "Thickness of that lip"),
    ("floor_thickness", 4, "Thickness of the floor of the cradle, under the panel"),
    ("back_height", 28, "How far the back wall of the cradle reaches up the back of the frame; it stays below the "
                        "HUB75 IN plug, 32 mm up"),
    ("back_thickness", 4, "Thickness of the back wall"),
    ("ear_thickness", 7, "Thickness of the side plates (ears) of the cradle, which carry the hinge and the nut"),
    ("ear_front_height", 16, "Height of an ear at its front, beside the panel; its top slopes up from there to the "
                             "top of the back wall"),
    ("hinge_radius", 10, "Radius of the rounded corner under the back wall, round the hinge axis"),
    ("ring_d", 18, "Raised ring round the hinge on the outside of each ear: diameter, at most 2 x hinge_radius"),
    ("ring_height", 1, "How far that ring stands out: the only place where an ear touches its cheek"),
    ("bolt_d", 5.4, "Hole for a hinge screw (M5)"),
    ("bolt_length", 12, "Length of a hinge screw, head included: M5 x 12 countersunk (only used for checking)"),
    ("screw_head_d", 10, "Diameter of the countersunk head of a hinge screw (M5: 10 mm; only used for checking)"),
    ("countersink_d", 10.4, "Countersink for that head in the outside of each cheek, 90 degrees: diameter at the "
                            "surface"),
    ("nut_af", 8.2, "Pocket for the M5 nut on the inside of each ear: across the flats (a nut is 8 mm)"),
    ("nut_depth", 4.2, "Depth of that pocket (a nut is 4 mm thick)"),
    ("base_thickness", 4, "Thickness of the base plate"),
    ("base_front", 40, "How far the base reaches in front of the hinge axis"),
    ("base_back", 90, "How far the base reaches behind the hinge axis"),
    ("base_gap", 1, "Space between the cradle and the base plate"),
    ("cheek_thickness", 4.5, "Thickness of the two cheeks on the base, with the countersink in it"),
    ("cheek_width", 20, "Width of a cheek; its top is a half round of this diameter round the hinge axis"),
    ("text_size", 10, "Height of the letters on the base"),
    ("text_depth", 0.8, "How deep the letters are sunk into the base"),
    ("text_margin", 7, "Front edge of the base to the letters"),
    # The back of the panel, seen from the back with the panel standing: "from the left" and "from the top" are
    # from the edges of the panel. See PANEL.md.
    ("frame_bar_width", 16, "Width of the four bars round the edge of the frame, flush with its back"),
    ("middle_bar_width", 20, "Width of the vertical middle bar, flush with the back of the frame"),
    ("bar_hole_top", 10, "Top of the 4 M3 holes (brass inserts, evenly spaced) in the middle bar: from the top"),
    ("side_hole_left", 17, "Top left M3 hole, in the top bar: from the left"),
    ("side_hole_top", 8, "Top left M3 hole, in the top bar: from the top"),
    ("side_mid_hole_left", 9, "Middle M3 hole in the left bar: from the left"),
    ("side_mid_hole_top", 87, "Middle M3 hole in the left bar: from the top"),
    ("pi_from_left", 90, "Pi with its hat: from the left to its nearest part"),
    ("pi_from_right", 40, "Pi with its hat: from the right"),
    ("pi_from_top", 40, "Pi: from the top to its top, the USB ports"),
    ("hat_from_bottom", 39, "The hat, sticking out below the Pi: from the bottom"),
    ("pi_gap", 7, "Back of the frame to the solder under the Pi, whose board lies 10 mm behind it"),
    ("pi_depth", 30, "How far the Pi with its hat sticks out behind the frame"),
    ("m3_d", 3.4, "Holes in the holder for its M3 screws"),
    ("holder_plate", 3, "Thickness of the plate of the holder, against the back of the frame"),
    ("holder_wall", 1.6, "Walls of the holder"),
    ("speaker_length", 84, "USB speaker: length of its flat grille face, a rectangle with half round ends"),
    ("speaker_height", 43, "Height of that face"),
    ("speaker_depth", 32, "Grille face to the back of its rounded body"),
    ("speaker_left", 5, "Speaker: from the left to the end of its face; its round end stays clear of the Pi"),
    ("speaker_top", 20, "Speaker: from the top to the top of its face"),
    ("speaker_fit", 0.4, "Play round the speaker in its cup, on each side"),
    ("cup_lip_width", 0.8, "How far the lips along the long sides of the cup reach over the speaker's face"),
    ("cup_lip_thickness", 1.2, "Thickness of those lips"),
    ("speaker_cable_at", 33, "Speaker's cable: leaves the bottom side this far from the left end of its face"),
    ("speaker_cable_room", 10, "Speaker's cable: room it needs below the speaker, for its sleeve"),
    ("cable_slot", 8, "Width of the slot in the bottom of the cup for the speaker's cable and its sleeve"),
    ("microbit_width", 51.6, "micro:bit V2: width, the edge with the USB port; upright in its holder"),
    ("microbit_height", 42, "Height of the micro:bit; across in its holder"),
    ("microbit_thickness", 11.65, "Thickness of the micro:bit with its parts on both sides"),
    ("microbit_fit", 0.6, "Play round the micro:bit in its pocket, in total"),
    ("microbit_left", 14, "Pocket of the micro:bit: from the left, just past the screw in the left bar"),
    ("microbit_top", 88, "Pocket of the micro:bit: from the top, just below the power connector, so the HUB75 "
                         "ribbon has room below it"),
    ("microbit_window", 4, "Edge left round the window in the cover over the micro:bit"),
    ("usb_slot", 14, "Width of the slot for the micro:bit's USB plug, in the side of its pocket"),
]
P = {alias: value for alias, value, _ in PARAMS}

# The cradle is modelled in the panel's own frame: x from the front of the panel backwards,
# y from its bottom edge upwards, z across, 0 in the middle. Names in capitals are the
# spreadsheet expressions of the lower-case values.
hw = P["panel_size"] / 2 + P["panel_fit"]  # inside of an ear
HW = "(Params.panel_size / 2 + Params.panel_fit)"
xb = P["panel_depth"] + P["panel_fit"]  # front of the back wall
XB = "(Params.panel_depth + Params.panel_fit)"
xbo = xb + P["back_thickness"]  # back of the cradle
XBO = "(Params.panel_depth + Params.panel_fit + Params.back_thickness)"
px, py = xbo - P["hinge_radius"], P["hinge_radius"] - P["floor_thickness"]  # hinge axis
PX, PY = "(%s - Params.hinge_radius)" % XBO, "(Params.hinge_radius - Params.floor_thickness)"
out = hw + P["ear_thickness"]  # outside of an ear
OUT = "(%s + Params.ear_thickness)" % HW
ci = out + P["ring_height"]  # inside of a cheek
CI = "(%s + Params.ring_height)" % OUT
# The base is modelled as it stands: x backwards from the hinge axis, y across, z up from the table.
ph = P["base_thickness"] + P["base_gap"] + P["hinge_radius"]  # height of the hinge axis
PH = "(Params.base_thickness + Params.base_gap + Params.hinge_radius)"

ORIGIN = (-1, 1)  # sketch origin point
H_AXIS, V_AXIS = -1, -2
ALONG_Y = App.Rotation(V(1, 0, 0), -90)  # turns a cylinder or prism from along z to along y
POINT_UP = App.Rotation(V(0, 0, 1), 30)  # turns a hex so that a corner, not a flat, points along y


def new_sketch(body, name, plane, z=0, z_expression=None):
    sketch = body.newObject("Sketcher::SketchObject", name)
    support = next(f for f in body.Origin.OriginFeatures if f.Role == plane)
    sketch.AttachmentSupport = [(support, "")]
    sketch.MapMode = "FlatFace"
    sketch.AttachmentOffset = App.Placement(V(0, 0, z), App.Rotation())
    if z_expression:
        sketch.setExpression("AttachmentOffset.Base.z", z_expression)
    return sketch


def dimension(sketch, constraint, name, expression):
    """Add a dimension that follows the Params spreadsheet."""
    sketch.renameConstraint(sketch.addConstraint(constraint), name)
    sketch.setExpression("Constraints." + name, expression)


def pinned_polygon(sketch, corners, arcs=()):
    """A closed outline whose corners are each held at (x, y), given as (x, y, x expression, y expression).
    An expression gives the distance from the axis, so it is never negative; None means on the axis.
    `arcs` maps i to (cx, cy, cx expression): the side from corner i to the next is then an arc round
    (cx, cy), anticlockwise, instead of a straight line."""
    n = len(corners)
    arcs = dict(arcs)
    for i in range(n):
        start, end = V(*corners[i][:2]), V(*corners[(i + 1) % n][:2])
        if i in arcs:
            centre = V(*arcs[i][:2])
            sketch.addGeometry(Part.ArcOfCircle(Part.Circle(centre, V(0, 0, 1), (start - centre).Length),
                                                math.atan2(start.y - centre.y, start.x - centre.x),
                                                math.atan2(end.y - centre.y, end.x - centre.x)))
        else:
            sketch.addGeometry(Part.LineSegment(start, end))
    for i in range(n):
        sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % n, 1))
    for i, (x, y, x_expression, y_expression) in enumerate(corners):
        for axis, value, expression, line in (("X", x, x_expression, V_AXIS), ("Y", y, y_expression, H_AXIS)):
            name = "corner%d_%s" % (i, axis.lower())
            if expression is None:
                sketch.addConstraint(Sketcher.Constraint("PointOnObject", i, 1, line))
            elif value >= 0:
                dimension(sketch, Sketcher.Constraint("Distance" + axis, *ORIGIN, i, 1, value), name, expression)
            else:
                dimension(sketch, Sketcher.Constraint("Distance" + axis, i, 1, *ORIGIN, -value), name, expression)
    for i, (cx, _, cx_expression) in arcs.items():
        # both ends are held already, so the place of the centre across fixes the arc
        dimension(sketch, Sketcher.Constraint("DistanceX", *ORIGIN, i, 3, cx), "arc%d_centre_x" % i, cx_expression)


def pad(body, name, sketch, length_expression, symmetric=False, reversed_=False):
    feature = body.newObject("PartDesign::Pad", name)
    feature.Profile = sketch
    feature.setExpression("Length", length_expression)
    if symmetric:
        feature.SideType = "Symmetric"
    feature.Reversed = reversed_
    return feature


def primitive(body, kind, name, sizes, at, turn=App.Rotation()):
    """A PartDesign primitive. `sizes` maps a property to (value, expression); `at` is three
    (value, expression) pairs for its place, an expression None meaning a fixed value."""
    feature = body.newObject("PartDesign::" + kind, name)
    for prop, (value, expression) in sizes.items():
        setattr(feature, prop, value)
        if expression:
            feature.setExpression(prop, expression)
    feature.Placement = App.Placement(V(*(value for value, _ in at)), turn)
    for axis, (_, expression) in zip("xyz", at):
        if expression:
            feature.setExpression("Placement.Base." + axis, expression)
    return feature


def hexagon(body, kind, name, across_flats, af_expression, height, height_expression, at, turn):
    return primitive(body, kind, name, {"Polygon": (6, None),
                                        "Circumradius": (across_flats / math.sqrt(3), af_expression + " / sqrt(3)"),
                                        "Height": (height, height_expression)}, at, turn)


doc = App.newDocument("stand")

params = doc.addObject("Spreadsheet::Sheet", "Params")
for row, (alias, value, meaning) in enumerate(PARAMS, start=1):
    params.set("A%d" % row, alias)
    params.set("B%d" % row, "%g mm" % value)
    params.set("C%d" % row, meaning)
    params.setAlias("B%d" % row, alias)
doc.recompute()

###########################
# Cradle
###########################

cradle = doc.addObject("PartDesign::Body", "Cradle")
# Cross-section, seen from the right-hand end: lip, floor, back wall. The corner under the back
# wall is rounded round the hinge axis, so at any angle between lying flat and upright no part
# of the cradle comes lower than the bottom of that round.
lip_t, floor_t, lip_h, back_h = P["lip_thickness"], P["floor_thickness"], P["lip_height"], P["back_height"]
profile = new_sketch(cradle, "CradleProfile", "XY_Plane")
pinned_polygon(profile, [(-lip_t, -floor_t, "Params.lip_thickness", "Params.floor_thickness"),
                         (px, -floor_t, PX, "Params.floor_thickness"),
                         (xbo, py, XBO, PY),
                         (xbo, back_h, XBO, "Params.back_height"),
                         (xb, back_h, XB, "Params.back_height"),
                         (xb, 0, XB, None),
                         (0, 0, None, None),
                         (0, lip_h, None, "Params.lip_height"),
                         (-lip_t, lip_h, "Params.lip_thickness", "Params.lip_height")],
               {1: (px, py, PX)})
pad(cradle, "Channel", profile, "2 * " + HW, symmetric=True)

# The ears: the same outline under the panel, and a top that slopes up from the front to the
# top of the back wall.
for side, sign in (("Right", 1), ("Left", -1)):
    ear = new_sketch(cradle, "Ear%sSketch" % side, "XY_Plane", sign * hw, ("" if sign > 0 else "-") + HW)
    pinned_polygon(ear, [(-lip_t, -floor_t, "Params.lip_thickness", "Params.floor_thickness"),
                         (px, -floor_t, PX, "Params.floor_thickness"),
                         (xbo, py, XBO, PY),
                         (xbo, back_h, XBO, "Params.back_height"),
                         (-lip_t, P["ear_front_height"], "Params.lip_thickness", "Params.ear_front_height")],
                   {1: (px, py, PX)})
    pad(cradle, "Ear" + side, ear, "Params.ear_thickness", reversed_=sign < 0)

for side, z, z_expression in (("Right", out, OUT), ("Left", -out - P["ring_height"], "-%s - Params.ring_height" % OUT)):
    primitive(cradle, "AdditiveCylinder", "Ring" + side,
              {"Radius": (P["ring_d"] / 2, "Params.ring_d / 2"), "Height": (P["ring_height"], "Params.ring_height")},
              [(px, PX), (py, PY), (z, z_expression)])
primitive(cradle, "SubtractiveCylinder", "HingeHole",
          {"Radius": (P["bolt_d"] / 2, "Params.bolt_d / 2"), "Height": (2 * ci + 2, "2 * %s + 2 mm" % CI)},
          [(px, PX), (py, PY), (-ci - 1, "-%s - 1 mm" % CI)])
# Nut pockets, open towards the panel: the nut goes in before the panel, and the bolt pulls it
# against the end of its pocket.
for side, z, z_expression in (("Right", hw, HW), ("Left", -hw - P["nut_depth"], "-%s - Params.nut_depth" % HW)):
    hexagon(cradle, "SubtractivePrism", "NutPocket" + side, P["nut_af"], "Params.nut_af",
            P["nut_depth"], "Params.nut_depth", [(px, PX), (py, PY), (z, z_expression)], POINT_UP)

###########################
# Base
###########################

base = doc.addObject("PartDesign::Body", "Base")
half = ci + P["cheek_thickness"]  # half the width of the base
HALF = "(%s + Params.cheek_thickness)" % CI
primitive(base, "AdditiveBox", "Plate",
          {"Length": (P["base_front"] + P["base_back"], "Params.base_front + Params.base_back"),
           "Width": (2 * half, "2 * " + HALF), "Height": (P["base_thickness"], "Params.base_thickness")},
          [(-P["base_front"], "-Params.base_front"), (-half, "-" + HALF), (0, None)])
cw = P["cheek_width"]
for side, y, y_expression in (("Right", ci, CI), ("Left", -half, "-" + HALF)):
    primitive(base, "AdditiveBox", "Cheek" + side,
              {"Length": (cw, "Params.cheek_width"), "Width": (P["cheek_thickness"], "Params.cheek_thickness"),
               "Height": (ph, PH)},
              [(-cw / 2, "-Params.cheek_width / 2"), (y, y_expression), (0, None)])
    primitive(base, "AdditiveCylinder", "CheekTop" + side,
              {"Radius": (cw / 2, "Params.cheek_width / 2"), "Height": (P["cheek_thickness"], "Params.cheek_thickness")},
              [(0, None), (y, y_expression), (ph, PH)], ALONG_Y)
primitive(base, "SubtractiveCylinder", "CheekHoles",
          {"Radius": (P["bolt_d"] / 2, "Params.bolt_d / 2"), "Height": (2 * half + 2, "2 * %s + 2 mm" % HALF)},
          [(0, None), (-half - 1, "-%s - 1 mm" % HALF), (ph, PH)], ALONG_Y)
# Countersinks for the screw heads: a 90 degree cone from the hole out to the surface of the
# cheek, and 1 mm beyond it for a clean cut
sink = (P["countersink_d"] - P["bolt_d"]) / 2
SINK = "(Params.countersink_d - Params.bolt_d) / 2"
for side, sign in (("Right", 1), ("Left", -1)):
    primitive(base, "SubtractiveCone", "Countersink" + side,
              {"Radius1": (P["bolt_d"] / 2, "Params.bolt_d / 2"), "Radius2": (P["countersink_d"] / 2 + 1,
                                                                             "Params.countersink_d / 2 + 1 mm"),
               "Height": (sink + 1, SINK + " + 1 mm")},
              [(0, None), (sign * (half - sink), ("" if sign > 0 else "-") + "(%s - %s)" % (HALF, SINK)), (ph, PH)],
              App.Rotation(V(1, 0, 0), -90 * sign))  # widens outwards

# The name, sunk into the plate in front of the panel and readable from the front
font = next(f for f in FONTS if os.path.exists(f))
letters = Draft.make_shapestring(TEXT, font, P["text_size"])
letters.Label = "Text"
letters.Justification = "Middle-Center"
letters.setExpression("Size", "Params.text_size")
letters.Placement = App.Placement(V(-P["base_front"] + P["text_margin"] + P["text_size"] / 2, 0, P["base_thickness"]),
                                  App.Rotation(V(0, 0, 1), -90))
letters.setExpression("Placement.Base.x", "-Params.base_front + Params.text_margin + Params.text_size / 2")
letters.setExpression("Placement.Base.z", "Params.base_thickness")
base.addObject(letters)
sunk = base.newObject("PartDesign::Pocket", "TextCut")
sunk.Profile = letters
sunk.setExpression("Length", "Params.text_depth")

###########################
# Holder on the back of the panel
###########################

# Modelled in the panel's frame like the cradle: x backwards from the front of the panel, y up
# from its bottom edge, z across. The places on the back are given as seen from the back: u
# from the left edge, v from the top edge; so y = panel_size - v and z = panel_size / 2 - u.
size, depth = P["panel_size"], P["panel_depth"]
ALONG_X = App.Rotation(V(0, 1, 0), 90)  # turns a cylinder from along z to along x


def mm(value, expression=None):
    """A length with its spreadsheet expression; a plain number gets one of its own."""
    return value, expression or "%g mm" % value


def add(a, b, sign=1):
    return a[0] + sign * b[0], "(%s) %s (%s)" % (a[1], "+" if sign > 0 else "-", b[1])


def region(body, kind, name, xs, us, vs):
    """A box from xs[0] to xs[1] backwards, us[0] to us[1] from the left, vs[0] to vs[1] from the top."""
    (x0, X0), (x1, X1) = xs
    (u0, U0), (u1, U1) = us
    (v0, V0), (v1, V1) = vs
    return primitive(body, kind, name, {"Length": (x1 - x0, "(%s) - (%s)" % (X1, X0)),
                                        "Width": (v1 - v0, "(%s) - (%s)" % (V1, V0)),
                                        "Height": (u1 - u0, "(%s) - (%s)" % (U1, U0))},
                     [(x0, X0), (size - v1, "Params.panel_size - (%s)" % V1),
                      (size / 2 - u1, "Params.panel_size / 2 - (%s)" % U1)])


def post(body, kind, name, xs, u, v, radius):
    """A cylinder from xs[0] to xs[1] backwards, round (u, v)."""
    (x0, X0), (x1, X1) = xs
    return primitive(body, kind, name, {"Radius": radius, "Height": (x1 - x0, "(%s) - (%s)" % (X1, X0))},
                     [(x0, X0), (size - v[0], "Params.panel_size - (%s)" % v[1]),
                      (size / 2 - u[0], "Params.panel_size / 2 - (%s)" % u[1])], ALONG_X)


def stadium(body, kind, name, xs, ends, v, radius):
    """A rectangle with half round ends, from xs[0] to xs[1] backwards: the round ends round (u, v)
    for u in `ends`, both of `radius`."""
    region(body, kind, name, xs, ends, (add(v, radius, -1), add(v, radius)))
    for i, u in enumerate(ends):
        post(body, kind.replace("Box", "Cylinder"), "%sEnd%d" % (name, i + 1), xs, u, v, radius)


D = mm(depth, "Params.panel_depth")
PLATE = add(D, mm(P["holder_plate"], "Params.holder_plate"))  # back of a plate
WALL = mm(P["holder_wall"], "Params.holder_wall")
M3 = mm(P["m3_d"] / 2, "Params.m3_d / 2")

# The speaker at the top
holder = doc.addObject("PartDesign::Body", "Holder")
fit = mm(P["speaker_fit"], "Params.speaker_fit")
left = mm(P["speaker_left"], "Params.speaker_left")
length = mm(P["speaker_length"], "Params.speaker_length")
half = mm(P["speaker_height"] / 2, "Params.speaker_height / 2")
middle = add(mm(P["speaker_top"], "Params.speaker_top"), half)  # v of the middle of the speaker
ends = (add(left, half), add(add(left, length), half, -1))  # u of the centres of its round ends
r_in = add(half, fit)
r_out = add(r_in, WALL)
lips = add(add(PLATE, mm(P["speaker_depth"], "Params.speaker_depth")), mm(0.2))  # face of the speaker
rim = add(lips, mm(P["cup_lip_thickness"], "Params.cup_lip_thickness"))
stadium(holder, "AdditiveBox", "SpeakerPlate", (D, PLATE), ends, middle, r_out)
# a strip along the top to the screw holes in the top left corner and the middle bar
region(holder, "AdditiveBox", "ScrewStrip", (D, PLATE),
       (add(mm(P["side_hole_left"], "Params.side_hole_left"), mm(6), -1), mm(size / 2 + 6, "Params.panel_size / 2 + 6 mm")),
       (mm(2), add(middle, r_out, -1)))
stadium(holder, "AdditiveBox", "Cup", (PLATE, rim), ends, middle, r_out)
stadium(holder, "SubtractiveBox", "CupInside", (PLATE, add(rim, mm(1))), ends, middle, r_in)
lip = mm(P["cup_lip_width"], "Params.cup_lip_width")
for name, vs in (("LipTop", (add(middle, r_in, -1), add(add(middle, r_in, -1), lip))),
                 ("LipBottom", (add(add(middle, r_in), lip, -1), add(middle, r_in)))):
    region(holder, "AdditiveBox", name, (lips, rim), ends, vs)
# a slot in the bottom of the cup, from the plate to the rim, where the cable leaves the speaker
slot = mm(P["cable_slot"] / 2, "Params.cable_slot / 2")
cable_u = add(left, mm(P["speaker_cable_at"], "Params.speaker_cable_at"))
region(holder, "SubtractiveBox", "CableSlot", (PLATE, add(rim, mm(1))),
       (add(cable_u, slot, -1), add(cable_u, slot)), (add(middle, add(r_in, mm(1), -1)), add(middle, add(r_out, mm(1)))))
# where the Pi comes close, only the plate and the rim of the cup stay
region(holder, "SubtractiveBox", "PiClearance",
       (add(D, mm(P["pi_gap"] - 1, "Params.pi_gap - 1 mm")), add(D, mm(P["pi_depth"] + 1, "Params.pi_depth + 1 mm"))),
       (mm(P["pi_from_left"] - 1, "Params.pi_from_left - 1 mm"), mm(size, "Params.panel_size")),
       (mm(P["pi_from_top"] - 1, "Params.pi_from_top - 1 mm"), mm(size, "Params.panel_size")))
for name, u, v in (("SideScrewHole", mm(P["side_hole_left"], "Params.side_hole_left"),
                    mm(P["side_hole_top"], "Params.side_hole_top")),
                   ("BarScrewHole", mm(size / 2, "Params.panel_size / 2"), mm(P["bar_hole_top"], "Params.bar_hole_top"))):
    post(holder, "SubtractiveCylinder", name, (add(D, mm(1), -1), add(PLATE, mm(1))), u, v, M3)

# The micro:bit below it, upright, its USB edge towards the Pi
ml = mm(P["microbit_left"], "Params.microbit_left")
mt = mm(P["microbit_top"], "Params.microbit_top")
across = mm(P["microbit_height"] + P["microbit_fit"], "Params.microbit_height + Params.microbit_fit")
down = mm(P["microbit_width"] + P["microbit_fit"], "Params.microbit_width + Params.microbit_fit")
cover = add(PLATE, mm(P["microbit_thickness"] + P["microbit_fit"], "Params.microbit_thickness + Params.microbit_fit"))
pocket_u, pocket_v = (ml, add(ml, across)), (mt, add(mt, down))
outer_u, outer_v = (add(ml, WALL, -1), add(pocket_u[1], WALL)), (add(mt, WALL, -1), add(pocket_v[1], WALL))
region(holder, "AdditiveBox", "MicrobitPlate", (D, PLATE), (mm(1), outer_u[1]), outer_v)
screw_u = mm(P["side_mid_hole_left"], "Params.side_mid_hole_left")
screw_v = mm(P["side_mid_hole_top"], "Params.side_mid_hole_top")
# a strip down the left bar joins it to the plate of the speaker, past the middle hole of that bar
region(holder, "AdditiveBox", "LeftStrip", (D, PLATE), (mm(1), outer_u[0]), (middle, add(outer_v[0], mm(1))))
region(holder, "AdditiveBox", "MicrobitWalls", (PLATE, add(cover, WALL)), outer_u, outer_v)
# the pocket, open to the side edge of the panel
region(holder, "SubtractiveBox", "MicrobitPocket", (PLATE, cover), (mm(-1), pocket_u[1]), pocket_v)
window = mm(P["microbit_window"], "Params.microbit_window")
region(holder, "SubtractiveBox", "Window", (add(cover, mm(1), -1), add(add(cover, WALL), mm(1))),
       (add(ml, window), add(pocket_u[1], window, -1)), (add(mt, window), add(pocket_v[1], window, -1)))
usb = mm(P["usb_slot"] / 2, "Params.usb_slot / 2")
centre_v = add(mt, mm((P["microbit_width"] + P["microbit_fit"]) / 2,
                      "(Params.microbit_width + Params.microbit_fit) / 2"))
region(holder, "SubtractiveBox", "UsbSlot", (PLATE, cover),
       (add(pocket_u[1], mm(1), -1), add(outer_u[1], mm(1))), (add(centre_v, usb, -1), add(centre_v, usb)))
post(holder, "SubtractiveCylinder", "LeftScrewHole", (add(D, mm(1), -1), add(PLATE, mm(1))), screw_u, screw_v, M3)

doc.recompute()

for obj in doc.Objects:
    if obj.isDerivedFrom("Sketcher::SketchObject") and not obj.FullyConstrained:
        print("%s is not fully constrained" % obj.Name, flush=True)
        raise SystemExit(1)
    if obj.State and "Invalid" in obj.State:
        print("%s did not build" % obj.Name, flush=True)
        raise SystemExit(1)

doc.saveAs(os.path.join(HERE, "stand.FCStd"))
for part, stl in ((base, "base.stl"), (cradle, "cradle.stl"), (holder, "holder.stl")):
    shape = part.Shape
    if not shape.isValid() or len(shape.Solids) != 1:
        print("%s is not a single valid solid" % part.Name, flush=True)
        raise SystemExit(1)
    if part is cradle:  # printed lying on its floor
        shape = shape.copy()
        shape.rotate(V(), V(1, 0, 0), 90)
        shape.translate(V(0, 0, -shape.optimalBoundingBox().ZMin))
    if part is holder:  # printed lying on its plate
        shape = shape.copy()
        shape.rotate(V(), V(0, 1, 0), -90)
        shape.translate(V(0, 0, -shape.optimalBoundingBox().ZMin))
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.02, AngularDeflection=0.2)
    mesh.write(os.path.join(HERE, stl))
    box = shape.optimalBoundingBox()
    print("%s %.2f x %.2f x %.2f mm, %.2f cm3" % (stl, box.XLength, box.YLength, box.ZLength, shape.Volume / 1000),
          flush=True)
