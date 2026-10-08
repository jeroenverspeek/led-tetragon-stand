# Parts for the stand of the LED tetragon
# by Jeroen Verspeek
#
# The tetragon is a single LED panel (64 x 64, P3, 192 x 192 mm) on its factory
# frame. The Raspberry Pi with its hat is fixed to the back of that frame, from
# the middle upwards, in landscape. The stand holds the panel leaning back at
# an angle that is set by hand and held by friction.
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
# Base: a plate on the table with an upright cheek at both ends. A bolt goes
# from outside through each cheek into the nut in the ear. Tightening it
# presses the cheek against the ring on the ear, and that friction holds the
# angle. The name is sunk into the plate in front of the panel.
#
# Knob: holds the head of a bolt, to tighten it by hand.
#
# Needed: 1 x Base, 1 x Cradle, 2 x Knob; 2 x M5 x 16 hex bolt, 2 x M5 nut.
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
    ("bolt_d", 5.4, "Hole for a hinge bolt (M5)"),
    ("bolt_length", 16, "Length of a hinge bolt under its head, M5 x 16 (only used for checking)"),
    ("nut_af", 8.2, "Pocket for the M5 nut on the inside of each ear: across the flats (a nut is 8 mm)"),
    ("nut_depth", 4.2, "Depth of that pocket (a nut is 4 mm thick)"),
    ("base_thickness", 4, "Thickness of the base plate"),
    ("base_front", 40, "How far the base reaches in front of the hinge axis"),
    ("base_back", 90, "How far the base reaches behind the hinge axis"),
    ("base_gap", 1, "Space between the cradle and the base plate"),
    ("cheek_thickness", 4, "Thickness of the two cheeks on the base"),
    ("cheek_width", 20, "Width of a cheek; its top is a half round of this diameter round the hinge axis"),
    ("knob_d", 16, "Diameter of a knob"),
    ("knob_floor", 4.5, "Thickness of a knob under the bolt head; sets the bolt length"),
    ("bolt_head_af", 8.2, "Hex pocket in a knob for the bolt head: across the flats (M5: 8 mm)"),
    ("bolt_head_height", 4, "Depth of that pocket (an M5 bolt head is 3.5 mm)"),
    ("text_size", 10, "Height of the letters on the base"),
    ("text_depth", 0.8, "How deep the letters are sunk into the base"),
    ("text_margin", 7, "Front edge of the base to the letters"),
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
# Knob
###########################

knob = doc.addObject("PartDesign::Body", "Knob")
knob_h = P["knob_floor"] + P["bolt_head_height"]
KNOB_H = "(Params.knob_floor + Params.bolt_head_height)"
primitive(knob, "AdditiveCylinder", "KnobDisc",
          {"Radius": (P["knob_d"] / 2, "Params.knob_d / 2"), "Height": (knob_h, KNOB_H)}, [(0, None)] * 3)
# grip: six round flutes round the rim, each over a flat of the hex pocket, where the wall is thickest
for i in range(6):
    c, s = math.cos(math.radians(30 + 60 * i)), math.sin(math.radians(30 + 60 * i))
    primitive(knob, "SubtractiveCylinder", "Flute%d" % (i + 1),
              {"Radius": (2, None), "Height": (knob_h + 2, KNOB_H + " + 2 mm")},
              [((P["knob_d"] / 2 + 0.5) * c, "(Params.knob_d / 2 + 0.5 mm) * %.9f" % c),
               ((P["knob_d"] / 2 + 0.5) * s, "(Params.knob_d / 2 + 0.5 mm) * %.9f" % s), (-1, None)])
primitive(knob, "SubtractiveCylinder", "KnobHole",
          {"Radius": (P["bolt_d"] / 2, "Params.bolt_d / 2"), "Height": (knob_h + 2, KNOB_H + " + 2 mm")},
          [(0, None), (0, None), (-1, None)])
hexagon(knob, "SubtractivePrism", "HeadPocket", P["bolt_head_af"], "Params.bolt_head_af",
        P["bolt_head_height"] + 1, "Params.bolt_head_height + 1 mm",
        [(0, None), (0, None), (P["knob_floor"], "Params.knob_floor")], App.Rotation())

doc.recompute()

for obj in doc.Objects:
    if obj.isDerivedFrom("Sketcher::SketchObject") and not obj.FullyConstrained:
        print("%s is not fully constrained" % obj.Name, flush=True)
        raise SystemExit(1)
    if obj.State and "Invalid" in obj.State:
        print("%s did not build" % obj.Name, flush=True)
        raise SystemExit(1)

doc.saveAs(os.path.join(HERE, "stand.FCStd"))
for part, stl in ((base, "base.stl"), (cradle, "cradle.stl"), (knob, "knob.stl")):
    shape = part.Shape
    if not shape.isValid() or len(shape.Solids) != 1:
        print("%s is not a single valid solid" % part.Name, flush=True)
        raise SystemExit(1)
    if part is cradle:  # printed lying on its floor
        shape = shape.copy()
        shape.rotate(V(), V(1, 0, 0), 90)
        shape.translate(V(0, 0, -shape.optimalBoundingBox().ZMin))
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.02, AngularDeflection=0.2)
    mesh.write(os.path.join(HERE, stl))
    box = shape.optimalBoundingBox()
    print("%s %.2f x %.2f x %.2f mm, %.2f cm3" % (stl, box.XLength, box.YLength, box.ZLength, shape.Volume / 1000),
          flush=True)
