import os
from build123d import *  # pyright: ignore
from yacv_server import show

THICKNESS = 3
WIDE_INNER_DIAMETER = 85.4
THIN_INNER_DIAMETER = 80
WIDE_LENGTH = 10
THIN_LENGTH = 80
CONNECTION_LENGTH = 10
WIDE_INNER_RADIUS = WIDE_INNER_DIAMETER / 2
THIN_INNER_RADIUS = THIN_INNER_DIAMETER / 2

wide_ring_inner = Circle(WIDE_INNER_RADIUS)
wide_ring_outer = Circle(WIDE_INNER_RADIUS + THICKNESS)
wide_ring = wide_ring_outer - wide_ring_inner

thin_ring_inner = Circle(THIN_INNER_RADIUS).move(Location((0, 0, -CONNECTION_LENGTH)))
thin_ring_outer = Circle(THIN_INNER_RADIUS + THICKNESS).move(
    Location((0, 0, -CONNECTION_LENGTH))
)
thin_ring = thin_ring_outer - thin_ring_inner

wide_cylinder = extrude(wide_ring, WIDE_LENGTH)
thin_cylinder = extrude(thin_ring, -THIN_LENGTH)
connection = loft([wide_ring_outer, thin_ring_outer]) - loft(
    [wide_ring_inner, thin_ring_inner]
)

part = wide_cylinder + connection + thin_cylinder

part.color = (0.3, 0.3, 0.3, 1)

show(part)  # pyright: ignore

export_stl(part, os.path.splitext(__file__)[0] + ".stl")
