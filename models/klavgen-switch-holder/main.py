import os
from yacv_server import show
from build123d import *  # pyright: ignore
from build123d import cast
from switch_holder import (
    HOLDER_BOTTOM_HEIGHT,
    HOLDER_FRONT_LIP_HEIGHT,
    HOLDER_FRONT_LOCK_BUMP_WIDTH,
    HOLDER_LIPS_CHAMFER_TOP,
    HOLDER_DEPTH,
    HOLDER_HEIGHT,
    render_switch_holder,
)

NEW_HOLDER_FRONT_WALL_DEPTH = 1.2
HOLE_HEIGHT = 2
HOLE_WIDTH = 4.2
HOLE_DISTANCE_FROM_TOP = 0.9
FRONT_LIP_EXTRA_HEIGHT = 0.2  # Added unnecessary height so the lip looks more flush

holder = render_switch_holder()

front_lip = Box(
    HOLDER_FRONT_LOCK_BUMP_WIDTH,
    NEW_HOLDER_FRONT_WALL_DEPTH,
    HOLDER_FRONT_LIP_HEIGHT
    + HOLDER_HEIGHT
    - HOLDER_BOTTOM_HEIGHT
    + FRONT_LIP_EXTRA_HEIGHT,
    align=(Align.CENTER, Align.MIN, Align.MIN),
)
front_lip = (
    Pos(0, -HOLDER_DEPTH / 2, HOLDER_HEIGHT - HOLDER_HEIGHT + HOLDER_BOTTOM_HEIGHT)
    * front_lip
)
front_lip = chamfer(
    front_lip.edges().group_by(Axis.Y)[0].group_by(Axis.Z)[-1].filter_by(Axis.X),
    HOLDER_LIPS_CHAMFER_TOP,
)
holder += front_lip

front_hole = Box(
    HOLE_WIDTH,
    NEW_HOLDER_FRONT_WALL_DEPTH,
    HOLE_HEIGHT,
    align=(Align.CENTER, Align.MIN, Align.MIN),
)
front_hole = (
    Pos(
        0,
        -HOLDER_DEPTH / 2,
        HOLDER_HEIGHT + HOLDER_FRONT_LIP_HEIGHT - HOLE_HEIGHT - HOLE_DISTANCE_FROM_TOP,
    )
    * front_hole
)
holder -= cast(Part, front_hole)

holder = Rot(Z=180) * Rot(X=90) * Pos(Y=HOLDER_DEPTH / 2, Z=-HOLDER_HEIGHT / 2) * holder

part = holder

export_stl(
    part, os.path.dirname(os.path.realpath(__file__)) + "/klavgen_switch_holder.stl"
)

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
