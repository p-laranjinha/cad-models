import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show

PIN_RADIUS = 2.5
PIN_DEPTH = 7.8
TOLERANCE = 0
CHAMFER_LENGTH = 0.4

part = Box(
    PIN_RADIUS * 6,
    PIN_RADIUS * 4,
    PIN_DEPTH * 2,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
) - Cylinder(
    PIN_RADIUS + TOLERANCE,
    PIN_DEPTH + CHAMFER_LENGTH,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)

part = chamfer(part.edges(), CHAMFER_LENGTH)

export_stl(part, os.path.splitext(__file__)[0] + ".stl")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
