from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore

HEIGHT = 50
WIDTH = 30
HOLE_HEIGHT = 30
HOLE_OFFSET = 5.9
CHAMFER_LENGTH = 2

stopper = Triangle(a=HEIGHT, c=HEIGHT, B=90, align=Align.MIN)
stopper = extrude(stopper, WIDTH)
stopper = chamfer(stopper.edges(), CHAMFER_LENGTH)

hole = Triangle(a=HOLE_HEIGHT, c=HOLE_HEIGHT, B=90, align=Align.MIN)
hole = extrude(hole, WIDTH)
hole = Pos(X=HOLE_OFFSET, Y=HOLE_OFFSET, Z=WIDTH - CHAMFER_LENGTH) * hole
hole = chamfer(hole.edges(), CHAMFER_LENGTH)

part = stopper - hole


export_step(
    part,
    os.path.dirname(os.path.realpath(__file__)) + "/trays-stopper.step",
)

show(part)
