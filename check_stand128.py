# Check of the stand for the 128 x 128 LED panel
# by Jeroen Verspeek
#
# Opens stand128.FCStd, puts the panel in the channel and checks that it fits,
# that the stand does not tip over, that the halves for the Ender fit together
# and that the stand fits the X2D and the halves the Ender; and puts the Pi, the
# speaker and the micro:bit on the holder and checks those and their plugs.
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
# Only used for the balance: the panel (weighed), the Pi with its hat and cables (a guess, as on
# the 64 x 64), the speaker and the micro:bit (from PANEL.md)
PANEL_MASS = 527  # g
PI_MASS = 120  # g
SPEAKER_MASS = 74  # g
MICROBIT_MASS = 10  # g
CONVERTER_MASS = 228  # g, weighed
TIP_MARGIN = 15  # mm, the centre of mass stays at least this far inside the base
PREVIEW_TEXT = ("Hello", "world")  # each dot of the font 4 x 4 LEDs
LEDS = 128  # LEDs along an edge of the panel
CONNECTORS = 47  # mm, the openings for the connectors lie at least this far from every edge (see PANEL.md)
# What stands on the holder, and its plugs, as on the 64 x 64: see the notes in check_stand.py and
# PANEL.md. Seen from the back with the arrows up: u from the left, v from the top; x behind the
# back of the panel.
PI_WIDTH = 62  # the Pi with its hat, across
PI_REACH = 113  # from its USB ports to the end of the hat
PI_STACK = 20  # the Pi's board to the top of the parts on the hat (from the 64 x 64: 10 to 30)
HAT_BOARD = 9.4  # the Pi's board to the hat's (19.4 and 10 on the 64 x 64)
SOLDER = 3  # under the Pi (guess)
USB_PORTS_FROM_LEFT = (9, 27)  # the Pi turned half round from the 64 x 64: USB ports down, USB-C to the left
USB_PLUG = (16, 8, 25)  # across, thick, long
USB_PORT_ABOVE_BOARD = 5
USB_C_FROM_END = 11.2  # from the end of the Pi's board without the USB ports
USB_C_PLUG = (12, 7, 25)
USB_C_ABOVE_BOARD = 3.3
# The cables, as on the 64 x 64: stiff, about 4 thick, straight out of the plugs for 10 (guess), then a
# bend of radius 30 over backwards
CABLE = 4
CABLE_OUT = 10
CABLE_BEND = 30
MICROBIT_BEHIND = 6.7  # parts behind the micro:bit's board
BUTTONS = 4.2  # in front of the micro:bit's board
MICROBIT_PLUG = (11, 8, 40)
USB_PORT_BEHIND = 1.5
M3_HEAD = (5.5, 3)  # diameter, height
# The screws of the converter: M3 x 10 with a small washer (DIN 433: 6 across, 0.5 thick)
CONVERTER_SCREW = 10
WASHER = (6, 0.5)
# The plugs on the panel, the only ones that matter being those in use: a HUB75 plug is 2 mm bigger
# all round than its header and 12 high, a power plug 8 high (from the 64 x 64)
HUB75_US = (93, 125)
POWER_US = (126.5, 142)
PLUG_VS = ((53.5, 66.5), (173.5, 186.5))
HUB75_HIGH = 12
POWER_HIGH = 8

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
panel_alone = Part.makeBox(DEPTH, SIZE, SIZE, V(0, 0, -SIZE / 2))  # in the panel's own frame, as the holder
panel = placed(panel_alone, spot)
holder = doc.getObject("Holder").Shape
PLATE = p["holder_plate"]


def back(us, vs, xs):
    """A box on the back of the panel: u from the left and v from the top as seen from the back, x
    behind the back of the panel."""
    return Part.makeBox(xs[1] - xs[0], vs[1] - vs[0], us[1] - us[0], V(DEPTH + xs[0], SIZE - vs[1], SIZE / 2 - us[1]))


def post(u, v, xs, radius):
    return Part.makeCylinder(radius, xs[1] - xs[0], V(DEPTH + xs[0], SIZE - v, SIZE / 2 - u), V(1, 0, 0))


