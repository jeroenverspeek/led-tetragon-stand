# Stand for the 128 x 128 LED panel
# by Jeroen Verspeek
#
# The panel (128 x 128, P1.875, 240 x 240 mm) leans back at a fixed angle, 15
# degrees from upright (75 degrees to the table), in a stand made in one
# piece. Like the cradle of the 64 x 64 stand (build_stand.py) it has a
# channel over the full width that the bottom edge of the panel stands in: a
# floor, a low lip in front and a back wall up the back of the panel, with an
# ear at both ends. Here the channel does not turn on a hinge: it is built
# tilted onto the base plate, the space under its floor filled down to the
# plate, so it prints without support. The name is sunk into the plate in
# front of the panel.
#
# The stand is 249 mm wide: in one piece on the Bambu Lab X2D (256 x 256 mm),
# in two halves on the Ender 3 v2, glued. The joint goes across between the
# words of the name; dovetails in the plate, in front of and behind the
# channel, hold the halves in line, and one half slides down onto the other.
#
# Run:  freecadcmd build_stand128.py   (or ./build.sh 128)
# Writes stand128.FCStd (the stand parametric: change values in the Params
# spreadsheet; the halves made from it as plain shapes) and stand128.stl (one
# piece), stand128_left.stl and stand128_right.stl (the halves) for the slicer.
###########################

import math
import os
import sys

import Draft
import FreeCAD as App
import Part

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stand_lib import check_built, font, make_params, new_sketch, pad, pinned_polygon, primitive, write_stl  # noqa: E402

V = App.Vector

TEXT = "Led Tetragon"  # on the base

# alias, value in mm (or in the unit given), meaning
PARAMS = [
    ("panel_size", 240, "Edge of the LED panel (128 x P1.875; measured 24 x 24 cm)"),
    ("panel_depth", 14, "Panel, front of the LEDs to the back of the panel or its frame (guess, as the 64 x 64; "
                        "measure)"),
    ("panel_fit", 0.5, "Play round the panel in the channel: behind it and at both sides"),
    ("tilt", 15, "How far the panel leans back from upright: 15 degrees is 75 degrees to the table", "deg"),
    ("lip_height", 1, "Height of the lip in front of the panel; it covers this much of the bottom row of LEDs. "
                      "More than 0"),
    ("lip_thickness", 2, "Thickness of that lip"),
    ("floor_thickness", 4, "Thickness of the floor of the channel, under the panel"),
    ("back_height", 28, "How far the back wall reaches up the back of the panel; keep it below the plugs on the back "
                        "(guess, as the 64 x 64; check)"),
    ("back_thickness", 4, "Thickness of the back wall"),
    ("ear_thickness", 4, "Thickness of the ears at both ends of the channel, which keep the panel in the middle"),
    ("ear_front_height", 16, "Height of an ear at its front, beside the panel; its top slopes up from there to the "
                             "top of the back wall"),
    ("base_thickness", 5, "Thickness of the base plate, and of the dovetails in it"),
    ("base_front", 40, "How far the base reaches in front of the bottom edge of the panel"),
    ("base_back", 90, "How far the base reaches behind it"),
    ("text_size", 10, "Height of the letters on the base"),
    ("text_depth", 0.8, "How deep the letters are sunk into the base"),
    ("text_margin", 7, "Front edge of the base to the letters"),
    ("dovetail_neck", 8, "The halves for the Ender: width of a dovetail where it leaves its half"),
    ("dovetail_head", 12, "Width of a dovetail at its end"),
    ("dovetail_length", 8, "How far a dovetail reaches into the other half"),
    ("joint_fit", 0.15, "Play all round the joint between the halves, for the glue"),
]
P = {row[0]: row[1] for row in PARAMS}

