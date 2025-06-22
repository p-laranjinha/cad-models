from math import pi
import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show


HANDLE_RADIUS = 42.2 / 2

MIDDLE_RING_OUTER_RADIUS = 45.2 / 2
MIDDLE_RING_WIDTH = 1
MIDDLE_RING_HEIGHT = 1.5

INNER_HOLE_RADIUS = MIDDLE_RING_OUTER_RADIUS - MIDDLE_RING_WIDTH - 2
INNER_HOLE_HEIGHT = 4 + MIDDLE_RING_HEIGHT
INNER_HOLE_GAP = 13

OUTER_RADIUS = MIDDLE_RING_OUTER_RADIUS + 4
HEIGHT = INNER_HOLE_HEIGHT + 4


def arc_angle(length, radius):
    return length / radius * 180 / pi


inner_ring_slice = cast(
    Rectangle,
    Plane.YZ
    * Pos(INNER_HOLE_RADIUS, MIDDLE_RING_HEIGHT)
    * Rectangle(
        MIDDLE_RING_OUTER_RADIUS - MIDDLE_RING_WIDTH - INNER_HOLE_RADIUS,
        INNER_HOLE_HEIGHT - MIDDLE_RING_HEIGHT,
        align=Align.MIN,
    ),
)
# The radius doesn't matter for this sweep
inner_ring_path = CenterArc(
    (0, 0), 10, 90, -360 + arc_angle(INNER_HOLE_GAP, INNER_HOLE_RADIUS)
)
inner_ring = sweep(inner_ring_slice, inner_ring_path)

outer_ring_slice = cast(
    Sketch,
    Plane.YZ
    * make_face(
        [
            Line(
                (MIDDLE_RING_OUTER_RADIUS - MIDDLE_RING_WIDTH, MIDDLE_RING_HEIGHT),
                (MIDDLE_RING_OUTER_RADIUS, MIDDLE_RING_HEIGHT),
            ),
            Line(
                (MIDDLE_RING_OUTER_RADIUS, MIDDLE_RING_HEIGHT),
                (MIDDLE_RING_OUTER_RADIUS, 0),
            ),
            Line((MIDDLE_RING_OUTER_RADIUS, 0), (OUTER_RADIUS, 0)),
            Line((OUTER_RADIUS, 0), (HANDLE_RADIUS, HEIGHT)),
            Line((HANDLE_RADIUS, HEIGHT), (HANDLE_RADIUS, INNER_HOLE_HEIGHT)),
            Line(
                (HANDLE_RADIUS, INNER_HOLE_HEIGHT),
                (MIDDLE_RING_OUTER_RADIUS - MIDDLE_RING_WIDTH, INNER_HOLE_HEIGHT),
            ),
            Line(
                (MIDDLE_RING_OUTER_RADIUS - MIDDLE_RING_WIDTH, INNER_HOLE_HEIGHT),
                (MIDDLE_RING_OUTER_RADIUS - MIDDLE_RING_WIDTH, MIDDLE_RING_HEIGHT),
            ),
        ]
    ),
)
# The radius doesn't matter for this sweep
outer_ring_path = Circle(10).edge()
outer_ring = sweep(outer_ring_slice, outer_ring_path)

cut = Rot(0, 0, 180) * Box(
    0.5, OUTER_RADIUS, HEIGHT, align=(Align.CENTER, Align.MIN, Align.MIN)
)

part = inner_ring + outer_ring - cut

export_step(part, os.path.splitext(__file__)[0] + ".step")

part.color = (0.3, 0.3, 0.3, 1)
show([part])  # pyright: ignore
