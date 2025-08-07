import math
from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore


DEPTH = 31
WIDTH = 95
# HEIGHT = 61
CORNER_RADIUS = 22
CORNER_ARC_SIZE = 160
CORNER_ROTATION = 45
BASE_LIP_DEPTH = 5
CUSHION_FILLET_RADIUS = 10
CUSHION_DEPTH = CUSHION_FILLET_RADIUS + BASE_LIP_DEPTH
BASE_THICKNESS = 3
BOTTOM_CHAMFER_LENGTH = 0.5

left = CenterArc((0, 0), CORNER_RADIUS, -CORNER_ROTATION, -CORNER_ARC_SIZE)
left = Pos(CORNER_RADIUS, CORNER_RADIUS) * left

right = CenterArc((0, 0), CORNER_RADIUS, CORNER_ROTATION - 180, CORNER_ARC_SIZE)
right = Pos(WIDTH - CORNER_RADIUS, CORNER_RADIUS) * right

# top = SagittaArc(left @ 1, right @ 1, HEIGHT - (left @ 1).Y)
top = TangentArc(
    left @ 1,
    right @ 1,
    tangent=(
        math.cos(math.radians(CORNER_ROTATION + (180 - CORNER_ARC_SIZE))),
        math.sin(math.radians(CORNER_ROTATION + (180 - CORNER_ARC_SIZE))),
    ),
)
bottom = TangentArc(
    left @ 0,
    right @ 0,
    tangent=(
        math.cos(math.radians(CORNER_ROTATION)),
        math.sin(math.radians(CORNER_ROTATION)),
    ),
)

cushion_face = make_face([left, right, top, bottom])

cushion = extrude(cushion_face, CUSHION_DEPTH)
cushion = fillet(cushion.edges().group_by(Axis.Z)[-1], CUSHION_FILLET_RADIUS)
cushion = chamfer(cushion.edges().group_by(Axis.Z)[0], BOTTOM_CHAMFER_LENGTH)

base_face = offset(cushion_face, BASE_THICKNESS) - cushion_face

base = extrude(cushion_face, -DEPTH + CUSHION_DEPTH)
base += extrude(base_face, -DEPTH + CUSHION_DEPTH)
base += extrude(base_face, BASE_LIP_DEPTH)
base = chamfer(base.edges().group_by(Axis.Z)[0], BOTTOM_CHAMFER_LENGTH)


export_step(
    cushion,
    os.path.dirname(os.path.realpath(__file__)) + "/wrist-rest-cushion.step",
)

export_step(
    base,
    os.path.dirname(os.path.realpath(__file__)) + "/wrist-rest-base.step",
)

show(cushion, base)