# Modelled as it stands, seen from the right-hand end: x backwards from the bottom edge of the
# front of the panel, y up from the table, z across, 0 in the middle, to the right seen from
# the front. The channel is sketched in the panel's own frame (x backwards from the front of the
# panel, y up from its bottom edge, as the cradle of the 64 x 64) and the sketch is turned back by
# the tilt. Names in capitals are the spreadsheet expressions of the lower-case values.
tilt = math.radians(P["tilt"])
hw = P["panel_size"] / 2 + P["panel_fit"]  # inside of an ear
HW = "(Params.panel_size / 2 + Params.panel_fit)"
xb = P["panel_depth"] + P["panel_fit"]  # front of the back wall
XB = "(Params.panel_depth + Params.panel_fit)"
xbo = xb + P["back_thickness"]  # back of the channel
XBO = "(Params.panel_depth + Params.panel_fit + Params.back_thickness)"
half = hw + P["ear_thickness"]  # half the width of the stand
HALF = "(%s + Params.ear_thickness)" % HW
# Height of the bottom edge of the panel above the table: the back corner of the floor, the lowest
# point of the channel, lies on the plate
h = P["base_thickness"] + xbo * math.sin(tilt) + P["floor_thickness"] * math.cos(tilt)
H = "(Params.base_thickness + %s * sin(Params.tilt) + Params.floor_thickness * cos(Params.tilt))" % XBO
# The outline of the channel reaches this far below its floor, through the plate; what comes below
# the table is cut off. Enough for a tilt up to 45 degrees.
deep = P["floor_thickness"] + xbo + P["lip_thickness"] + 2 * P["base_thickness"]
DEEP = "(Params.floor_thickness + %s + Params.lip_thickness + 2 * Params.base_thickness)" % XBO


def tilted_sketch(body, name, z, z_expression):
    """A sketch in the panel's frame, across at z: its origin on the bottom edge of the front of the
    panel, turned back by the tilt."""
    sketch = new_sketch(body, name, "XY_Plane")
    sketch.AttachmentOffset = App.Placement(V(0, h, z), App.Rotation(V(0, 0, -1), P["tilt"]))
    sketch.setExpression("AttachmentOffset.Base.y", H)
    sketch.setExpression("AttachmentOffset.Base.z", z_expression)
    sketch.setExpression("AttachmentOffset.Rotation.Angle", "Params.tilt")
    return sketch


doc = App.newDocument("stand128")
make_params(doc, PARAMS)

stand = doc.addObject("PartDesign::Body", "Stand")
lip_t, floor_t, lip_h, back_h = P["lip_thickness"], P["floor_thickness"], P["lip_height"], P["back_height"]
# The channel: lip, floor and back wall, the floor filled down into the plate
profile = tilted_sketch(stand, "ChannelProfile", 0, "0 mm")
pinned_polygon(profile, [(-lip_t, -deep, "Params.lip_thickness", DEEP),
                         (xbo, -deep, XBO, DEEP),
                         (xbo, back_h, XBO, "Params.back_height"),
                         (xb, back_h, XB, "Params.back_height"),
                         (xb, 0, XB, None),
                         (0, 0, None, None),
                         (0, lip_h, None, "Params.lip_height"),
                         (-lip_t, lip_h, "Params.lip_thickness", "Params.lip_height")])
pad(stand, "Channel", profile, "2 * " + HW, symmetric=True)
# The ears: the same outline under the panel, and a top that slopes up from the front to the top of
# the back wall
for side, sign in (("Right", 1), ("Left", -1)):
    ear = tilted_sketch(stand, "Ear%sSketch" % side, sign * hw, ("" if sign > 0 else "-") + HW)
    pinned_polygon(ear, [(-lip_t, -deep, "Params.lip_thickness", DEEP),
                         (xbo, -deep, XBO, DEEP),
                         (xbo, back_h, XBO, "Params.back_height"),
                         (-lip_t, P["ear_front_height"], "Params.lip_thickness", "Params.ear_front_height")])
    pad(stand, "Ear" + side, ear, "Params.ear_thickness", reversed_=sign < 0)
primitive(stand, "AdditiveBox", "Plate",
          {"Length": (P["base_front"] + P["base_back"], "Params.base_front + Params.base_back"),
           "Width": (P["base_thickness"], "Params.base_thickness"), "Height": (2 * half, "2 * " + HALF)},
          [(-P["base_front"], "-Params.base_front"), (0, None), (-half, "-" + HALF)])
