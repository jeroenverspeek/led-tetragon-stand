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
# sunk flush into the cheek. The rings have a little play between the cheeks,
# so the cradle goes in; tightening the screw presses the cheek against the
# ring on the ear, and that friction holds the angle. The name is sunk into the
# plate in front of the panel.
#
# Holder: the USB speaker and the micro:bit on the back of the panel, in the
# left half seen from the back, beside the Pi; one part on three screws: the
# top left corner hole, the top hole of the middle bar and the middle hole of
# the left bar; the last two are slots, so the screws go in even when the
# print is a little off. At the top a plate with a cup for the rounded back
# of the speaker, grille facing backwards, with a lip along both long sides
# and a slot in the bottom for its cable. A band (a cable tie, rubber band or
# wire) loops round an eye on both long sides of the cup and over the middle
# of the grille, and presses the speaker in; notches at both ends let a
# screwdriver lever it out. The plate bridges the frame, so the power cable
# can run up under it. A strip down the left bar joins it to the plate for
# the micro:bit, upright and parallel to the panel, between the power
# connector and HUB75 IN, its LEDs towards the panel and its USB port towards
# the Pi. It lies on four posts, high enough for its buttons: one under the
# GND ring, with a screw through the ring into it; one under ring 0, with a
# printed peg through the ring; two under its USB edge.
# Prints lying on its plate.
#
# Needed: 1 x Base, 1 x Cradle, 1 x Holder; 2 x M5 x 12 countersunk screw,
# 2 x M5 nut, 4 x M3 x 10 screw, a cable tie or rubber band for the speaker.
#
# Run:  freecadcmd build_stand.py   (or ./build.sh)
# Writes stand.FCStd (parametric: change values in the Params spreadsheet)
# and an .stl per part for the slicer.
###########################

import math
import os
import sys

import Draft
import FreeCAD as App

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from stand_lib import check_built, font, make_params, new_sketch, pad, pinned_polygon, primitive, write_stl  # noqa: E402

V = App.Vector

