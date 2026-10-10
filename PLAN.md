# Stand for the LED tetragon

The tetragon is one 64 x 64 P3 LED panel (192 x 192 mm) on its factory frame.
The Raspberry Pi with the electrodragon hat sits on the back of the frame, in
portrait on the vertical middle bar, USB ports at the top, from the middle to
the right seen from the back. The USB speaker and the micro:bit go in the left
half. All measurements of the panel and what is on it are in
[PANEL.md](PANEL.md).

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
  flush. Tightening the screw presses cheek and ring together; that friction
  holds the angle. Set it once with a key or screwdriver so the panel turns
  by hand but stays where it is put.
- `Holder`: one part on three M3 x 10 screws, in the left half seen from the
  back, beside the Pi: the top left corner hole, the top hole of the middle
  bar and the middle hole of the left bar. Prints lying on its plate.
  - Speaker at the top, grille facing backwards, 5 mm from the left so its
    rounded end stays clear of the Pi: a cup on the plate for its rounded
    back, held by a lip along both long sides. The cable leaves the speaker's
    bottom side, 33 mm from its left end, through a slot in the bottom of the
    cup, with 10 mm free below it for its sleeve, 3 mm above the power plug.
    The plate bridges the frame, so the power cable, leaving the power plug
    upwards, bends up under it: 11 mm above the plug. The speaker sticks out
    36 mm behind the frame, the Pi 30 mm.
  - A strip down the left bar, past the power plug, joins it to the micro:bit:
    upright in a pocket, parallel to the panel so it tilts with it, LEDs
    towards the panel, USB port towards the Pi. Just below the power plug (2
    mm), so the HUB75 ribbon has 4 mm below it to bend up over it. The
    micro:bit slides in from the side edge of the panel, and its USB plug,
    through a slot in the side of the pocket, keeps it there. A window in the
    cover shows its back. Sticks out 17 mm.
  - The micro:bit's USB plug, straight, sticks out 40 mm and reaches 6 mm
    under the edge of the Pi; a cable with an angled (90 degree) micro USB
    plug, the cable turning up towards the Pi's USB ports, stays clear.

Why not a prop leg in notches: the stand is so small that 5 degree steps lie
only 4 to 6 mm apart, and a loose prop against the back of the panel slides
unless it is fixed to the panel.

Hardware: 2 x M5 x 12 countersunk screw (90 degree head, any drive), 2 x M5
nut, 3 x M3 x 10 screw. Put the nuts in their pockets before the panel goes
in.

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
| `PANEL.md` | All measurements of the panel, the Pi, the speaker and the micro:bit |

The base (218 x 130 mm) only just fits the 220 x 200 mm bed.

## Measured and decided

The measurements themselves are in [PANEL.md](PANEL.md).

- `lip_height` 1 mm is fine.
- The back wall of the cradle was 40 mm high; the HUB75 IN plug, 32 mm up,
  sticks out behind the frame, so it is 28 mm now. That clears the hat too
  (it comes down to 39 mm, 19 mm behind the frame).
- Countersunk screws instead of knobs. From the outside of a cheek to the
  inside of an ear is 12.5 mm, so the screws are M5 x 12; a longer one
  reaches into the panel (a 19 mm one by 7 mm), so cut it to 12 mm. Making
  cheek and ear thicker instead would make the base too wide for the bed.

## Still guessed

- The weight of the panel (400 g) and the Pi (120 g): only used to check that
  the stand does not tip.
- The shape of the speaker's rounded back (from pictures); the cup only holds
  it by its flat face and leaves room behind it.
- How far the parts on the Pi and the hat stick out.
- How far the HUB75 IN plug sticks out and how much bigger it is than the
  header (12 mm and 2 mm all round). The cradle, the holder and the ribbon's
  bend depend on it.
