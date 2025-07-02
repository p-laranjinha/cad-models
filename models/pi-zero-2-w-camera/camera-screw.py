import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show
from bd_warehouse.thread import *
from bd_warehouse.fastener import *

INCH = 25.4

TOLERANCE = 0.2


def get_inner_thread_diameter(outer_diameter, pitch):
    thread_height = sqrt(3) / 2 * pitch
    return outer_diameter - 2 * (5 / 8 * thread_height)


# Camera thread (ISO):
# 1/4 inch diameter
# 20 threads per inch
# 1/4 inch length
thread = IsoThread(
    INCH / 4 - TOLERANCE,
    INCH / 20,
    INCH / 4,
    end_finishes=("fade", "fade"),
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

core_1 = Cylinder(
    get_inner_thread_diameter(INCH / 4 - TOLERANCE, INCH / 20) / 2,
    INCH / 4,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
core_2 = Pos(Z=INCH / 4) * Cylinder(
    (INCH / 4) / 2 - TOLERANCE,
    INCH / 3 - INCH / 4,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

top = Pos(Z=INCH / 3) * Cylinder(
    INCH / 4,
    INCH / 8,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)
# top = split(cast(Solid, top), Plane.YZ.offset(-INCH / 6))
# top = split(cast(Solid, top), Plane.ZY.offset(-INCH / 6))

part = Part() + [thread, core_1, core_2, top]

part = split(cast(Solid, part), Plane.XZ.offset(-INCH / 12))
part = split(cast(Solid, part), Plane.ZX.offset(-INCH / 12))

part = Pos(Z=INCH / 12) * Rot(X=90) * part

export_stl(part, os.path.splitext(__file__)[0] + ".stl")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