# The speaker: a flat face with half round ends, a straight part behind it, and a rounded back: half a
# cylinder with half a ball at both ends (from the photos). It rests on the edge of the hole in the plate.
su, sv, sr, sl = p["speaker_u"], p["speaker_v"], p["speaker_height"] / 2, p["speaker_length"]
s_low = PLATE - p["speaker_sink"]  # the lowest point of its back
s_axis, s_face = s_low + sr, s_low + p["speaker_depth"]
s_ends = (sv - sl / 2 + sr, sv + sl / 2 - sr)
speaker = back((su - sr, su + sr), s_ends, (s_axis, s_face))
speaker = speaker.fuse(Part.makeCylinder(sr, s_ends[1] - s_ends[0], V(DEPTH + s_axis, SIZE - s_ends[1], SIZE / 2 - su),
                                         V(0, 1, 0)))
for v in s_ends:
    speaker = speaker.fuse(post(su, v, (s_axis, s_face), sr))
    speaker = speaker.fuse(Part.makeSphere(sr, V(DEPTH + s_axis, SIZE - v, SIZE / 2 - su)))
speaker = speaker.cut(back((0, SIZE), (0, SIZE), (s_face, s_face + 50))).removeSplitter()
window = back((p["window_left"], p["window_right"]), (p["window_top"], p["window_bottom"]), (-p["window_depth"], 0))

# The Pi with its hat, on its posts
pl, pb, rest = p["pi_left"], p["pi_bottom"], PLATE + p["pi_rest"]
pi_us = (pl, pl + PI_WIDTH)
pi_end = pb - 3 - p["pi_length"]  # the end of its board without the USB ports
pi_board = back(pi_us, (pi_end, pb), (rest, rest + PI_STACK))
hat = back(pi_us, (pb - PI_REACH, pi_end), (rest + HAT_BOARD, rest + PI_STACK))
pi = pi_board.fuse(hat).removeSplitter()

# The micro:bit on its posts
ml, mt, mw, mh = p["microbit_left"], p["microbit_top"], p["microbit_width"], p["microbit_height"]
mx = PLATE + p["microbit_rest"]
microbit = back((ml, ml + mw), (mt, mt + mh), (mx, mx + p["microbit_board"] + MICROBIT_BEHIND))
ring_v = mt + p["ring_from_edge"]
microbit = microbit.cut(post(ml + p["ring_from_end"], ring_v, (mx - 1, mx + 20), 2.025))

# The plugs in the Pi, in the micro:bit and on the panel
usb_x = rest + USB_PORT_ABOVE_BOARD
usb_plugs = [back((pl + at - USB_PLUG[0] / 2, pl + at + USB_PLUG[0] / 2), (pb, pb + USB_PLUG[2]),
                  (usb_x - USB_PLUG[1] / 2, usb_x + USB_PLUG[1] / 2)) for at in USB_PORTS_FROM_LEFT]
usb_c_x = rest + USB_C_ABOVE_BOARD
usb_c_v = pi_end + USB_C_FROM_END
usb_c = back((pl - USB_C_PLUG[2], pl), (usb_c_v - USB_C_PLUG[0] / 2, usb_c_v + USB_C_PLUG[0] / 2),
             (usb_c_x - USB_C_PLUG[1] / 2, usb_c_x + USB_C_PLUG[1] / 2))
plug_u = ml + mw / 2
plug_x = mx + p["microbit_board"] + USB_PORT_BEHIND
microbit_plug = back((plug_u - MICROBIT_PLUG[0] / 2, plug_u + MICROBIT_PLUG[0] / 2),
                     (mt + mh, mt + mh + MICROBIT_PLUG[2]),
                     (plug_x - MICROBIT_PLUG[1] / 2, plug_x + MICROBIT_PLUG[1] / 2))


