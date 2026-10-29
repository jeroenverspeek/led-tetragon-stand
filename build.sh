#!/bin/sh
# Rebuild the stand parts, check them and make them viewable in FreeCAD.
# ./build.sh builds both stands; ./build.sh 64 or ./build.sh 128 only that one.
cd "$(dirname "$0")" || exit 1
stands=${*:-64 128}
status=0
for stand in $stands; do
    case $stand in
        64) suffix= ;;
        128) suffix=128 ;;
        *) echo "usage: $0 [64] [128]" >&2; exit 2 ;;
    esac
    freecadcmd "build_stand$suffix.py" && freecadcmd "check_stand$suffix.py" || { status=1; break; }
done
if [ $status = 0 ]; then
    STANDS="$stands" QT_QPA_PLATFORM=offscreen freecad set_view.py
    status=$?
fi
rm -rf __pycache__ ./*.FCBak
exit $status
