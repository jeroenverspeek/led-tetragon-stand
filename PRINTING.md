# Printing the stand

How the parts of the stand are printed. The same printer and settings are
used for the [led-hexahedron-stand](https://github.com/jeroenverspeek/led-hexahedron-stand).

## Printer and slicer

- Creality Ender 3 v2. The bed is 220 x 220 mm; the model takes 220 x 200 mm
  as usable (`BED` in `check_stand.py`), 220 from left to right.
- Sliced with Ultimaker Cura.
- PLA: bed 60 °C, nozzle 200 °C.

## Layer height

On the first stand of the LED hexahedron, surfaces that were almost
horizontal showed steps: one layer is too thick to follow the slope
smoothly. Thinner layers would help there, but overhangs more often go
wrong with thinner layers. Cura's "Use Adaptive Layers" (under Experimental)
can do both: it makes the layers thinner only where a surface lies almost
flat and keeps them thick elsewhere. Not tried yet.

## Before printing: level the bed

Level the bed with `Ender3_LEVEL_psd.gcode`, which is on the printer's SD
card (it comes from the internet): print it from the printer's menu.

## The parts

One of each. The STL files already lie the right way up for printing; load
them in Cura as they are and only turn them on the bed.

| File | Lies on | On the bed | Size on the bed |
|---|---|---|---|
| `base.stl` | its plate, the letters up | its long side from left to right | 218 x 130 mm |
| `cradle.stl` | its floor | turned 24 degrees: it only fits across the diagonal | 209 x 20.5 mm |
| `holder.stl` | its plate | as it is | 101 x 140.5 mm |

The base (218 mm) only just fits: leave no skirt or brim that makes it
wider than 220 mm.

## After printing

- Put the M5 nuts in their pockets on the inside of the ears of the cradle
  before the panel goes in.
- The hinge screws are M5 x 12 countersunk; cut a longer one to 12 mm, or it
  reaches into the panel.
- Tighten the hinge screws so that the panel turns by hand but stays where
  it is put.
- Fix the holder with three M3 x 10 screws: in the top left corner hole, the
  top hole of the middle bar and the middle hole of the left bar.
