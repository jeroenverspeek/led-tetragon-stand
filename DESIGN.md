# Stand for the LED tetragon

The tetragon is one 64 x 64 P3 LED panel (192 x 192 mm) on its factory frame.
The Raspberry Pi with the electrodragon hat sits on the back of the frame, in
portrait on the vertical middle bar, USB ports at the top, from the middle to
the right seen from the back. The USB speaker and the micro:bit go in the left
half. All measurements of the panel and what is on it, what was decided
from them and what is still guessed are in [PANEL.md](PANEL.md).

## Design

The panel leans back at an angle that can be set by hand: anything from lying
flat to upright, held by friction. 75 degrees to the table (leaning back 15
degrees) is the default and a good viewing angle on a desk.

- `Cradle`: a full-width channel that the bottom edge of the panel stands in:
  floor, a 1 mm lip in front, a 28 mm back wall up the back of the frame,
  below the HUB75 IN plug (32 mm up). The panel rests in it by its own
  weight. Ears at both
  ends carry the hinge: a hole, a pocket for an M5 nut on the inside and a
  raised ring on the outside. The corner under the back wall is rounded round
  the hinge axis, so the cradle clears the base at every angle.
- `Base`: plate with a cheek at both ends and "Led Tetragon" sunk in front.
  Each cheek has a countersink on the outside, so the head of the screw lies
  flush. The rings have 0.3 mm play between the cheeks (`hinge_play`), so the
  cradle goes in; tightening the screw bends the cheek onto its ring, and
  that friction holds the angle. Set it once with a key or screwdriver so
  the panel turns by hand but stays where it is put.
- `Holder`: one part on three M3 x 10 screws, in the left half seen from the
  back, beside the Pi: the top left corner hole, the top hole of the middle
  bar and the middle hole of the left bar. Prints lying on its plate. Only
  the corner hole is round; the other two, 80 mm from it, are slots, 2.5 mm
  longer each way (`screw_slot`): the one in the middle bar from left to
  right, the one in the left bar from top to bottom. They take up what the
  print and the measurements from the photo are off: with three round holes
  the third screw did not go in on the first print, 1.5 mm off.
  - Speaker at the top, grille facing backwards, 5 mm from the left so its
    rounded end stays clear of the Pi: a cup on the plate for its rounded
    back, with a lip along both long sides. The lips alone left it loose, so
    a cable tie loops through an eye on both long sides of the cup and twice
    over the middle of the grille, in a notch 1 mm below the face, and
    presses it onto the plate. A notch at both round ends lets a screwdriver
    lever it out. The cable leaves the speaker's
    bottom side, 33 mm from its left end, through a slot in the bottom of the
    cup, with 10 mm free below it for its sleeve, 2 mm above the power plug.
    The plate bridges the frame, so the power cable, leaving the power plug
    upwards, bends up under it: 10 mm above the plug. The speaker sticks out
    36 mm behind the frame, the Pi 30 mm.
  - A strip down the left bar, past the power plug, joins it to a plate for
    the micro:bit: upright, parallel to the panel so it tilts with it, LEDs
    towards the panel, USB port towards the Pi. Just below the power plug (1.1
    mm), so the HUB75 ribbon has 4.7 mm below it to bend up over it. It lies
    on four posts 6 mm high, 1.8 mm clear of its buttons: under the GND ring
    a post that an M3 x 10 screw through the ring cuts its thread in, under
    ring 0 one with a printed peg through the ring, and two under the USB
    edge. The screw is the only metal on a ring: rings 0, 1 and 2 are touch
    inputs, and the black oxide screws conduct; on GND it does no harm. The
    back of the micro:bit stays open. Sticks out 16 mm.
  - The micro:bit's USB plug, straight, sticks out 40 mm and reaches 6 mm
    under the edge of the Pi; a cable with an angled (90 degree) micro USB
    plug, the cable turning up towards the Pi's USB ports, stays clear.

Why not a prop leg in notches: the stand is so small that 5 degree steps lie
only 4 to 6 mm apart, and a loose prop against the back of the panel slides
unless it is fixed to the panel.

Hardware: 2 x M5 x 12 countersunk screw (90 degree head, any drive), 2 x M5
nut, 4 x M3 x 10 screw (3 for the holder, 1 for the micro:bit), 1 cable tie for the speaker (at most 4.8 mm wide,
at least 200 mm long). Put the nuts in their pockets before the panel goes
in.

All black (black oxide steel):

| Part | What | Order |
|---|---|---|
| 2 x hinge screw | M5 x 12 countersunk hex socket, DIN 7991, 10.9 or 12.9; 3 mm key. Not aluminium, too soft. | [RS PRO 0281467](https://benl.rs-online.com/web/p/socket-screws/0281467), [AliExpress](https://nl.aliexpress.com/w/wholesale-M5-countersunk-hex-socket-black-DIN7991.html) |
| 2 x nut | M5 hex nut, DIN 934: 8 across the flats, 4 thick. Not a nylon insert nut, too thick for the 4.2 mm pocket. | [AliExpress](https://nl.aliexpress.com/w/wholesale-M5-hex-nut-black-DIN934.html) |
| 4 x holder screw | M3 x 10 socket head cap, DIN 912, 12.9; 2.5 mm key. | [AliExpress](https://nl.aliexpress.com/w/wholesale-M3-socket-head-cap-screw-black-DIN912.html) |

On AliExpress the length is chosen per listing; check that it is the 12 or
10 mm variant.

## Files

| File | What |
|---|---|
| `build_stand.py` | Builds all parts. Run `./build.sh` |
| `stand.FCStd` | All parts, parametric: change values in the `Params` spreadsheet |
| `base.stl`, `cradle.stl`, `holder.stl` | For the slicer (1 of each); the cradle prints lying on its floor, the holder on its plate |
| `check_stand.py` | Assembles the stand at 60, 75 and 90 degrees and checks it |
| `stand_preview.FCStd` | The stand with the panel at 75 degrees showing "Hello world", and the holder with the speaker and micro:bit on the back, for looking at only |
| `stand_preview.png`, `stand_back.png` | Pictures of that from the front and from the back, for the README |
| `set_view.py` | Makes the two FreeCAD files open with the model in view |
| `build.sh` | Build, check and view settings in one go |
| `PANEL.md` | All measurements of the panel, the Pi, the speaker and the micro:bit; what was decided from them and what is still guessed |
| `PRINTING.md` | Printer, slicer and settings, how each part lies on the bed, and what to do after printing |
| `Ender3_LEVEL_psd.gcode` | The program for levelling the bed before printing (by psdesign, CC BY; see `PRINTING.md`) |
| `photos/` | Photos of the back of the panel and of the micro:bit, and `grid.py` to measure from them (see `PANEL.md`) |

The base (218 x 130 mm) only just fits the 220 x 200 mm bed.

