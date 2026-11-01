# Stand for the 128 x 128 LED panel
# by Jeroen Verspeek
#
# The panel (128 x 128, P1.875, 240 x 240 mm) leans back at a fixed angle, 15
# degrees from upright (75 degrees to the table), in a stand made in one
# piece. Like the cradle of the 64 x 64 stand (../stand64/build_stand64.py) it has a
# channel over the full width that the bottom edge of the panel stands in: a
# floor, a low lip in front and a back wall up the back of the panel, with an
# ear at both ends. Here the channel does not turn on a hinge: it is built
# tilted onto the base plate, the space under its floor filled down to the
# plate, so it prints without support. The name is sunk into the plate in
# front of the panel. Behind the channel the 48 -> 5 V converter is screwed
# through the four U-shaped slots in its flanges onto four posts on the
# plate, in the middle, with room at both ends for the wires of its terminals.
# Two M3 screws through the back wall go into the two outer brass inserts of
# the bottom edge of the panel, so a touch does not push it out of the channel.
#
# The stand is 249 mm wide: in one piece on the Bambu Lab X2D (256 x 256 mm),
# in two halves on the Ender 3 v2, glued. The joint goes across between the
# words of the name; dovetails in the plate, in front of and behind the
# channel, hold the halves in line, and one half slides down onto the other.
#
# Holder: a plate flat on the back of the panel, on three M3 screws in the
# brass inserts, with the panel standing with the arrows on its back up. The
# rounded back of the USB speaker sinks through a hole in the plate into the
# opening left by the pushed-out middle rectangle, and a cable tie over its
# grille pulls it into that hole. The Pi with its hat stands on four posts to
# the right of it seen from the back, USB ports down and USB power to the left,
# the micro:bit on four posts to the left, USB edge down.
# Both connector openings stay free. Prints lying on its plate.
#
# Run:  freecadcmd build_stand128.py   (or ./build.sh 128)
# Writes stand128.FCStd (the stand and the holder parametric: change values in
# the Params spreadsheet; the halves made from the stand as plain shapes) and
# stand128.stl (one piece), stand128_left.stl and stand128_right.stl (the
# halves) and holder128.stl for the slicer.
###########################

import math
import os
import sys

import Draft
import FreeCAD as App
import Part

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))  # stand_lib.py
from stand_lib import check_built, font, make_params, new_sketch, pad, pinned_polygon, primitive, write_stl  # noqa: E402

V = App.Vector

TEXT = "Led Tetragon"  # on the base

