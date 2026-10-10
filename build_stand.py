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
# Holder: carries the USB speaker and the micro:bit on the back of the panel,
# in the top half beside the Pi (to the left of it, seen from the back). A
# plate is screwed into the top hole of the middle bar, with a rib on both
# sides of the bar so it cannot turn. The micro:bit lies flat on the plate,
# parallel to the panel, in a pocket that is open to the side edge of the
# panel; its USB plug goes down through a slot and holds it in place. On top
# of that is a cup for the rounded back of the speaker, its grille facing
# backwards, held by a lip along both long sides, with a slot for the cable at
# both ends. Prints standing on the rim of the cup.
#
# Needed: 1 x Base, 1 x Cradle, 1 x Holder; 2 x M5 x 12 countersunk screw,
# 2 x M5 nut, 1 x M3 x 10 screw.
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
    ("panel_depth", 14, "Panel with its factory frame, front of the LEDs to back of the frame (guess: 12 mm frame "
                        "+ 2 mm board)"),
    ("panel_fit", 0.5, "Play round the panel in the cradle: behind it and at both sides"),
    ("lip_height", 1, "Height of the lip in front of the panel; it covers this much of the bottom row of LEDs. "
                      "More than 0"),
    ("lip_thickness", 2, "Thickness of that lip"),
    ("floor_thickness", 4, "Thickness of the floor of the cradle, under the panel"),
    ("back_height", 40, "How far the back wall of the cradle reaches up the back of the frame; the Pi starts at "
                        "the middle"),
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
    ("bar_width", 20, "Width of the vertical middle bar on the back of the frame; its back is flush with the frame"),
    ("bar_hole_top", 10, "Top screw hole in that bar (M3, brass insert): from the top edge of the panel"),
    ("bar_fit", 0.2, "Play between the bar and the ribs of the holder on both sides of it"),
    ("m3_d", 3.4, "Hole in the holder for its M3 screw"),
    ("holder_plate", 3, "Thickness of the plate of the holder, against the back of the frame"),
    ("rib_depth", 3, "How far the ribs of the holder reach into the frame beside the bar"),
    ("rib_width", 2, "Thickness of a rib"),
    ("rib_length", 16, "Length of a rib, along the bar"),
    ("rib_from_top", 16, "Top edge of the panel to the top of the ribs"),
    ("holder_wall", 1.6, "Walls of the holder"),
    ("speaker_length", 84, "USB speaker: length of its flat grille face, a rectangle with half round ends"),
    ("speaker_height", 43, "Height of that face"),
    ("speaker_depth", 32, "Grille face to the back of its rounded body"),
    ("speaker_fit", 0.4, "Play round the speaker in its cup, on each side"),
    ("cup_lip_width", 0.8, "How far the lips along the long sides of the cup reach over the speaker's face"),
    ("cup_lip_thickness", 1.2, "Thickness of those lips"),
    ("cable_slot", 5, "Width of the slot for the speaker's cable at both ends of the cup"),
    ("microbit_width", 51.6, "micro:bit V2: width, the edge with the USB port"),
    ("microbit_height", 42, "Height of the micro:bit"),
    ("microbit_thickness", 11.65, "Thickness of the micro:bit with its parts on both sides"),
    ("microbit_fit", 0.6, "Play round the micro:bit in its pocket, in total"),
    ("usb_slot", 14, "Width of the slot for the micro:bit's USB plug, below the middle of its pocket"),
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
# Holder
###########################