def stiff_cable(start, along):
    """A stiff cable, in the panel's frame: from `start` (the end of its plug) straight on `along` (a
    unit vector in the panel's plane) for CABLE_OUT, then bending over backwards."""
    end = start + along * CABLE_OUT
    r, backwards = CABLE_BEND, V(1, 0, 0)
    corner = end + along * r + backwards * r  # the bend's end, pointing backwards
    middle = end + along * (r / math.sqrt(2)) + backwards * (r - r / math.sqrt(2))
    path = Part.Wire([Part.LineSegment(start, end).toShape(), Part.Arc(end, middle, corner).toShape(),
                      Part.LineSegment(corner, corner + backwards * r).toShape()])
    return path.makePipeShell([Part.Wire(Part.makeCircle(CABLE / 2, start, along))], True, True)


usb_cables = [stiff_cable(V(DEPTH + usb_x, SIZE - pb - USB_PLUG[2], SIZE / 2 - (pl + at)), V(0, -1, 0))
              for at in USB_PORTS_FROM_LEFT]
usb_c_cable = stiff_cable(V(DEPTH + usb_c_x, SIZE - usb_c_v, SIZE / 2 - pl + USB_C_PLUG[2]), V(0, 0, 1))
panel_plugs = [back(HUB75_US, vs, (0, HUB75_HIGH)) for vs in PLUG_VS] + [back(POWER_US, vs, (0, POWER_HIGH))
                                                                         for vs in PLUG_VS]
heads = [post(SIZE - p["insert_edge"], p["insert_middle"], (PLATE, PLATE + M3_HEAD[1]), M3_HEAD[0] / 2),
         post(p["insert_edge"], p["insert_middle"], (PLATE, PLATE + M3_HEAD[1]), M3_HEAD[0] / 2),
         post(p["insert_top_u"], p["insert_edge"], (PLATE, PLATE + M3_HEAD[1]), M3_HEAD[0] / 2)]

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
middle = SIZE / LEDS / 2
check("stand: the lip stays below the middle of the bottom row of LEDs", p["lip_height"] <= middle - 0.25,
      "%g mm, the middle of the row %.2f mm from the edge" % (p["lip_height"], middle))
check("stand: the back wall stays below the connectors, whichever way up the panel stands",
      p["back_height"] <= CONNECTORS - 10, "%g mm, the connectors from %g mm" % (p["back_height"], CONNECTORS))

on_holder = [(PI_MASS, pi), (SPEAKER_MASS, speaker), (MICROBIT_MASS, microbit), (holder.Volume * PLA, holder)]
# The converter on its posts on the base, in the stand's frame, in the middle of the stand: its base
# with the flanges, its body with the fins, and the half round openings in the flanges
c_y = BT + p["converter_rest"]
c_mid = p["converter_front"] + p["converter_width"] / 2
cl, cw, cb, fw, ft = (p["converter_length"], p["converter_width"], p["converter_body"], p["flange_width"],
                      p["flange_thickness"])
converter = Part.makeBox(cw, p["converter_height"], cb, V(p["converter_front"], c_y, -cb / 2))
converter = converter.fuse(Part.makeBox(fw, ft, cl, V(c_mid - fw / 2, c_y, -cl / 2)))
mounts = [(c_mid + a * p["mount_across"] / 2, s * p["mount_along"] / 2) for a in (-1, 1) for s in (-1, 1)]
for mx_, mz_ in mounts:
    sign = 1 if mz_ > 0 else -1
    out = Part.makeBox(p["mount_d"], ft + 2, 10, V(mx_ - p["mount_d"] / 2, c_y - 1, mz_ if sign > 0 else mz_ - 10))
    converter = converter.cut(Part.makeCylinder(p["mount_d"] / 2, ft + 2, V(mx_, c_y - 1, mz_), V(0, 1, 0))).cut(out)
converter = converter.removeSplitter()
masses = ([(PANEL_MASS, centre(panel)), (stand.Volume * PLA, centre(stand)), (CONVERTER_MASS, centre(converter))]
          + [(m, centre(placed(s, spot))) for m, s in on_holder])
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