# alias, value in mm (or in the unit given), meaning
PARAMS = [
    ("panel_size", 240, "Edge of the LED panel (128 x P1.875; measured 24 x 24 cm)"),
    ("panel_depth", 14.4, "Panel, front of the LEDs to the flat back of its plastic shell, as it stands (measured): "
                          "14 with the opening of 0.4 between board and shell pressed shut"),
    ("panel_fit", 0.5, "Play round the panel in the channel: behind it and at both sides"),
    ("tilt", 15, "How far the panel leans back from upright: 15 degrees is 75 degrees to the table", "deg"),
    ("lip_height", 0.5, "Height of the lip in front of the panel; the bottom row of LEDs lies from 0.1 to 1.7 above "
                        "the edge, its middle at 0.94. More than 0"),
    ("lip_thickness", 2, "Thickness of that lip"),
    ("floor_thickness", 4, "Thickness of the floor of the channel, under the panel"),
    ("back_height", 28, "How far the back wall reaches up the back of the panel; the connectors start 47 from an "
                        "edge"),
    ("back_thickness", 4, "Thickness of the back wall"),
    ("panel_screw_d", 4, "Holes in the back wall for the two M3 screws into the panel: wide, as printed holes come "
                         "out small and the inserts are only measured from a photo"),
    ("panel_screw_along", 39, "Those holes, at the two outer inserts of the bottom edge: from the ends of that edge"),
    ("ear_thickness", 4, "Thickness of the ears at both ends of the channel, which keep the panel in the middle"),
    ("ear_front_height", 16, "Height of an ear at its front, beside the panel; its top slopes up from there to the "
                             "top of the back wall"),
    ("base_thickness", 5, "Thickness of the base plate, and of the dovetails in it"),
    ("base_front", 40, "How far the base reaches in front of the bottom edge of the panel"),
    ("base_back", 100, "How far the base reaches behind it, past the converter"),
    ("text_size", 10, "Height of the letters on the base"),
    ("text_depth", 0.8, "How deep the letters are sunk into the base"),
    ("text_margin", 7, "Front edge of the base to the letters"),
    ("dovetail_neck", 8, "The halves for the Ender: width of a dovetail where it leaves its half"),
    ("dovetail_head", 12, "Width of a dovetail at its end"),
    ("dovetail_length", 8, "How far a dovetail reaches into the other half"),
    ("joint_fit", 0.15, "Play all round the joint between the halves, for the glue"),
    ("converter_length", 110, "48 -> 5 V converter (WGI20-48S05L): length with its flanges, across the stand, its "
                              "middle over the middle of the stand"),
    ("converter_width", 70, "Its width with its fins, from front to back"),
    ("converter_height", 23, "Its height with its flange (only used for checking)"),
    ("converter_body", 94, "Length of its body, without the flanges (from the drawing; only used for checking)"),
    ("flange_width", 55, "Width of the flange at both ends (from the drawing; only used for checking)"),
    ("flange_thickness", 2.4, "Thickness of the flange (from the drawing; only used for checking)"),
    ("converter_front", 27, "The front of its fins: how far behind the bottom edge of the panel"),
    ("mount_across", 39.5, "The U-shaped slots in its flanges: from front to back (from the drawing)"),
    ("mount_along", 102.1, "Those slots: from end to end, the screws 3.95 from the ends of the flanges "
                           "(100.6 scaled from the drawing was 1 to 1.5 short on the printed stand)"),
    ("mount_d", 3.8, "Width of those openings (only used for checking)"),
    ("converter_rest", 4, "Height of the posts under the converter, above the plate: air under it, and only the "
                          "posts touch it, as PLA softens near the 80 C its case may reach"),
    ("converter_post_d", 9, "Diameter of those posts"),
    # The holder. Places on the back of the panel as seen from the back, standing with the arrows up: u from the
    # left edge, v from the top edge. See ../PANEL.md (there seen as in the photos: v = from the left, u = 240 - from
    # the top).
    ("holder_plate", 3, "Thickness of the plate of the holder, flat against the back of the panel"),
    ("insert_edge", 10, "The brass inserts: from the edge of the panel"),
    ("insert_middle", 120, "The inserts in the middle of the left and the right side: from the top"),
    ("insert_top_u", 201, "The insert at the top that the holder uses: from the left"),
    ("pin_edge", 8.5, "The pins, at the left and the right side: from the edge"),
    ("pin_v", 89.5, "The pins: from the top"),
    ("pin_hole_d", 6, "Holes in the plate for the pins, which stay on the panel"),
    ("m3_d", 3.4, "Holes in the holder for its M3 screws"),
    ("m3_tap_d", 2.6, "Hole in a post that an M3 screw cuts its own thread in"),
    ("screw_slot", 2.5, "Two of the three holes for the screws are slots, this much longer each way than a hole: "
                        "they take up the difference between the panel and the print"),
    ("window_left", 90, "The opening of the middle rectangle, pushed out: from the left (only used for checking)"),
    ("window_right", 150, "Its right side: from the left (only used for checking)"),
    ("window_top", 79, "Its top: from the top (only used for checking)"),
    ("window_bottom", 162, "Its bottom: from the top (only used for checking)"),
    ("window_depth", 9, "How deep that opening is (guess; only used for checking)"),
    ("speaker_length", 84, "USB speaker: length of its flat grille face, a rectangle with half round ends"),
    ("speaker_height", 43, "Width of that face; the back of the body is half round of this diameter"),
    ("speaker_depth", 32, "Grille face to the lowest point of its rounded back"),
    ("speaker_u", 109, "Middle of the speaker: from the left; left of the middle of the opening, so its cable, on "
                       "the right, has room to bend"),
    ("speaker_v", 120.5, "Middle of the speaker: from the top"),
    ("speaker_sink", 10, "How far the back of the speaker sinks below the top of the plate; the hole in the plate is "
                         "as wide as the body is at that height"),
    ("speaker_cable_at", 31, "Speaker's cable: leaves its rounded back this far from the bottom end, to the right"),
    ("cable_slot", 8, "Width of the slot in the plate for the speaker's cable"),
    ("band_width", 6, "Width of the channel in an eye for the cable tie over the grille"),
    ("eye_side", 3, "Eyes for the cable tie: material at both sides of the channel"),
    ("eye_length", 4, "Eyes for the cable tie: length of the channel"),
    ("eye_gap", 2.5, "Eyes for the cable tie: height of the channel"),
    ("eye_roof", 2.5, "Eyes for the cable tie: thickness of the bar over the channel"),
    ("pi_left", 160, "Pi with its hat: from the left to its nearest part, on the side of the USB power port"),
    ("pi_bottom", 122, "Pi: from the top to the end of its USB ports, which point down"),
    ("pi_rest", 5, "Height of the posts the Pi stands on, above the plate: clear of the solder under it"),
    ("pi_post_d", 7, "Diameter of those posts"),
    ("pi_tap_d", 2.2, "Hole in those posts: an M2.5 screw cuts its own thread in it"),
    ("pi_hole_left", 3.5, "The Pi's board: from the left side of the Pi with its hat"),
    ("pi_hole_inset", 3.5, "The Pi's holes: from the edges of its board"),
    ("pi_hole_across", 49, "The Pi's holes: across"),
    ("pi_hole_along", 58, "The Pi's holes: along, from the end without the USB ports"),
    ("pi_length", 85, "Length of the Pi's board; its USB ports stick out 3 past it"),
    ("microbit_width", 51.6, "micro:bit V2: width, the edge with the USB port, here at the bottom"),
    ("microbit_height", 42, "Height of the micro:bit"),
    ("microbit_board", 1.6, "Thickness of the micro:bit's board (guess, 1.3 to 1.9 in the photos)"),
    ("microbit_left", 30, "micro:bit: from the left to its side with ring 0"),
    ("microbit_top", 78, "micro:bit: from the top to its edge with the rings"),
    ("ring_from_edge", 6.55, "The micro:bit's rings 0 and GND: their middles from its edge with the rings"),
    ("ring_from_end", 4.1, "Rings 0 and GND: their middles from the ends of that edge"),
    ("microbit_rest", 6, "Height of the posts the micro:bit lies on, above the plate: clear of its buttons, and "
                         "an M3 x 10 screw through the board stays within the post and the plate"),
    ("ring_post_d", 7, "Diameter of the posts under rings 0 and GND"),
    ("ring_peg_d", 3.6, "Printed peg through ring 0 (a hole of 4 mm for a banana plug)"),
    ("ring_peg", 1.5, "How far that peg sticks out past the back of the board"),
    ("usb_rest_d", 5, "Diameter of the two posts under the USB edge"),
    ("usb_rest_at", 5, "Those posts: their middles from the ends of the USB edge, and 3 mm from that edge; "
                       "clear of the USB port's tabs in the middle"),
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

# The converter behind the channel: four posts on the plate, one under each U-shaped slot in
# its flanges, that an M3 screw cuts its own thread in. Only the posts touch it, so it may bridge the
# joint between the halves, which stays clear of them.
ALONG_Y = App.Rotation(V(1, 0, 0), -90)  # turns a cylinder from along z to along y
mid_x = P["converter_front"] + P["converter_width"] / 2
MID_X = "Params.converter_front + Params.converter_width / 2"
post_top = P["base_thickness"] + P["converter_rest"]
POST_TOP = "Params.base_thickness + Params.converter_rest"
for i, (front_back, side) in enumerate(((-1, -1), (-1, 1), (1, -1), (1, 1))):
    at_x = (mid_x + front_back * P["mount_across"] / 2,
            "%s %s Params.mount_across / 2" % (MID_X, "+" if front_back > 0 else "-"))
    at_z = (side * P["mount_along"] / 2, "%sParams.mount_along / 2" % ("" if side > 0 else "-"))
    primitive(stand, "AdditiveCylinder", "ConverterPost%d" % (i + 1),
              {"Radius": (P["converter_post_d"] / 2, "Params.converter_post_d / 2"),
               "Height": (P["converter_rest"], "Params.converter_rest")},
              [at_x, (P["base_thickness"], "Params.base_thickness"), at_z], ALONG_Y)
    primitive(stand, "SubtractiveCylinder", "ConverterTap%d" % (i + 1),
              {"Radius": (P["m3_tap_d"] / 2, "Params.m3_tap_d / 2"), "Height": (post_top - 0.5, POST_TOP + " - 0.5 mm")},
              [at_x, (0.5, "0.5 mm"), at_z], ALONG_Y)

# Two holes through the back wall, square to it, for the screws that hold the panel: at the two outer
# inserts of its bottom edge, left and right of the converter
ACROSS_WALL = App.Rotation(V(0, 0, -1), P["tilt"]).multiply(App.Rotation(V(0, 1, 0), 90))
for i, side in enumerate((-1, 1)):
    z = P["panel_size"] / 2 - P["panel_screw_along"]
    across, up = xb - 1, P["insert_edge"]
    primitive(stand, "SubtractiveCylinder", "PanelScrew%d" % (i + 1),
              {"Radius": (P["panel_screw_d"] / 2, "Params.panel_screw_d / 2"),
               "Height": (P["back_thickness"] + 2, "Params.back_thickness + 2 mm")},
              [(across * math.cos(tilt) + up * math.sin(tilt),
                "(%s - 1 mm) * cos(Params.tilt) + Params.insert_edge * sin(Params.tilt)" % XB),
               (h - across * math.sin(tilt) + up * math.cos(tilt),
                "%s - (%s - 1 mm) * sin(Params.tilt) + Params.insert_edge * cos(Params.tilt)" % (H, XB)),
               (side * z, "%s(Params.panel_size / 2 - Params.panel_screw_along)" % ("" if side > 0 else "-"))],
              ACROSS_WALL)

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

###########################
# Holder on the back of the panel
###########################

# Modelled in the panel's frame like the channel: x backwards from the front of the panel, y up from
# its bottom edge, z across. Places on the back are given as seen from the back: u from the left, v
# from the top; so y = panel_size - v and z = panel_size / 2 - u.
size = P["panel_size"]
ALONG_X = App.Rotation(V(0, 1, 0), 90)  # turns a cylinder from along z to along x


def mm(value, expression=None):
    """A length with its spreadsheet expression; a plain number gets one of its own."""
    return value, expression or "%g mm" % value


def par(alias):
    return mm(P[alias], "Params." + alias)


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


holder = doc.addObject("PartDesign::Body", "Holder")
BACK = par("panel_depth")  # the back of the panel
TOP = add(BACK, par("holder_plate"))  # the top of the plate
THROUGH = (add(BACK, mm(1), -1), add(TOP, mm(1)))
PLATE = (BACK, TOP)
# The plate, along the middle of the back, past both connector openings. To the left for the
# micro:bit, in the middle round the speaker, to the right for the Pi, and up to the screw at the top
region(holder, "AdditiveBox", "PlateLeft", PLATE, (mm(1), mm(90)), (mm(72), mm(128)))
region(holder, "AdditiveBox", "PlateMiddle", PLATE, (mm(80), mm(140)), (mm(72), mm(168)))
region(holder, "AdditiveBox", "PlateRight", PLATE, (mm(130), add(par("panel_size"), mm(1), -1)), (mm(72), mm(129)))
pi_u0 = add(add(par("pi_left"), par("pi_hole_left")), par("pi_hole_inset"))  # left holes of the Pi
pi_u1 = add(pi_u0, par("pi_hole_across"))
# the top holes, near the end of the board without the USB ports, which stick out 3 past it
pi_v0 = add(add(add(par("pi_bottom"), mm(3), -1), par("pi_length"), -1), par("pi_hole_inset"))
pi_v1 = add(pi_v0, par("pi_hole_along"))
top_u = par("insert_top_u")
region(holder, "AdditiveBox", "PlateArm", PLATE, (mm(153), add(pi_u1, mm(5))), (add(pi_v0, mm(10), -1), mm(73)))
region(holder, "AdditiveBox", "PlateStrip", PLATE, (add(top_u, mm(6), -1), add(top_u, mm(6))), (mm(4), mm(57)))

# The hole for the speaker: as wide as its rounded back is at the top of the plate, a half round at
# both ends, like the body. The back rests on the edge of the hole.
su, sv = par("speaker_u"), par("speaker_v")
radius = P["speaker_height"] / 2
RADIUS = "Params.speaker_height / 2"
seat = mm(math.sqrt(radius ** 2 - (radius - P["speaker_sink"]) ** 2),
          "sqrt((%s) ^ 2 - (%s - Params.speaker_sink) ^ 2)" % (RADIUS, RADIUS))
to_end = mm(P["speaker_length"] / 2 - radius, "Params.speaker_length / 2 - " + RADIUS)
region(holder, "SubtractiveBox", "SpeakerHole", THROUGH, (add(su, seat, -1), add(su, seat)),
       (add(sv, to_end, -1), add(sv, to_end)))
for name, v in (("Top", add(sv, to_end, -1)), ("Bottom", add(sv, to_end))):
    post(holder, "SubtractiveCylinder", "SpeakerHole" + name, THROUGH, su, v, seat)
# a slot from that hole to the right, where the cable leaves the speaker's back
cable_v = mm(P["speaker_v"] + P["speaker_length"] / 2 - P["speaker_cable_at"],
             "Params.speaker_v + Params.speaker_length / 2 - Params.speaker_cable_at")
slot = mm(P["cable_slot"] / 2, "Params.cable_slot / 2")
region(holder, "SubtractiveBox", "CableSlot", THROUGH, (su, mm(142)), (add(cable_v, slot, -1), add(cable_v, slot)))
# An eye on both sides of the speaker, on the plate, at its middle: the cable tie goes through the
# channel and over the bar, and twice over the grille. The channel runs from left to right, so the
# bar prints as a short bridge.
just_clear = mm(radius + 1, RADIUS + " + 1 mm")
eye_half = add(mm(P["band_width"] / 2, "Params.band_width / 2"), par("eye_side"))
channel_half = mm(P["band_width"] / 2, "Params.band_width / 2")
eye_top = add(add(TOP, par("eye_gap")), par("eye_roof"))
for name, sign in (("Left", -1), ("Right", 1)):
    near, far = add(su, just_clear, sign), add(add(su, just_clear, sign), par("eye_length"), sign)
    us = (near, far)[::sign]
    region(holder, "AdditiveBox", "Eye" + name, (TOP, eye_top), us, (add(sv, eye_half, -1), add(sv, eye_half)))
    region(holder, "SubtractiveBox", "EyeChannel" + name, (TOP, add(TOP, par("eye_gap"))),
           (add(us[0], mm(1), -1), add(us[1], mm(1))), (add(sv, channel_half, -1), add(sv, channel_half)))

# The Pi on four posts; a hole through each that an M2.5 screw, or the thread of a spacer, goes in
pi_rest = add(TOP, par("pi_rest"))
for i, (u, v) in enumerate(((pi_u0, pi_v0), (pi_u1, pi_v0), (pi_u0, pi_v1), (pi_u1, pi_v1))):
    post(holder, "AdditiveCylinder", "PiPost%d" % (i + 1), (TOP, pi_rest), u, v,
         mm(P["pi_post_d"] / 2, "Params.pi_post_d / 2"))
    post(holder, "SubtractiveCylinder", "PiTap%d" % (i + 1), (add(BACK, mm(1), -1), add(pi_rest, mm(1))), u, v,
         mm(P["pi_tap_d"] / 2, "Params.pi_tap_d / 2"))

# The micro:bit, USB edge down and LEDs towards the panel, on four posts as on the 64 x 64: under the GND
# ring on the right one that a screw through the ring cuts its thread in, under ring 0 on the left one
# with a peg through the ring, and two under the USB edge
ml, mt = par("microbit_left"), par("microbit_top")
REST = add(TOP, par("microbit_rest"))
ring_v = add(mt, par("ring_from_edge"))
ring0_u = add(ml, par("ring_from_end"))
gnd_u = add(add(ml, par("microbit_width")), par("ring_from_end"), -1)
ring_post = mm(P["ring_post_d"] / 2, "Params.ring_post_d / 2")
post(holder, "AdditiveCylinder", "GndPost", (TOP, REST), gnd_u, ring_v, ring_post)
post(holder, "AdditiveCylinder", "Ring0Post", (TOP, REST), ring0_u, ring_v, ring_post)
peg_end = add(add(REST, par("microbit_board")), par("ring_peg"))
post(holder, "AdditiveCylinder", "Ring0Peg", (REST, peg_end), ring0_u, ring_v,
     mm(P["ring_peg_d"] / 2, "Params.ring_peg_d / 2"))
usb_v = add(add(mt, par("microbit_height")), mm(3), -1)
for i, u in enumerate((add(ml, par("usb_rest_at")), add(add(ml, par("microbit_width")), par("usb_rest_at"), -1))):
    post(holder, "AdditiveCylinder", "UsbRest%d" % (i + 1), (TOP, REST), u, usb_v,
         mm(P["usb_rest_d"] / 2, "Params.usb_rest_d / 2"))
post(holder, "SubtractiveCylinder", "GndScrewHole", (add(BACK, mm(1), -1), add(REST, mm(1))), gnd_u, ring_v,
     mm(P["m3_tap_d"] / 2, "Params.m3_tap_d / 2"))

# The screws: the one on the right goes in first and fixes the holder; the one on the left, 220 mm
# from it, is a slot from left to right, the one at the top a slot from top to bottom. Holes for the
# pins, which stay on the panel
M3 = mm(P["m3_d"] / 2, "Params.m3_d / 2")
SLOT = par("screw_slot")
edge, middle = par("insert_edge"), par("insert_middle")
post(holder, "SubtractiveCylinder", "RightScrewHole", THROUGH, add(par("panel_size"), edge, -1), middle, M3)
region(holder, "SubtractiveBox", "LeftScrewSlot", THROUGH, (add(edge, SLOT, -1), add(edge, SLOT)),
       (add(middle, M3, -1), add(middle, M3)))
region(holder, "SubtractiveBox", "TopScrewSlot", THROUGH, (add(top_u, M3, -1), add(top_u, M3)),
       (add(edge, SLOT, -1), add(edge, SLOT)))
for i, u in enumerate((add(edge, SLOT, -1), add(edge, SLOT))):
    post(holder, "SubtractiveCylinder", "LeftScrewSlotEnd%d" % (i + 1), THROUGH, u, middle, M3)
for i, v in enumerate((add(edge, SLOT, -1), add(edge, SLOT))):
    post(holder, "SubtractiveCylinder", "TopScrewSlotEnd%d" % (i + 1), THROUGH, top_u, v, M3)
pin_hole = mm(P["pin_hole_d"] / 2, "Params.pin_hole_d / 2")
post(holder, "SubtractiveCylinder", "PinHoleLeft", THROUGH, par("pin_edge"), par("pin_v"), pin_hole)
post(holder, "SubtractiveCylinder", "PinHoleRight", THROUGH, add(par("panel_size"), par("pin_edge"), -1), par("pin_v"),
     pin_hole)

doc.recompute()
check_built(doc)
doc.saveAs(os.path.join(HERE, "stand128.FCStd"))
# printed lying on the plate
for name, part, stl in (("Stand", shape, "stand128.stl"), ("LeftHalf", left, "stand128_left.stl"),
                        ("RightHalf", right, "stand128_right.stl")):
    write_stl(name, part, os.path.join(HERE, stl), V(1, 0, 0), 90)
write_stl("Holder", holder.Shape, os.path.join(HERE, "holder128.stl"), V(0, 1, 0), -90)  # lying on its plate
