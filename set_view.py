# View settings for the stand files
# by Jeroen Verspeek
#
# Files written by freecadcmd open with every object hidden and the camera
# not aimed at the model. This opens them with the FreeCAD window (which can
# be off-screen), sets what is visible, aims the camera and saves again.
#
# Also renders the previews as PNGs for the README: the 64 x 64 stand from the
# front and from the back, the 128 x 128 stand from the front and its halves
# for the Ender pulled apart.
#
# Run:  QT_QPA_PLATFORM=offscreen freecad set_view.py
# Does both stands; with STANDS=64 or STANDS=128 in the environment only that
# one (as ./build.sh does).
###########################

import os

import FreeCAD as App
import FreeCADGui as Gui
from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
V = App.Vector
CAMERA = """#Inventor V2.1 ascii

OrthographicCamera {
  viewportMapping ADJUST_CAMERA
  position %f %f %f
  orientation %f %f %f %f
  nearDistance 0
  farDistance %f
  aspectRatio 1
  focalDistance %f
  height %f
}
"""


def looking_from(back, up=V(0, 0, 1)):
    """A camera turn that looks along -back, with `up` up on the screen."""
    back = back.normalize()
    right = up.cross(back).normalize()
    up = back.cross(right)
    return App.Rotation(App.Matrix(right.x, up.x, back.x, 0, right.y, up.y, back.y, 0,
                                   right.z, up.z, back.z, 0, 0, 0, 0, 1))


# from the front, a little from the left and from above; x points backwards, y to the left
FRONT = looking_from(V(-2, 1, 1.2))
# from the back, a little from the left (seen from the back) and from above
BACK = looking_from(V(2, -1, 1.2))
# the same for the 128 x 128 stand, which is modelled with y up and z to the right
FRONT128 = looking_from(V(-2, 1.2, -1), V(0, 1, 0))
ABOVE128 = looking_from(V(-1, 2.5, -0.6), V(0, 1, 0))  # from higher up, so the dovetails show
STANDS = os.environ.get("STANDS", "64 128").split()


def aim(doc, shown, turn=FRONT):
    """Aim a camera at the shown objects."""
    Gui.updateGui()  # let the window finish opening the document
    box = App.BoundBox()
    for obj in shown:
        box.add(obj.Shape.BoundBox)
    reach = box.DiagonalLength
    eye = box.Center + turn.multVec(V(0, 0, 1)) * reach
    axis = turn.Axis
    # written out in full: the view commands are animated and may not be finished when saving
    Gui.getDocument(doc.Name).ActiveView.setCamera(
        CAMERA % (eye.x, eye.y, eye.z, axis.x, axis.y, axis.z, turn.Angle, 2 * reach, reach, reach))
    Gui.updateGui()


def save(doc, shown, turn=FRONT):
    """Aim a camera at the shown objects and save the document."""
    aim(doc, shown, turn)
    doc.save()


def screenshot(doc, path, size=1200):
    """Save the view of a document as a PNG, not yet cropped."""
    Gui.getDocument(doc.Name).ActiveView.saveImage(path, size, size, "White")


def crop_alike(paths, margin=20):
    """Crop the PNGs to the same box round the models, with a small white margin, so that
    they have the same size and scale side by side."""
    images = [Image.open(path).convert("RGB") for path in paths]
    boxes = [ImageChops.difference(image, Image.new("RGB", image.size, "white")).getbbox() for image in images]
    width, height = images[0].size
    box = (max(min(b[0] for b in boxes) - margin, 0), max(min(b[1] for b in boxes) - margin, 0),
           min(max(b[2] for b in boxes) + margin, width), min(max(b[3] for b in boxes) + margin, height))
    for image, path in zip(images, paths):
        image.crop(box).save(path)


if "64" in STANDS:
    # stand.FCStd: show the base; the cradle is modelled in its own place and stays hidden
    doc = App.openDocument(os.path.join(HERE, "stand.FCStd"))
    for obj in doc.Objects:
        obj.ViewObject.Visibility = False
    for body in doc.Objects:
        if body.isDerivedFrom("PartDesign::Body"):
            body.Tip.ViewObject.Visibility = True
            body.ViewObject.Visibility = body.Name == "Base"
    save(doc, [doc.getObject("Base")])

    # stand_preview.FCStd: light stand, dark panel with red LEDs, green outline of the Pi, blue holder
    # with a black speaker and a dark green micro:bit, a white power plug, grey HUB75 and USB plugs and black
    # USB cables, the Pi's USB-C power cable among them
    doc = App.openDocument(os.path.join(HERE, "stand_preview.FCStd"))
    colours = {"Base": (0.85, 0.85, 0.8), "Cradle": (0.30, 0.47, 0.66), "Panel": (0.15, 0.15, 0.15),
               "Pi_outline": (0.1, 0.5, 0.2), "LEDs": (1.0, 0.15, 0.1), "Holder": (0.30, 0.47, 0.66),
               "PowerPlug": (0.92, 0.92, 0.88), "Hub75Plug": (0.55, 0.55, 0.55),
               "MicrobitPlug": (0.55, 0.55, 0.55), "UsbPlugs": (0.55, 0.55, 0.55),
               "PowerUsbPlug": (0.55, 0.55, 0.55),
               "Microbit": (0.05, 0.35, 0.25)}
    for obj in doc.Objects:
        obj.ViewObject.Visibility = True
        obj.ViewObject.ShapeColor = colours.get(obj.Name, (0.1, 0.1, 0.1))  # screws and speaker black
    front, back = os.path.join(HERE, "stand_preview.png"), os.path.join(HERE, "stand_back.png")
    save(doc, doc.Objects, BACK)
    screenshot(doc, back)
    save(doc, doc.Objects)
    screenshot(doc, front)
    crop_alike([front, back])

if "128" in STANDS:
    # stand128.FCStd: the halves pulled apart for a picture, then the stand alone
    doc = App.openDocument(os.path.join(HERE, "stand128.FCStd"))
    for obj in doc.Objects:
        obj.ViewObject.Visibility = False
    halves = [doc.getObject("LeftHalf"), doc.getObject("RightHalf")]
    for obj in halves:
        obj.ViewObject.Visibility = True
        obj.ViewObject.ShapeColor = (0.30, 0.47, 0.66)
    halves[1].Placement = App.Placement(V(0, 0, 40), App.Rotation())
    doc.recompute()
    aim(doc, halves, ABOVE128)
    path = os.path.join(HERE, "stand128_halves.png")
    screenshot(doc, path)
    crop_alike([path])
    for obj in halves:
        obj.ViewObject.Visibility = False
    halves[1].Placement = App.Placement()
    stand = doc.getObject("Stand")
    stand.Tip.ViewObject.Visibility = True
    stand.ViewObject.Visibility = True
    doc.recompute()
    save(doc, [stand], FRONT128)

    # stand128_preview.FCStd: blue stand, dark panel with red LEDs
    doc = App.openDocument(os.path.join(HERE, "stand128_preview.FCStd"))
    colours = {"Stand": (0.30, 0.47, 0.66), "Panel": (0.15, 0.15, 0.15), "LEDs": (1.0, 0.15, 0.1)}
    for obj in doc.Objects:
        obj.ViewObject.Visibility = True
        obj.ViewObject.ShapeColor = colours[obj.Name]
    front = os.path.join(HERE, "stand128_preview.png")
    save(doc, doc.Objects, FRONT128)
    screenshot(doc, front)
    crop_alike([front])

os._exit(0)
