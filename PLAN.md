# Stand for the LED tetragon

The tetragon is one 64 x 64 P3 LED panel (192 x 192 mm) on its factory frame.
The Raspberry Pi with the electrodragon hat sits on the back of the frame,
from the middle upwards, in landscape.

## Design

The panel leans back at an angle that can be set by hand: anything from lying
flat to upright, held by friction. 75 degrees to the table (leaning back 15
degrees) is the default and a good viewing angle on a desk.

- `Cradle`: a full-width channel that the bottom edge of the panel stands in:
  floor, a 1 mm lip in front, a 40 mm back wall up the back of the frame
  (well below the Pi). The panel rests in it by its own weight. Ears at both
  ends carry the hinge: a hole, a pocket for an M5 nut on the inside and a
  raised ring on the outside. The corner under the back wall is rounded round
  the hinge axis, so the cradle clears the base at every angle.
- `Base`: plate with a cheek at both ends and "Led Tetragon" sunk in front.
  Each cheek has a countersink on the outside, so the head of the screw lies
  flush. Tightening the screw presses cheek and ring together; that friction
  holds the angle. Set it once with a key or screwdriver so the panel turns
  by hand but stays where it is put.

Why not a prop leg in notches: the stand is so small that 5 degree steps lie
only 4 to 6 mm apart, and a loose prop against the back of the panel slides
unless it is fixed to the panel.

Hardware: 2 x M5 x 12 countersunk screw (90 degree head, any drive), 2 x M5
nut. Put the nuts in their pockets before the panel goes in.

## Files

| File | What |
|---|---|
| `build_stand.py` | Builds all parts. Run `./build.sh` |
| `stand.FCStd` | All parts, parametric: change values in the `Params` spreadsheet |
| `base.stl`, `cradle.stl` | For the slicer (1 of each); the cradle prints lying on its floor |
| `check_stand.py` | Assembles the stand at 60, 75 and 90 degrees and checks it |
| `stand_preview.FCStd` | The stand with the panel at 75 degrees showing "Hello world", for looking at only |
| `set_view.py` | Makes the two FreeCAD files open with the model in view |
| `build.sh` | Build, check and view settings in one go |

The base (218 x 130 mm) only just fits the 220 x 200 mm bed.

## Measured and decided

- `panel_depth` 14 mm (12 mm factory frame + 2 mm board): correct.
- The back of the frame has no magnets, only the distance holders of the Pi,
  so the lowest 40 mm is free for the back wall. The feed of the electrodragon
  board and the Pi's power (via a USB adapter) are separate cables.
- The Pi board lies 22 mm and the electrodragon board 33 mm behind the LED
  board. With about 9 mm of parts on the hat (guess) the stack sticks out
  30 mm behind the frame.
- `lip_height` 1 mm is fine.
- Countersunk screws instead of knobs. From the outside of a cheek to the
  inside of an ear is 12.5 mm, so the screws are M5 x 12; a longer one
  reaches into the panel (a 19 mm one by 7 mm), so cut it to 12 mm. Making
  cheek and ear thicker instead would make the base too wide for the bed.

## Still guessed

- The weight of the panel (400 g) and the Pi (120 g): only used to check that
  the stand does not tip.