# The holder
check("holder: one valid solid", holder.isValid() and len(holder.Solids) == 1)
check("holder: lies flat on the back of the panel", abs(holder.BoundBox.XMin - DEPTH) < 1e-6)
wall_top = back((0, SIZE), (SIZE - p["back_height"], SIZE), (0, 40))
check("holder: above the back wall of the stand", holder.common(wall_top).Volume < TOUCH)
check("holder: the speaker rests in its hole", overlap(holder, speaker) < 0.01, "%.3f mm3" % overlap(holder, speaker))
gap = holder.distToShape(speaker)[0]
check("holder: the speaker touches the edge of the hole", gap < 0.01, "%.3f mm" % gap)
sunk = p["speaker_sink"] - PLATE
check("holder: the speaker's back reaches %.1f mm into the opening, %g mm deep (guess)" % (sunk, p["window_depth"]),
      sunk <= p["window_depth"] - 1)
below = speaker.common(back((0, SIZE), (0, SIZE), (-30, 0)))
check("holder: what sinks into the panel stays inside the opening", below.cut(window).Volume < 0.01,
      "%.3f mm3 outside it" % below.cut(window).Volume)
check("holder: the Pi clear of the speaker", pi.distToShape(speaker)[0] >= 5, "%.1f mm" % pi.distToShape(speaker)[0])
check("holder: the Pi stands on its posts and is otherwise clear of the holder", overlap(holder, pi) < TOUCH
      and pi.distToShape(holder)[0] < TOUCH)
check("holder: the micro:bit on its posts, its peg through ring 0", overlap(holder, microbit) < TOUCH
      and microbit.distToShape(holder)[0] < TOUCH)
check("holder: the solder under the Pi clear of the plate", p["pi_rest"] - SOLDER >= 1, "%g mm" % (p["pi_rest"] - SOLDER))
check("holder: the micro:bit's buttons clear of the plate", p["microbit_rest"] - BUTTONS >= 1,
      "%.1f mm" % (p["microbit_rest"] - BUTTONS))
plugs = {"USB": usb_plugs[0], "USB 2": usb_plugs[1], "USB-C": usb_c, "micro:bit USB": microbit_plug}
for name, plug in plugs.items():
    far = min(plug.distToShape(s)[0] for s in (holder, speaker, microbit if name != "micro:bit USB" else pi))
    check("plugs: the %s plug clear of the holder, the speaker and the micro:bit" % name, far >= 1, "%.1f mm" % far)
check("plugs: the Pi's plugs stay within the edges of the panel",
      all(s.BoundBox.ZMin >= -SIZE / 2 and s.BoundBox.YMax <= SIZE for s in (usb_plugs[0], usb_plugs[1], usb_c)))
near = min(s.distToShape(plug)[0] for s in (holder, speaker, pi, microbit, microbit_plug, usb_c) for plug in panel_plugs)
check("plugs: the panel's HUB75 and power plugs clear of everything on the holder", near >= 1, "%.1f mm" % near)
head_gap = min(h.distToShape(s)[0] for h in heads for s in (speaker, pi, microbit, usb_c, *usb_plugs))
check("plugs: the screw heads clear of what stands near them", head_gap >= 1, "%.1f mm" % head_gap)
standing = [placed(s, spot) for s in (holder, speaker, pi, microbit, *usb_plugs, usb_c, microbit_plug)]
near = min(s.distToShape(stand)[0] for s in standing)
check("holder: everything on it clear of the stand", near >= 5, "%.1f mm" % near)
for name, cable in (("USB", usb_cables[0]), ("USB 2", usb_cables[1]), ("USB-C", usb_c_cable)):
    far = min(cable.distToShape(s)[0] for s in (holder, speaker, microbit, panel_alone))
    check("cables: the %s cable clear of the holder, the speaker and the panel" % name, far >= 1, "%.1f mm" % far)
check("cables: all behind the panel, within its outline", all(
    c.BoundBox.YMax <= SIZE and c.BoundBox.YMin >= 0 and abs(c.BoundBox.ZMin) <= SIZE / 2 and abs(c.BoundBox.ZMax) <= SIZE / 2
    for c in usb_cables + [usb_c_cable]))