TEXT = "Led Tetragon"  # on the base

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
    # The printed base came out with 1 mm in total between the rings and the cheeks, not 0.6; an M5 spring
    # washer at one end takes it up (see PANEL.md). A reprint without the washer needs less play; not tried.
    ("hinge_play", 0.3, "Space between each ring and its cheek, so the cradle goes in between the cheeks; "
                        "tightening the screw bends the cheek onto the ring"),
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
    ("cheek_thickness", 4.2, "Thickness of the two cheeks on the base, with the countersink in it"),
    ("cheek_width", 20, "Width of a cheek; its top is a half round of this diameter round the hinge axis"),
    ("text_size", 10, "Height of the letters on the base"),
    ("text_depth", 0.8, "How deep the letters are sunk into the base"),
    ("text_margin", 7, "Front edge of the base to the letters"),
    # The back of the panel, seen from the back with the panel standing: "from the left" and "from the top" are
    # from the edges of the panel. See PANEL.md.
    ("frame_bar_width", 16, "Width of the four bars round the edge of the frame, flush with its back"),
    ("middle_bar_width", 20, "Width of the vertical middle bar, flush with the back of the frame"),
    ("bar_hole_top", 9, "Top of the 4 M3 holes (brass inserts, evenly spaced) in the middle bar: from the top"),
    ("side_hole_left", 16, "Top left M3 hole, in the top bar: from the left"),
    ("side_hole_top", 8, "Top left M3 hole, in the top bar: from the top"),
    ("side_mid_hole_left", 8, "Middle M3 hole in the left bar: from the left"),
    ("side_mid_hole_top", 88.5, "Middle M3 hole in the left bar: from the top"),
    ("pi_from_left", 90, "Pi with its hat: from the left to its nearest part"),
    ("pi_from_right", 40, "Pi with its hat: from the right"),
    ("pi_from_top", 40, "Pi: from the top to its top, the USB ports"),
    ("hat_from_bottom", 39, "The hat, sticking out below the Pi: from the bottom"),
    ("pi_gap", 7, "Back of the frame to the solder under the Pi, whose board lies 10 mm behind it"),
    ("pi_depth", 30, "How far the Pi with its hat sticks out behind the frame"),
    ("m3_d", 3.4, "Holes in the holder for its M3 screws"),
    ("m3_tap_d", 2.6, "Hole in a post that an M3 screw cuts its own thread in"),
    ("screw_slot", 2.5, "The holder's holes in the middle bar and the left bar are slots, this much longer each way "
                      "than a hole: they take up the difference between the frame and the print"),
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
    ("band_at", 50, "A band over the middle of the speaker's grille holds it in its cup (a cable tie, rubber band or "
                    "wire): its middle, from the left, clear of the cable slot"),
    ("band_width", 6, "Width of the notches in the rim that the band presses the face through, and of the eyes on the "
                      "outside of the cup that it loops round"),
    ("band_gap", 2.5, "Eyes for the band: gap between the cup and the bar of an eye, that the band goes through"),
    ("eye_bar", 3, "Eyes for the band: thickness of the bar, and of the posts that hold it on both sides"),
    ("eye_height", 8, "Eyes for the band: height of the bar, along the side of the cup"),
    ("lever_notch", 8, "Notch in the rim at both round ends of the cup, for a screwdriver to lever the speaker out: "
                       "width"),
    ("lever_depth", 3, "How far those notches reach below the face of the speaker"),
    ("microbit_width", 51.6, "micro:bit V2: width, the edge with the USB port; upright in its holder"),
    ("microbit_height", 42, "Height of the micro:bit; across in its holder"),
    ("microbit_thickness", 11.65, "Thickness of the micro:bit with its parts on both sides"),
    ("microbit_board", 1.6, "Thickness of the micro:bit's board (guess, 1.3 to 1.9 in the photos)"),
    ("microbit_buttons", 4.2, "How far the buttons A and B stick out from the front of the micro:bit"),
    ("microbit_left", 14, "micro:bit: from the left to its edge with the rings, just past the screw in the left bar"),
    ("microbit_top", 88.65, "micro:bit: from the top, just below the power connector, so the HUB75 ribbon has room "
                            "below it"),
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
ci = out + P["ring_height"] + P["hinge_play"]  # inside of a cheek
CI = "(%s + Params.ring_height + Params.hinge_play)" % OUT
# The base is modelled as it stands: x backwards from the hinge axis, y across, z up from the table.
ph = P["base_thickness"] + P["base_gap"] + P["hinge_radius"]  # height of the hinge axis
PH = "(Params.base_thickness + Params.base_gap + Params.hinge_radius)"

ALONG_Y = App.Rotation(V(1, 0, 0), -90)  # turns a cylinder or prism from along z to along y
POINT_UP = App.Rotation(V(0, 0, 1), 30)  # turns a hex so that a corner, not a flat, points along y


def hexagon(body, kind, name, across_flats, af_expression, height, height_expression, at, turn):
    return primitive(body, kind, name, {"Polygon": (6, None),
                                        "Circumradius": (across_flats / math.sqrt(3), af_expression + " / sqrt(3)"),
                                        "Height": (height, height_expression)}, at, turn)


doc = App.newDocument("stand")

make_params(doc, PARAMS)

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
letters = Draft.make_shapestring(TEXT, font(), P["text_size"])
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
# The band: it crosses the face in a notch in the rim on both long sides, 1 mm below the face so it
# presses the speaker onto the plate, and loops round the bar of an eye on the outside of the cup,
# 2 mm below the notch. The underside of an eye slopes at 45 degrees, so it prints without support.
band_u = mm(P["band_at"], "Params.band_at")
band_half = mm(P["band_width"] / 2, "Params.band_width / 2")
bar = mm(P["eye_bar"], "Params.eye_bar")
gap = mm(P["band_gap"], "Params.band_gap")
reach = add(gap, bar)  # how far an eye stands out from the cup
notch = add(lips, mm(1), -1)  # bottom of a notch
eye_top = add(notch, mm(2), -1)
eye_bottom = add(eye_top, mm(P["eye_height"], "Params.eye_height"), -1)
lip = mm(P["cup_lip_width"], "Params.cup_lip_width")


