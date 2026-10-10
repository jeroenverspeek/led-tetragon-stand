# Stand for the LED tetragon

The tetragon is one 64 x 64 P3 LED panel (192 x 192 mm) on its factory frame.
The Raspberry Pi with the electrodragon hat sits on the back of the frame, in
portrait on the vertical middle bar (its middle two screw holes), USB ports at
the top. Seen from the back it reaches from the middle to 40 mm off the right
edge, and from 40 mm under the top down to 39 mm above the bottom, where the
hat sticks out below the Pi. The HUB75 and power connectors of the panel are
on the left half, seen from the back.

## Design

The panel leans back at an angle that can be set by hand: anything from lying
flat to upright, held by friction. 75 degrees to the table (leaning back 15
degrees) is the default and a good viewing angle on a desk.

- `Cradle`: a full-width channel that the bottom edge of the panel stands in:
  floor, a 1 mm lip in front, a 40 mm back wall up the back of the frame
  (in front of the hat, which lies 33 mm behind the LED board). The panel rests
  in it by its own weight. Ears at both
  ends carry the hinge: a hole, a pocket for an M5 nut on the inside and a
  raised ring on the outside. The corner under the back wall is rounded round
  the hinge axis, so the cradle clears the base at every angle.
- `Base`: plate with a cheek at both ends and "Led Tetragon" sunk in front.
  Each cheek has a countersink on the outside, so the head of the screw lies
  flush. Tightening the screw presses cheek and ring together; that friction
  holds the angle. Set it once with a key or screwdriver so the panel turns
  by hand but stays where it is put.
- `Holder`: carries the USB speaker (84 x 43 x 32 mm, sold as Adafruit 3369)
  and the micro:bit V2 on the back of the panel, in the top of the left half
  seen from the back, beside the Pi and well above the power connector. A
  plate goes over the middle bar with an M3 x 10 screw in its top hole; a rib
  on both sides of the bar keeps it from turning. The micro:bit lies flat on
  the plate, parallel to the panel, so it tilts with it: LEDs towards the
  panel, USB port down. It slides in from the side edge of the panel, and its
  USB plug, going down through a slot, keeps it there. On top of it is a cup
  for the rounded back of the speaker, grille facing backwards, held by a lip
  along both long sides; a slot at both ends lets the cable out. The holder
  with the speaker sticks out 50 mm behind the frame, the Pi 30 mm.

Why not a prop leg in notches: the stand is so small that 5 degree steps lie
only 4 to 6 mm apart, and a loose prop against the back of the panel slides
unless it is fixed to the panel.

Hardware: 2 x M5 x 12 countersunk screw (90 degree head, any drive), 2 x M5
nut, 1 x M3 x 10 screw. Put the nuts in their pockets before the panel goes
in.

## Files

| File | What |
|---|---|
| `build_stand.py` | Builds all parts. Run `./build.sh` |
| `stand.FCStd` | All parts, parametric: change values in the `Params` spreadsheet |
| `base.stl`, `cradle.stl`, `holder.stl` | For the slicer (1 of each); the cradle prints lying on its floor, the holder standing on the rim of its cup |
| `check_stand.py` | Assembles the stand at 60, 75 and 90 degrees and checks it |
| `stand_preview.FCStd` | The stand with the panel at 75 degrees showing "Hello world", and the holder with the speaker and micro:bit on the back, for looking at only |
| `stand_preview.png`, `stand_back.png` | Pictures of that from the front and from the back, for the README |
| `set_view.py` | Makes the two FreeCAD files open with the model in view |
| `build.sh` | Build, check and view settings in one go |

The base (218 x 130 mm) only just fits the 220 x 200 mm bed.

## Measured and decided

- `panel_depth` 14 mm (12 mm factory frame + 2 mm board): correct.
- The back of the frame has no magnets, only the distance holders of the Pi.
  The hat comes down to 39 mm above the bottom, but 19 mm behind the frame, so
  the 40 mm back wall stays 15 mm clear of it. The feed of the electrodragon
  board and the Pi's power (via a USB adapter) are separate cables.
- The Pi board lies 22 mm and the electrodragon board 33 mm behind the LED
  board. With about 9 mm of parts on the hat (guess) the stack sticks out
  30 mm behind the frame.
- `lip_height` 1 mm is fine.
- Middle bar: 20 mm wide, flush with the back of the frame, 4 M3 holes with
  brass inserts, the top one 10 mm under the top; the Pi is on the middle two.
- The panel's HUB75 connectors are 30 mm from the left side (seen from the
  back), only the lower one (IN) is used; its cable and plug stick out. The
  power connector is 39 mm from the left side, 80 mm under the top, and sticks
  out.
- micro:bit: on a 20 cm USB cable, only tilted together with the panel; its
  buttons are not used.
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