# The converter
check("converter: on its four posts", overlap(converter, stand) < TOUCH and converter.distToShape(stand)[0] < TOUCH,
      "%.3f mm3" % overlap(converter, stand))
check("converter: air under it", p["converter_rest"] >= 3, "%g mm" % p["converter_rest"])
in_post = CONVERTER_SCREW - p["flange_thickness"] - WASHER[1]
check("converter: its M3 x 10 screws reach into the posts, not through them",
      5 <= in_post <= BT + p["converter_rest"] - 0.5 - 0.5, "%.1f mm in the post" % in_post)
check("converter: the washer fits between the end of the flange and the body",
      (cl - cb) / 2 - (cl - p["mount_along"]) / 2 >= WASHER[0] / 2,
      "%.1f mm, the washer's radius %g" % ((cl - cb) / 2 - (cl - p["mount_along"]) / 2, WASHER[0] / 2))
far = min(c.distToShape(converter)[0] for c in (placed(usb_cables[0], spot), placed(usb_cables[1], spot)))
check("cables: the USB cables clear of the converter", far >= 1, "%.1f mm" % far)
check("converter: clear of the channel", converter.BoundBox.XMin >= channel.XMax + 1,
      "%.1f mm" % (converter.BoundBox.XMin - channel.XMax))
far = min(converter.distToShape(s)[0] for s in (panel, placed(holder, spot), placed(pi, spot)))
check("converter: well below the panel and what is on its back", far >= 5, "%.1f mm" % far)
check("converter: stays on the base", p["converter_front"] + cw <= p["base_back"] - 1
      and cl / 2 <= SIZE / 2, "%.0f mm behind it" % (p["base_back"] - p["converter_front"] - cw))
room = SIZE / 2 + FIT + p["ear_thickness"] - cl / 2
check("converter: room at both ends for the wires of its terminals", room >= 40, "%.1f mm to the edge of the base" % room)
to_joint = min(abs(abs(mz_) - abs(right.BoundBox.ZMin - p["joint_fit"])) for _, mz_ in mounts) - p["converter_post_d"] / 2
check("converter: the posts clear of the joint between the halves", to_joint >= 5, "%.1f mm" % to_joint)
print("     behind the panel: the speaker's face %.1f mm, the Pi %.1f mm, the micro:bit %.1f mm"
      % (s_face, rest + PI_STACK, mx + p["microbit_board"] + MICROBIT_BEHIND), flush=True)
lying = holder.copy()
lying.rotate(V(), V(0, 1, 0), -90)
box = lying.optimalBoundingBox()
fit = bed_fit(box, X2D_BED)
check("print: holder fits the X2D", bool(fit), "%.1f x %.1f mm, %s" % (box.XLength, box.YLength, fit))

leds, (width, height) = preview_leds(PREVIEW_TEXT, SIZE, LEDS, 4)
check("preview: the text fits the panel", height <= LEDS and width <= LEDS, "%d x %d LEDs" % (width, height))

preview = App.newDocument("stand128_preview")
preview.addObject("Part::Feature", "Stand").Shape = stand
preview.addObject("Part::Feature", "Panel").Shape = panel.cut(placed(window, spot))
preview.addObject("Part::Feature", "Converter").Shape = converter
preview.addObject("Part::Feature", "UsbPlugs").Shape = placed(Part.makeCompound(usb_plugs + [usb_c]), spot)
preview.addObject("Part::Feature", "UsbCables").Shape = placed(Part.makeCompound(usb_cables + [usb_c_cable]), spot)
for name, shape in (("Holder", holder), ("Speaker", speaker), ("Pi", pi), ("Microbit", microbit)):
    preview.addObject("Part::Feature", name).Shape = placed(shape, spot)
preview.addObject("Part::Feature", "LEDs").Shape = placed(Part.makeCompound(leds), spot)
preview.recompute()
preview.saveAs(os.path.join(HERE, "stand128_preview.FCStd"))

summary()
