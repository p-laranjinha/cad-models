import math
from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore


SCREW_HOLE_RADIUS = 4.5 / 2
SCREW_HOLE_CHAMFER_RADIUS = 7.5 / 2
BAR_WIDTH = 14.95
BAR_HEIGHT = 29.5
GAP_LENGTH_BETWEEN_HOLES = 14
PEG_BOTTOM_RADIUS = 7.5 / 2
PEG_TOP_RADIUS = 6 / 2
PEG_HEIGHT = 7.8
PLATE_DEPTH = 2.5
WALL_SIDE_WIDTH = 5
WALL_BOTTOM_WIDTH = 10
WALL_HEIGHT = 20


plate = Box(
    BAR_WIDTH + WALL_SIDE_WIDTH * 2, BAR_HEIGHT + WALL_BOTTOM_WIDTH, PLATE_DEPTH
)
plate = Pos(Y=-WALL_BOTTOM_WIDTH / 2) * plate

screw_hole = Cone(SCREW_HOLE_RADIUS, SCREW_HOLE_CHAMFER_RADIUS, PLATE_DEPTH)
plate -= Pos(Y=GAP_LENGTH_BETWEEN_HOLES / 2 + SCREW_HOLE_RADIUS) * screw_hole
plate -= Pos(Y=-GAP_LENGTH_BETWEEN_HOLES / 2 - SCREW_HOLE_RADIUS) * screw_hole

peg = Cone(PEG_TOP_RADIUS, PEG_BOTTOM_RADIUS, PEG_HEIGHT)
peg = Pos(Z=-PLATE_DEPTH / 2 - PEG_HEIGHT / 2) * peg

walls = Box(
    BAR_WIDTH + WALL_SIDE_WIDTH * 2, BAR_HEIGHT + WALL_BOTTOM_WIDTH, WALL_HEIGHT
)
walls = Pos(Y=-WALL_BOTTOM_WIDTH / 2, Z=WALL_HEIGHT / 2 + PLATE_DEPTH / 2) * walls
walls_removed = [
    Line(
        (-BAR_WIDTH / 2, BAR_HEIGHT / 2),
        (-BAR_WIDTH / 2, -BAR_HEIGHT / 2 + BAR_WIDTH / 2),
    ),
    RadiusArc(
        (-BAR_WIDTH / 2, -BAR_HEIGHT / 2 + BAR_WIDTH / 2),
        (BAR_WIDTH / 2, -BAR_HEIGHT / 2 + BAR_WIDTH / 2),
        -BAR_WIDTH / 2,
    ),
    Line(
        (BAR_WIDTH / 2, BAR_HEIGHT / 2),
        (BAR_WIDTH / 2, -BAR_HEIGHT / 2 + BAR_WIDTH / 2),
    ),
    Line((-BAR_WIDTH / 2, BAR_HEIGHT / 2), (BAR_WIDTH / 2, BAR_HEIGHT / 2)),
]
walls_removed = make_face(walls_removed)
walls_removed = extrude(walls_removed, WALL_HEIGHT)
walls_removed = Pos(Z=PLATE_DEPTH / 2) * walls_removed

walls -= walls_removed

part = Part() + [plate, walls, peg]
part = Rot(90) * part

export_step(
    part,
    os.path.dirname(os.path.realpath(__file__)) + "/closet-rod-holder.step",
)

show(part)
