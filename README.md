# led-tetragon-stand

A 3D-printed stand for the LED tetragon: one 64 x 64 P3 LED panel on its
factory frame, with the Raspberry Pi on the back. The panel leans back at an
angle that is set by hand (75 degrees to the table by default) and held by two
knobs on a friction hinge.

Print 1 x `base.stl`, 1 x `cradle.stl` (lying on its floor) and 2 x
`knob.stl`. Also needed: 2 x M5 x 16 hex bolt and 2 x M5 nut.

The model is made in FreeCAD 1.x from `build_stand.py`; all dimensions are in
the `Params` spreadsheet in `stand.FCStd`. Run `./build.sh` to build, check
and save the files. See [PLAN.md](PLAN.md) for the design and the measurements.

## Licence

GNU General Public License v3.0, see [LICENSE](LICENSE).