# what reaches below the table
primitive(stand, "SubtractiveBox", "BelowTable",
          {"Length": (P["base_front"] + P["base_back"] + 100, "Params.base_front + Params.base_back + 100 mm"),
           "Width": (100, None), "Height": (2 * half + 2, "2 * %s + 2 mm" % HALF)},
          [(-P["base_front"] - 50, "-Params.base_front - 50 mm"), (-100, None), (-half - 1, "-%s - 1 mm" % HALF)])

# The name, sunk into the plate in front of the panel and readable from the front: the letters run
# to the right (z), their tops towards the panel (x), facing up (y)
letters = Draft.make_shapestring(TEXT, font(), P["text_size"])
letters.Label = "Text"
letters.Justification = "Middle-Center"
letters.setExpression("Size", "Params.text_size")
letters.Placement = App.Placement(V(-P["base_front"] + P["text_margin"] + P["text_size"] / 2, P["base_thickness"], 0),
                                  App.Rotation(App.Matrix(0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1)))
letters.setExpression("Placement.Base.x", "-Params.base_front + Params.text_margin + Params.text_size / 2")
letters.setExpression("Placement.Base.y", "Params.base_thickness")
stand.addObject(letters)
sunk = stand.newObject("PartDesign::Pocket", "TextCut")
sunk.Profile = letters
sunk.setExpression("Length", "Params.text_depth")

doc.recompute()
check_built(doc)

###########################
# The halves, for the Ender
###########################

shape = stand.Shape
# The joint goes across in the widest gap between the letters: the space between the words
spans = sorted((face.BoundBox.ZMin, face.BoundBox.ZMax) for face in letters.Shape.Faces)
gaps, reach = [], spans[0][1]
for low, high in spans[1:]:
    if low > reach:
        gaps.append((low - reach, (low + reach) / 2))
    reach = max(reach, high)
joint = max(gaps)[1] if gaps else 0
# Dovetails from the left half into the right one, where there is only the plate: between the
# letters and the channel, and behind the channel; 2 mm clear of them and of the edges
above = shape.common(Part.makeBox(1000, 1000, 40, V(-500, P["base_thickness"] + 0.01, joint - 20))).BoundBox
neck, head, length = P["dovetail_neck"], P["dovetail_head"], P["dovetail_length"]
tails = []
for start, end in ((letters.Shape.BoundBox.XMax + 2, above.XMin - 2), (above.XMax + 2, P["base_back"] - 2)):
    n = int((end - start + head) // (2 * head))  # as many as fit, a dovetail wide apart
    tails += [start + (end - start) * (i + 0.5) / n for i in range(n)]
# The left half: everything left of the joint, with the dovetails, through the whole height
outline = [(-1000, joint)]
for x in tails:
    outline += [(x - neck / 2, joint), (x - head / 2, joint + length), (x + head / 2, joint + length),
                (x + neck / 2, joint)]
outline += [(1000, joint), (1000, -1000), (-1000, -1000)]
left_face = Part.Face(Part.makePolygon([V(x, -1, z) for x, z in outline + outline[:1]]))
tall = V(0, shape.BoundBox.YMax + 2, 0)
left = shape.common(left_face.extrude(tall)).removeSplitter()
right = shape.cut(left_face.makeOffset2D(P["joint_fit"], 2).extrude(tall)).removeSplitter()
for name, part in (("LeftHalf", left), ("RightHalf", right)):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = part
    obj.Label2 = "For the Ender: made by build_stand128.py from the Stand, not updated by a change in Params"
print("joint %.1f mm %s of the middle, dovetails at %s mm" % (abs(joint), "right" if joint >= 0 else "left",
                                                              ", ".join("%.0f" % x for x in tails)), flush=True)

doc.recompute()
doc.saveAs(os.path.join(HERE, "stand128.FCStd"))
# printed lying on the plate
for name, part, stl in (("Stand", shape, "stand128.stl"), ("LeftHalf", left, "stand128_left.stl"),
                        ("RightHalf", right, "stand128_right.stl")):
    write_stl(name, part, os.path.join(HERE, stl), V(1, 0, 0), 90)
