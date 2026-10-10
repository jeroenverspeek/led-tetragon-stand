# led-tetragon-stand

<img src="stand_preview.png" alt="The panel on its stand at 75 degrees" width="450">

A 3D-printed stand for the LED tetragon: one 64 x 64 P3 LED panel on its
factory frame, with the Raspberry Pi on the back. The panel leans back at an
angle that is set by hand (75 degrees to the table by default) and held by a
friction hinge with two countersunk screws.

Print 1 x `base.stl` and 1 x `cradle.stl` (lying on its floor). Also needed:
2 x M5 x 12 countersunk screw and 2 x M5 nut.

The model is made in FreeCAD 1.x from `build_stand.py`; all dimensions are in
the `Params` spreadsheet in `stand.FCStd`. Run `./build.sh` to build, check
and save the files. See [PLAN.md](PLAN.md) for the design and the measurements.

## Licence

GNU General Public License v3.0, see [LICENSE](LICENSE).
