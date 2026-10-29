# Printing the stand

How the parts of the stands are printed. The 64 x 64 stand is printed on the
Ender 3 v2; the same printer and settings are used for the
[led-hexahedron-stand](https://github.com/jeroenverspeek/led-hexahedron-stand).
The 128 x 128 stand ([STAND128.md](STAND128.md)) is 249 mm wide: in one piece
on the Bambu Lab X2D, or in two halves on the Ender, glued.

## Printer and slicer: Ender 3 v2

- Creality Ender 3 v2. The bed is 220 x 220 mm; the model takes 220 x 200 mm
  as usable (`BED` in `check_stand.py`), 220 from left to right.
- Sliced with Ultimaker Cura. Use the printer "Creality Ender-3 V2", or set
  Printer width (X) to 220 mm under Preferences > Printers > Machine
  Settings. The combined profile "Creality Ender-3 / Ender-3 v2" takes the
  bed as 235 mm wide and centres the base on X = 117.5, so it reaches X =
  226; the v2 stops a few mm short of that and does not print what lies
  beyond. The first base lost the outer 3 mm of a cheek that way.
- PLA: bed 60 °C, nozzle 200 °C. Cura's PLA profile sets the bed to 50 °C:
  set Build Plate Temperature (under Material) to 60. Cura writes both
  temperatures at the top of the G-code, and the printer waits for them
  before it homes.
- Build Plate Adhesion Type: None, for every part. The start G-code draws
  two purge lines along the left edge of the bed (X 0.1 and 0.4, Y 20 to
  200), so no skirt is needed to prime the nozzle.

## Printer and slicer: Bambu Lab X2D

- The build plate is 256 x 256 mm with one nozzle; with both nozzles in use
  235.5 mm from left to right and 256 from front to back (from the
  retailers' specifications). The 128 x 128 stand (249 x 130 mm) fits
  either way: straight with one nozzle, its long side from front to back
  with both.
- Sliced with Bambu Studio, PLA with its own profile. Not printed yet.
- A brim of more than 3 mm does not fit beside the stand along its 249 mm.

## Layer height

On the first stand of the LED hexahedron, surfaces that were almost
horizontal showed steps: one layer is too thick to follow the slope
smoothly. Thinner layers would help there, but overhangs more often go
wrong with thinner layers. Cura's "Use Adaptive Layers" (under Experimental)
can do both: it makes the layers thinner only where a surface lies almost
flat and keeps them thick elsewhere. Not tried yet.

## Before printing: level the bed

Level the bed with `Ender3_LEVEL_psd.gcode`, which is in this repository
and on the printer's SD card: print it from the printer's menu. It is one of
the "Creality Leveling Cycle GCodes" by psdesign (Peter Solomon) on Thingiverse
(https://www.thingiverse.com/thing:4761680), licensed under the Creative
Commons Attribution licence (CC BY), linked from the
description of BV3D's (Bryan Vines) video "Creality's NEW Ender 3v2 3D
Printer! Unbox! Build! First Print!"
(https://www.youtube.com/watch?v=L6FZjkWcW2g).

## The parts of the 64 x 64 stand

One of each. The STL files already lie the right way up for printing; load
them in Cura as they are and only turn them on the bed.

| File | Lies on | On the bed | Size on the bed |
|---|---|---|---|
| `base.stl` | its plate, the letters up | its long side from left to right | 218 x 130 mm |
| `cradle.stl` | its floor | turned 24 degrees: it only fits across the diagonal | 209 x 20.5 mm |
| `holder.stl` | its plate | as it is | 101 x 140 mm |

The base (218 mm) only just fits: with a skirt it is 220 mm wide, the whole
bed, and the skirt crosses the purge lines. Without one the base lies from
X 1 to 219, about half a millimetre from the purge lines; if they stick to
its first layer, they snap off afterwards.

## The 128 x 128 stand

| File | Printer | Lies on | Size on the bed |
|---|---|---|---|
| `stand128.stl` | X2D | its plate, the letters up | 249 x 130 mm |
| `stand128_left.stl` | Ender | its plate, the letters up | 112 x 130 mm |
| `stand128_right.stl` | Ender | its plate, the letters up | 145 x 130 mm |

Print either the one piece or the two halves, not both. No support is
needed: the back wall leans back 15 degrees.

Glue the halves:

- First fit them dry: the left half (with "Led") flat on the table, and the
  right half (with "Tetragon") slid down from above onto the four dovetails
  until both lie flat. There is 0.15 mm play all round; if it is tight, sand
  the dovetails a little.
- Glue for PLA: cyanoacrylate gel (super glue gel) sets in seconds;
  two-component epoxy gives a few minutes to set the halves straight. Put
  it on the face of the joint and on the dovetails, not near the channel's
  inside or the letters, where it would squeeze out.
- Slide them together on a flat table, press them against each other and
  onto the table so that the bottoms are flush, and check with a ruler in
  the channel that it runs straight across the joint. Wipe off what
  squeezes out and let it set before the panel goes in.

## After printing (64 x 64 stand)

- Put the M5 nuts in their pockets on the inside of the ears of the cradle
  before the panel goes in.
- The hinge screws are M5 x 12 countersunk; cut a longer one to 12 mm, or it
  reaches into the panel.
- Put the M5 spring washer on one hinge screw, between the ring on the ear
  and the cheek, when the cradle goes in between the cheeks. Without it the
  rings have 1 mm of play in total and the panel falls flat however tight
  the screws are.
- Tighten the hinge screws firmly, so that the panel turns by hand but stays
  where it is put. If it starts to slip later, turn them a little further.
- Fix the holder with three M3 x 10 screws: first in the top left corner
  hole (the round one), then the top hole of the middle bar and the middle
  hole of the left bar (the slots). Leave them loose until all three are in.
- The micro:bit: LEDs towards the panel, USB port towards the Pi. Put ring 0
  over the peg, then a fourth M3 x 10 screw through the GND ring into its
  post; it cuts its own thread, so turn it in gently and stop when the board
  is held.
- The speaker: press it into its cup, then loop a cable tie (at most 4.8 mm
  wide) through both eyes and twice over the grille, in the notches, and
  pull it tight. To take it out, cut the tie and lever the speaker out with
  a screwdriver in a notch at one of its ends.
