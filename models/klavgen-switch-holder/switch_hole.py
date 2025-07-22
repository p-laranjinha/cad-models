from build123d import *  # pyright: ignore
from build123d import cast
from switch_holder import (
    CASE_THICKNESS,
    PLATE_FRONT_HOLE_DEPTH,
    PLATE_FRONT_HOLE_START_Y,
    PLATE_FRONT_HOLE_WIDTH,
    PLATE_SIDE_HOLE_DEPTH,
    PLATE_SIDE_HOLE_WIDTH,
    SWITCH_HOLE_DEPTH,
    SWITCH_HOLE_WIDTH,
)


def render_switch_hole():
    switch_hole = Box(
        SWITCH_HOLE_WIDTH,
        SWITCH_HOLE_DEPTH,
        CASE_THICKNESS,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )

    side_hole_left = Box(
        PLATE_SIDE_HOLE_WIDTH,
        PLATE_SIDE_HOLE_DEPTH,
        CASE_THICKNESS,
        align=Align.MIN,
    )
    side_hole_left = (
        Pos(-SWITCH_HOLE_WIDTH / 2 - PLATE_SIDE_HOLE_WIDTH, -SWITCH_HOLE_DEPTH / 2)
        * side_hole_left
    )
    switch_hole += side_hole_left

    side_hole_right = Box(
        PLATE_SIDE_HOLE_WIDTH,
        PLATE_SIDE_HOLE_DEPTH,
        CASE_THICKNESS,
        align=Align.MIN,
    )
    side_hole_right = (
        Pos(SWITCH_HOLE_WIDTH / 2, -SWITCH_HOLE_DEPTH / 2) * side_hole_right
    )
    switch_hole += side_hole_right

    front_hole = Box(
        PLATE_FRONT_HOLE_WIDTH,
        PLATE_FRONT_HOLE_DEPTH,
        CASE_THICKNESS,
        align=Align.MIN,
    )
    front_hole = Pos(-PLATE_FRONT_HOLE_WIDTH / 2, PLATE_FRONT_HOLE_START_Y) * front_hole
    switch_hole += front_hole

    switch_hole = Rot(Z=180) * switch_hole

    return cast(Compound, switch_hole)
