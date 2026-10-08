# View settings for the stand files
# by Jeroen Verspeek
#
# Files written by freecadcmd open with every object hidden and the camera
# not aimed at the model. This opens them with the FreeCAD window (which can
# be off-screen), sets what is visible, aims the camera and saves again.
#
# Run:  QT_QPA_PLATFORM=offscreen freecad set_view.py
###########################

import os

import FreeCAD as App
import FreeCADGui as Gui

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


def looking_from(back):
    """A camera turn that looks along -back, with the z axis up on the screen."""
    back = back.normalize()
    right = V(0, 0, 1).cross(back).normalize()
    up = back.cross(right)
    return App.Rotation(App.Matrix(right.x, up.x, back.x, 0, right.y, up.y, back.y, 0,
                                   right.z, up.z, back.z, 0, 0, 0, 0, 1))


# from the front, a little from the left and from above; x points backwards, y to the left
FRONT = looking_from(V(-2, 1, 1.2))


def save(doc, shown, turn=FRONT):
    """Aim a camera at the shown objects and save the document."""
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
    doc.save()


# stand.FCStd: show the base; the cradle and the knob are modelled in their own places and stay hidden
doc = App.openDocument(os.path.join(HERE, "stand.FCStd"))
for obj in doc.Objects:
    obj.ViewObject.Visibility = False
for body in doc.Objects:
    if body.isDerivedFrom("PartDesign::Body"):
        body.Tip.ViewObject.Visibility = True
        body.ViewObject.Visibility = body.Name == "Base"
save(doc, [doc.getObject("Base")])

# stand_preview.FCStd: light stand, dark panel, green outline of the Pi
doc = App.openDocument(os.path.join(HERE, "stand_preview.FCStd"))
colours = {"Base": (0.85, 0.85, 0.8), "Cradle": (0.30, 0.47, 0.66), "Panel": (0.15, 0.15, 0.15),
           "Pi_outline": (0.1, 0.5, 0.2)}
for obj in doc.Objects:
    obj.ViewObject.Visibility = True
    obj.ViewObject.ShapeColor = colours.get(obj.Name, (0.96, 0.52, 0.09))  # knobs orange
save(doc, doc.Objects)

os._exit(0)