# Modelled in the panel's frame like the cradle: x backwards from the front of the panel, y up
# from its bottom edge, z across (seen from the back, +z is to the left). The cup is flush with
# the top and the left edge (seen from the back), the plate reaches over the bar.
holder = doc.addObject("PartDesign::Body", "Holder")
size, depth = P["panel_size"], P["panel_depth"]
li, hi = P["speaker_length"] + 2 * P["speaker_fit"], P["speaker_height"] + 2 * P["speaker_fit"]
LI, HI = "(Params.speaker_length + 2 * Params.speaker_fit)", "(Params.speaker_height + 2 * Params.speaker_fit)"
lo, ho = li + 2 * P["holder_wall"], hi + 2 * P["holder_wall"]
LO, HO = "(%s + 2 * Params.holder_wall)" % LI, "(%s + 2 * Params.holder_wall)" % HI
yb, YB = size - ho, "(Params.panel_size - %s)" % HO  # bottom of the holder
yc, YC = size - ho / 2, "(Params.panel_size - %s / 2)" % HO  # its middle
zs, ZS = size / 2 - lo, "(Params.panel_size / 2 - %s)" % LO  # its end towards the bar
ends = [(zs + ho / 2, "(%s + %s / 2)" % (ZS, HO)), (size / 2 - ho / 2, "(Params.panel_size / 2 - %s / 2)" % HO)]
xp, XP = depth + P["holder_plate"], "(Params.panel_depth + Params.holder_plate)"  # top of the plate
mt, MT = P["microbit_thickness"] + P["microbit_fit"], "(Params.microbit_thickness + Params.microbit_fit)"
xf, XF = xp + mt + P["holder_wall"], "(%s + %s + Params.holder_wall)" % (XP, MT)  # floor of the cup
xl, XL = xf + P["speaker_depth"] + 0.2, "(%s + Params.speaker_depth + 0.2 mm)" % XF  # under the lips
xr, XR = xl + P["cup_lip_thickness"], "(%s + Params.cup_lip_thickness)" % XL  # rim of the cup
ALONG_X = App.Rotation(V(0, 1, 0), 90)  # turns a cylinder from along z to along x
rib_out = P["bar_width"] / 2 + P["bar_fit"] + P["rib_width"]
RIB_OUT = "(Params.bar_width / 2 + Params.bar_fit + Params.rib_width)"

primitive(holder, "AdditiveBox", "HolderPlate",
          {"Length": (P["holder_plate"], "Params.holder_plate"), "Width": (ho, HO),
           "Height": (size / 2 + rib_out, "Params.panel_size / 2 + " + RIB_OUT)},
          [(depth, "Params.panel_depth"), (yb, YB), (-rib_out, "-" + RIB_OUT)])
for side, z, z_expression in (("Right", -rib_out, "-" + RIB_OUT),
                              ("Left", P["bar_width"] / 2 + P["bar_fit"], "Params.bar_width / 2 + Params.bar_fit")):
    primitive(holder, "AdditiveBox", "Rib" + side,
              {"Length": (P["rib_depth"], "Params.rib_depth"), "Width": (P["rib_length"], "Params.rib_length"),
               "Height": (P["rib_width"], "Params.rib_width")},
              [(depth - P["rib_depth"], "Params.panel_depth - Params.rib_depth"),
               (size - P["rib_from_top"] - P["rib_length"], "Params.panel_size - Params.rib_from_top - Params.rib_length"),
               (z, z_expression)])
# under the cup: a block with the pocket for the micro:bit, its top the floor of the cup
primitive(holder, "AdditiveBox", "MicrobitBlock",
          {"Length": (xf - xp, MT + " + Params.holder_wall"), "Width": (ho, HO), "Height": (lo, LO)},
          [(xp, XP), (yb, YB), (zs, ZS)])
# the cup: a rectangle with half round ends, as the speaker
primitive(holder, "AdditiveBox", "Cup",
          {"Length": (xr - xf, "%s - %s" % (XR, XF)), "Width": (ho, HO), "Height": (lo - ho, "%s - %s" % (LO, HO))},
          [(xf, XF), (yb, YB), ends[0]])
for i, end in enumerate(ends):
    primitive(holder, "AdditiveCylinder", "CupEnd%d" % (i + 1),
              {"Radius": (ho / 2, HO + " / 2"), "Height": (xr - xf, "%s - %s" % (XR, XF))},
              [(xf, XF), (yc, YC), end], ALONG_X)
primitive(holder, "SubtractiveBox", "CupInside",
          {"Length": (xr - xf + 1, "%s - %s + 1 mm" % (XR, XF)), "Width": (hi, HI),
           "Height": (lo - ho, "%s - %s" % (LO, HO))},
          [(xf, XF), (yc - hi / 2, "%s - %s / 2" % (YC, HI)), ends[0]])
