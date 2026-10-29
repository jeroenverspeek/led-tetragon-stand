# Shared by the build and check scripts of both stands
# by Jeroen Verspeek
#
# build_stand.py, check_stand.py (the 64 x 64 panel) and build_stand128.py,
# check_stand128.py (the 128 x 128 panel) import this; it is not run itself.
###########################

import math
import os

import FreeCAD as App
import MeshPart
import Part
import Sketcher

V = App.Vector

# The font for the text on the base: the first file that exists (as on the cube's stand)
FONTS = [os.path.expanduser("~/.fonts/segoescb.ttf"), "/run/media/jeroen/OS/Windows/Fonts/segoescb.ttf",
         "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]

ORIGIN = (-1, 1)  # sketch origin point
H_AXIS, V_AXIS = -1, -2

###########################
# Building
###########################


def font():
    return next(f for f in FONTS if os.path.exists(f))


def make_params(doc, params):
    """The Params spreadsheet: one row per (alias, value, meaning), the value in mm, or per (alias,
    value, meaning, unit) for another unit, such as "deg"."""
    sheet = doc.addObject("Spreadsheet::Sheet", "Params")
    for row, (alias, value, meaning, *unit) in enumerate(params, start=1):
        sheet.set("A%d" % row, alias)
        sheet.set("B%d" % row, "%g %s" % (value, unit[0] if unit else "mm"))
        sheet.set("C%d" % row, meaning)
        sheet.setAlias("B%d" % row, alias)
    doc.recompute()
    return sheet


def new_sketch(body, name, plane, z=0, z_expression=None):
    sketch = body.newObject("Sketcher::SketchObject", name)
    support = next(f for f in body.Origin.OriginFeatures if f.Role == plane)
    sketch.AttachmentSupport = [(support, "")]
    sketch.MapMode = "FlatFace"
    sketch.AttachmentOffset = App.Placement(V(0, 0, z), App.Rotation())
    if z_expression:
        sketch.setExpression("AttachmentOffset.Base.z", z_expression)
    return sketch


def dimension(sketch, constraint, name, expression):
    """Add a dimension that follows the Params spreadsheet."""
    sketch.renameConstraint(sketch.addConstraint(constraint), name)
    sketch.setExpression("Constraints." + name, expression)


def pinned_polygon(sketch, corners, arcs=()):
    """A closed outline whose corners are each held at (x, y), given as (x, y, x expression, y expression).
    An expression gives the distance from the axis, so it is never negative; None means on the axis.
    `arcs` maps i to (cx, cy, cx expression): the side from corner i to the next is then an arc round
    (cx, cy), anticlockwise, instead of a straight line."""
    n = len(corners)
    arcs = dict(arcs)
    for i in range(n):
        start, end = V(*corners[i][:2]), V(*corners[(i + 1) % n][:2])
        if i in arcs:
            centre = V(*arcs[i][:2])
            sketch.addGeometry(Part.ArcOfCircle(Part.Circle(centre, V(0, 0, 1), (start - centre).Length),
                                                math.atan2(start.y - centre.y, start.x - centre.x),
                                                math.atan2(end.y - centre.y, end.x - centre.x)))
        else:
            sketch.addGeometry(Part.LineSegment(start, end))
    for i in range(n):
        sketch.addConstraint(Sketcher.Constraint("Coincident", i, 2, (i + 1) % n, 1))
    for i, (x, y, x_expression, y_expression) in enumerate(corners):
        for axis, value, expression, line in (("X", x, x_expression, V_AXIS), ("Y", y, y_expression, H_AXIS)):
            name = "corner%d_%s" % (i, axis.lower())
            if expression is None:
                sketch.addConstraint(Sketcher.Constraint("PointOnObject", i, 1, line))
            elif value >= 0:
                dimension(sketch, Sketcher.Constraint("Distance" + axis, *ORIGIN, i, 1, value), name, expression)
            else:
                dimension(sketch, Sketcher.Constraint("Distance" + axis, i, 1, *ORIGIN, -value), name, expression)
    for i, (cx, _, cx_expression) in arcs.items():
        # both ends are held already, so the place of the centre across fixes the arc
        dimension(sketch, Sketcher.Constraint("DistanceX", *ORIGIN, i, 3, cx), "arc%d_centre_x" % i, cx_expression)


def pad(body, name, sketch, length_expression, symmetric=False, reversed_=False):
    feature = body.newObject("PartDesign::Pad", name)
    feature.Profile = sketch
    feature.setExpression("Length", length_expression)
    if symmetric:
        feature.SideType = "Symmetric"
    feature.Reversed = reversed_
    return feature


def primitive(body, kind, name, sizes, at, turn=App.Rotation()):
    """A PartDesign primitive. `sizes` maps a property to (value, expression); `at` is three
    (value, expression) pairs for its place, an expression None meaning a fixed value."""
    feature = body.newObject("PartDesign::" + kind, name)
    for prop, (value, expression) in sizes.items():
        setattr(feature, prop, value)
        if expression:
            feature.setExpression(prop, expression)
    feature.Placement = App.Placement(V(*(value for value, _ in at)), turn)
    for axis, (_, expression) in zip("xyz", at):
        if expression:
            feature.setExpression("Placement.Base." + axis, expression)
    return feature


def check_built(doc):
    """Stop if a sketch is not fully constrained or a feature did not build."""
    for obj in doc.Objects:
        if obj.isDerivedFrom("Sketcher::SketchObject") and not obj.FullyConstrained:
            print("%s is not fully constrained" % obj.Name, flush=True)
            raise SystemExit(1)
        if obj.State and "Invalid" in obj.State:
            print("%s did not build" % obj.Name, flush=True)
            raise SystemExit(1)


def write_stl(name, shape, path, axis=None, degrees=0):
    """Check that the shape is one valid solid, turn it to lie on the bed as it is printed (round
    `axis` by `degrees`), put it on z = 0 and write it as an STL."""
    if not shape.isValid() or len(shape.Solids) != 1:
        print("%s is not a single valid solid" % name, flush=True)
        raise SystemExit(1)
    if axis:
        shape = shape.copy()
        shape.rotate(V(), axis, degrees)
        shape.translate(V(0, 0, -shape.optimalBoundingBox().ZMin))
    mesh = MeshPart.meshFromShape(Shape=shape, LinearDeflection=0.02, AngularDeflection=0.2)
    mesh.write(path)
    box = shape.optimalBoundingBox()
    print("%s %.2f x %.2f x %.2f mm, %.2f cm3" % (os.path.basename(path), box.XLength, box.YLength, box.ZLength,
                                                  shape.Volume / 1000), flush=True)


###########################
# Checking
###########################

TOUCH = 1e-6
PLA = 1.24 / 1000  # g/mm3; a printed part weighs less, so the stand is lighter than this
failures = []


def read_params(doc):
    """Every parameter in the Params spreadsheet by its alias, in mm (an angle in degrees)."""
    params = doc.getObject("Params")
    p = {}
    row = 1
    while params.getContents("A%d" % row):
        alias = params.getContents("A%d" % row).lstrip("'")
        p[alias] = getattr(params, alias).Value
        row += 1
    return p


def check(name, ok, detail=""):
    print("%-4s %s %s" % ("ok" if ok else "FAIL", name, detail), flush=True)
    if not ok:
        failures.append(name)


def summary():
    print("%d checks failed" % len(failures) if failures else "all checks passed", flush=True)


def placed(shape, placement):
    copy = shape.copy()
    copy.Placement = placement.multiply(copy.Placement)
    return copy


def centre(shape):
    """Centre of mass of a solid or of a compound of solids."""
    solids = shape.Solids
    return sum((solid.CenterOfMass * solid.Volume for solid in solids), V()) / sum(solid.Volume for solid in solids)


def overlap(a, b):
    return a.common(b).Volume if a.BoundBox.intersect(b.BoundBox) else 0.0


def bed_fit(box, bed):
    """How the part fits the bed (width, depth) lying as modelled: 'straight', 'turned N degrees' or ''."""
    for degrees in range(0, 91):
        turn = math.radians(degrees)
        if (box.XLength * math.cos(turn) + box.YLength * math.sin(turn) <= bed[0]
                and box.XLength * math.sin(turn) + box.YLength * math.cos(turn) <= bed[1]):
            return "straight" if degrees == 0 else "turned %d degrees" % degrees
    return ""


# Shown on the panel in the previews, in a 5 x 7 font
FONT = {
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "e": ("00000", "00000", "01110", "10001", "11111", "10000", "01110"),
    "l": ("01100", "00100", "00100", "00100", "00100", "00100", "01110"),
    "o": ("00000", "00000", "01110", "10001", "10001", "10001", "01110"),
    "w": ("00000", "00000", "10001", "10001", "10101", "10101", "01010"),
    "r": ("00000", "00000", "10110", "11001", "10000", "10000", "10000"),
    "d": ("00001", "00001", "01101", "10011", "10001", "10001", "01111"),
}


def preview_leds(text, size, leds, dot):
    """The lit LEDs showing the lines of `text` in the middle of a panel of `size` mm with `leds` LEDs
    along an edge, each dot of the font `dot` x `dot` LEDs; in the panel's frame (x backwards from the
    front, y up from the bottom edge, z across, 0 in the middle). Returns them and the text's size in LEDs."""
    pitch = size / leds
    # each line as 7 rows of font dots, one empty font column between the letters
    lines = [[" ".join(FONT[ch][row] for ch in line) for row in range(7)] for line in text]
    height = dot * (7 * len(lines) + 2 * (len(lines) - 1))  # 2 empty font rows between the lines
    width = dot * max(len(rows[0]) for rows in lines)
    lit = []
    for n, rows in enumerate(lines):
        for row, dots in enumerate(rows):
            for col, d in enumerate(dots):
                for dy in range(dot if d == "1" else 0):
                    for dx in range(dot):
                        left = (leds - dot * len(dots)) // 2 + dot * col + dx  # LEDs from the left
                        top = (leds - height) // 2 + dot * (9 * n + row) + dy  # LEDs from the top
                        lit.append(Part.makeBox(0.4, 0.8 * pitch, 0.8 * pitch,
                                                V(-0.4, size - (top + 0.9) * pitch, -size / 2 + (left + 0.1) * pitch)))
    return lit, (width, height)
