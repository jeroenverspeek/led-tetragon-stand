#!/bin/sh
# Rebuild the stand parts, check them and make them viewable in FreeCAD
cd "$(dirname "$0")" || exit 1
freecadcmd build_stand.py && freecadcmd check_stand.py && QT_QPA_PLATFORM=offscreen freecad set_view.py
status=$?
rm -rf __pycache__ ./*.FCBak
exit $status
