import math
import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show

TOLERANCE = 0.4

WALL_THICKNESS = 3
SPACING = 30

WIRE_DIAMETER = 4.09 + TOLERANCE
WIRE_TOP_WIDTH = 63.13
WIRE_BOTTOM_WIDTH = 53.86
WIRE_HEIGHT = 30.71
EXTRA_WIRE_HEIGHT = 10

ANGLE = 90 - math.degrees(
    math.asin(
        WIRE_HEIGHT
        / (math.sqrt(WIRE_HEIGHT**2 + ((WIRE_TOP_WIDTH - WIRE_BOTTOM_WIDTH) / 2) ** 2))
    )
)

hole_right = Cylinder(
    WIRE_DIAMETER / 2, WIRE_HEIGHT + EXTRA_WIRE_HEIGHT, align=Align.MIN
)
hole_right = Rot(Y=ANGLE) * hole_right
hole_right = Pos((WIRE_BOTTOM_WIDTH / 2 - WIRE_DIAMETER)) * hole_right

hole_left = Cylinder(
    WIRE_DIAMETER / 2,
    WIRE_HEIGHT + EXTRA_WIRE_HEIGHT,
    align=(Align.MAX, Align.MIN, Align.MIN),
)
hole_left = Rot(Y=-ANGLE) * hole_left
hole_left = Pos(-(WIRE_BOTTOM_WIDTH / 2 - WIRE_DIAMETER)) * hole_left

holes = Part() + [hole_left, hole_right]

spacer = Box(
    WIRE_TOP_WIDTH + WALL_THICKNESS * 2,
    WIRE_DIAMETER + WALL_THICKNESS + SPACING,
    WIRE_HEIGHT / 2 + WALL_THICKNESS,
    align=(Align.CENTER, Align.MIN, Align.MIN),
)
spacer = Pos(Y=-WALL_THICKNESS, Z=-WALL_THICKNESS + WIRE_HEIGHT / 2) * spacer


part = cast(Part, spacer - holes)

part = chamfer(part.edges(), 0.48)

export_stl(part, os.path.splitext(__file__)[0] + ".stl")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