def xy(x, v):
    """A corner in the XY plane: x backwards, v from the top."""
    return x[0], size - v[0], x[1], "Params.panel_size - (%s)" % v[1]


for side, sign in (("Top", -1), ("Bottom", 1)):
    wall = add(middle, r_out, sign)  # outside of the cup
    inside = add(wall, mm(P["holder_wall"] / 2, "Params.holder_wall / 2"), -sign)
    outside = add(wall, reach, sign)
    eye = new_sketch(holder, "Eye%sSketch" % side, "XY_Plane", size / 2 - P["band_at"],
                     "Params.panel_size / 2 - Params.band_at")
    pinned_polygon(eye, [xy(eye_top, inside), xy(add(eye_bottom, reach, -1), inside),
                         xy(add(eye_bottom, reach, -1), wall), xy(eye_bottom, outside), xy(eye_top, outside)])
    pad(holder, "Eye" + side, eye, "Params.band_width + 2 * Params.eye_bar", symmetric=True)
    channel = (wall, add(wall, gap, sign))[::sign]
    region(holder, "SubtractiveBox", "Eye%sChannel" % side, (add(add(eye_bottom, reach, -1), mm(1), -1), add(eye_top, mm(1))),
           (add(band_u, band_half, -1), add(band_u, band_half)), channel)
    lips_edge = add(add(middle, r_in, sign), lip, -sign)  # inner edge of the lip on this side
    region(holder, "SubtractiveBox", "BandNotch" + side, (notch, add(rim, mm(1))),
           (add(band_u, band_half, -1), add(band_u, band_half)),
           (add(wall, mm(1), sign), add(lips_edge, mm(1), -sign))[::-sign])
# notches at both round ends, for a screwdriver to go in beside the speaker and lever it out
lever = mm(P["lever_notch"] / 2, "Params.lever_notch / 2")
for side, end, sign in (("Left", ends[0], -1), ("Right", ends[1], 1)):
    region(holder, "SubtractiveBox", "LeverNotch" + side,
           (add(lips, mm(P["lever_depth"], "Params.lever_depth"), -1), add(rim, mm(1))),
           (add(add(end, r_out, sign), mm(1), sign), add(add(end, r_in, sign), mm(1), -sign))[::-sign],
           (add(middle, lever, -1), add(middle, lever)))
# where the Pi comes close, only the plate and the rim of the cup stay
region(holder, "SubtractiveBox", "PiClearance",
       (add(D, mm(P["pi_gap"] - 1, "Params.pi_gap - 1 mm")), add(D, mm(P["pi_depth"] + 1, "Params.pi_depth + 1 mm"))),
       (mm(P["pi_from_left"] - 1, "Params.pi_from_left - 1 mm"), mm(size, "Params.panel_size")),
       (mm(P["pi_from_top"] - 1, "Params.pi_from_top - 1 mm"), mm(size, "Params.panel_size")))
# the screw in the top left corner goes in first and fixes the holder; the hole in the middle bar,
# 80 mm to the right of it, is a slot from left to right
THROUGH = (add(D, mm(1), -1), add(PLATE, mm(1)))
SLOT = mm(P["screw_slot"], "Params.screw_slot")
post(holder, "SubtractiveCylinder", "SideScrewHole", THROUGH, mm(P["side_hole_left"], "Params.side_hole_left"),
     mm(P["side_hole_top"], "Params.side_hole_top"), M3)
bar_u = mm(size / 2, "Params.panel_size / 2")
stadium(holder, "SubtractiveBox", "BarScrewSlot", THROUGH, (add(bar_u, SLOT, -1), add(bar_u, SLOT)),
        mm(P["bar_hole_top"], "Params.bar_hole_top"), M3)