for i, end in enumerate(ends):
    primitive(holder, "SubtractiveCylinder", "CupEndInside%d" % (i + 1),
              {"Radius": (hi / 2, HI + " / 2"), "Height": (xr - xf + 1, "%s - %s + 1 mm" % (XR, XF))},
              [(xf, XF), (yc, YC), end], ALONG_X)
# the lips along the long sides, over the rim of the speaker's face
for side, y, y_expression in (("Top", yc + hi / 2 - P["cup_lip_width"], "%s + %s / 2 - Params.cup_lip_width" % (YC, HI)),
                              ("Bottom", yc - hi / 2, "%s - %s / 2" % (YC, HI))):
    primitive(holder, "AdditiveBox", "Lip" + side,
              {"Length": (P["cup_lip_thickness"], "Params.cup_lip_thickness"),
               "Width": (P["cup_lip_width"], "Params.cup_lip_width"),
               "Height": (lo - ho, "%s - %s" % (LO, HO))},
              [(xl, XL), (y, y_expression), ends[0]])
# a slot for the cable at both ends, from the floor of the cup to the rim
for i, (z, z_expression) in enumerate([(zs - 1, ZS + " - 1 mm"),
                                       (size / 2 - P["holder_wall"] - 1, "Params.panel_size / 2 - Params.holder_wall - 1 mm")]):
    primitive(holder, "SubtractiveBox", "CableSlot%d" % (i + 1),
              {"Length": (xr - xf + 1, "%s - %s + 1 mm" % (XR, XF)), "Width": (P["cable_slot"], "Params.cable_slot"),
               "Height": (P["holder_wall"] + 2, "Params.holder_wall + 2 mm")},
              [(xf, XF), (yc - P["cable_slot"] / 2, "%s - Params.cable_slot / 2" % YC), (z, z_expression)])
# the pocket for the micro:bit, open to the side edge of the panel: it slides in from there
mw, MW = P["microbit_width"] + P["microbit_fit"], "(Params.microbit_width + Params.microbit_fit)"
mh, MH = P["microbit_height"] + P["microbit_fit"], "(Params.microbit_height + Params.microbit_fit)"
zm, ZM = zs + P["holder_wall"], "(%s + Params.holder_wall)" % ZS  # end of the pocket
primitive(holder, "SubtractiveBox", "MicrobitPocket",
          {"Length": (mt, MT), "Width": (mh, MH), "Height": (size / 2 + 1 - zm, "Params.panel_size / 2 + 1 mm - " + ZM)},
          [(xp, XP), (yc - mh / 2, "%s - %s / 2" % (YC, MH)), (zm, ZM)])
# its USB plug goes down through the bottom of the pocket, below the middle of the micro:bit
primitive(holder, "SubtractiveBox", "UsbSlot",
          {"Length": (mt, MT), "Width": (ho / 2 - mh / 2 + 1, "%s / 2 - %s / 2 + 1 mm" % (HO, MH)),
           "Height": (P["usb_slot"], "Params.usb_slot")},
          [(xp, XP), (yb - 0.5, YB + " - 0.5 mm"),
           (zm + mw / 2 - P["usb_slot"] / 2, "%s + %s / 2 - Params.usb_slot / 2" % (ZM, MW))])
primitive(holder, "SubtractiveCylinder", "ScrewHole",
          {"Radius": (P["m3_d"] / 2, "Params.m3_d / 2"),
           "Height": (P["holder_plate"] + P["rib_depth"] + 2, "Params.holder_plate + Params.rib_depth + 2 mm")},
          [(depth - P["rib_depth"] - 1, "Params.panel_depth - Params.rib_depth - 1 mm"),
           (size - P["bar_hole_top"], "Params.panel_size - Params.bar_hole_top"), (0, None)], ALONG_X)

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
    if part is holder:  # printed standing on the rim of the cup
        shape = shape.copy()
        shape.rotate(V(), V(0, 1, 0), 90)
        shape.translate(V(0, 0, -shape.optimalBoundingBox().ZMin))
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.02, AngularDeflection=0.2)
    mesh.write(os.path.join(HERE, stl))
    box = shape.optimalBoundingBox()
    print("%s %.2f x %.2f x %.2f mm, %.2f cm3" % (stl, box.XLength, box.YLength, box.ZLength, shape.Volume / 1000),
          flush=True)