# The micro:bit below it, upright, its USB edge towards the Pi and its LEDs towards the panel, on four
# posts clear of its buttons: under the GND ring at the top a post that a screw through the ring cuts
# its thread in, under ring 0 at the bottom one with a peg through the ring, and two under the USB edge
ml = mm(P["microbit_left"], "Params.microbit_left")
mt = mm(P["microbit_top"], "Params.microbit_top")
across = mm(P["microbit_height"], "Params.microbit_height")
down = mm(P["microbit_width"], "Params.microbit_width")
outer_u = (add(ml, WALL, -1), add(add(ml, across), WALL))
outer_v = (add(mt, WALL, -1), add(add(mt, down), WALL))
region(holder, "AdditiveBox", "MicrobitPlate", (D, PLATE), (mm(1), outer_u[1]), outer_v)
screw_u = mm(P["side_mid_hole_left"], "Params.side_mid_hole_left")
screw_v = mm(P["side_mid_hole_top"], "Params.side_mid_hole_top")
# a strip down the left bar joins it to the plate of the speaker, past the middle hole of that bar
region(holder, "AdditiveBox", "LeftStrip", (D, PLATE), (mm(1), outer_u[0]), (middle, add(outer_v[0], mm(1))))
REST = add(PLATE, mm(P["microbit_rest"], "Params.microbit_rest"))  # front of the micro:bit's board
ring_u = add(ml, mm(P["ring_from_edge"], "Params.ring_from_edge"))
ring_end = mm(P["ring_from_end"], "Params.ring_from_end")
gnd_v, ring0_v = add(mt, ring_end), add(add(mt, down), ring_end, -1)
ring_post = mm(P["ring_post_d"] / 2, "Params.ring_post_d / 2")
post(holder, "AdditiveCylinder", "GndPost", (PLATE, REST), ring_u, gnd_v, ring_post)
post(holder, "AdditiveCylinder", "Ring0Post", (PLATE, REST), ring_u, ring0_v, ring_post)
peg_end = add(add(REST, mm(P["microbit_board"], "Params.microbit_board")), mm(P["ring_peg"], "Params.ring_peg"))
post(holder, "AdditiveCylinder", "Ring0Peg", (REST, peg_end), ring_u, ring0_v,
     mm(P["ring_peg_d"] / 2, "Params.ring_peg_d / 2"))
usb_u = add(add(ml, across), mm(3), -1)
usb_at = mm(P["usb_rest_at"], "Params.usb_rest_at")
for i, v in enumerate((add(mt, usb_at), add(add(mt, down), usb_at, -1))):
    post(holder, "AdditiveCylinder", "UsbRest%d" % (i + 1), (PLATE, REST), usb_u, v,
         mm(P["usb_rest_d"] / 2, "Params.usb_rest_d / 2"))
post(holder, "SubtractiveCylinder", "GndScrewHole", (add(D, mm(1), -1), add(REST, mm(1))), ring_u, gnd_v,
     mm(P["m3_tap_d"] / 2, "Params.m3_tap_d / 2"))
# the hole in the left bar, 80 mm below the corner, is a slot from top to bottom
slot_v = (add(screw_v, SLOT, -1), add(screw_v, SLOT))
region(holder, "SubtractiveBox", "LeftScrewSlot", THROUGH, (add(screw_u, M3, -1), add(screw_u, M3)), slot_v)
for i, v in enumerate(slot_v):
    post(holder, "SubtractiveCylinder", "LeftScrewSlotEnd%d" % (i + 1), THROUGH, screw_u, v, M3)

doc.recompute()

check_built(doc)
doc.saveAs(os.path.join(HERE, "stand.FCStd"))
write_stl("Base", base.Shape, os.path.join(HERE, "base.stl"))
write_stl("Cradle", cradle.Shape, os.path.join(HERE, "cradle.stl"), V(1, 0, 0), 90)  # lying on its floor
write_stl("Holder", holder.Shape, os.path.join(HERE, "holder.stl"), V(0, 1, 0), -90)  # lying on its plate
