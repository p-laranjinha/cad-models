import os
from build123d import (
    Axis,
    Circle,
    Location,
    Mesher,
    Plane,
    Rectangle,
    Unit,
    export_stl,
    extrude,
    fillet,
)
from yacv_server import show

PHONE_WIDTH = 69.6
PHONE_HEIGHT = 151.7
PHONE_DEPTH = 9.1  # including camera

phone = (
    Mesher(Unit.M)
    .read(os.path.dirname(os.path.abspath(__file__)) + "/phone.stl")[0]
    .move(Location((0, 0, -PHONE_DEPTH / 2 + 0.7)))
)
cover = fillet(
    fillet(
        extrude(Rectangle(PHONE_WIDTH + 1, PHONE_HEIGHT + 2), -PHONE_DEPTH + 0.15)
        .edges()
        .filter_by(Axis.Z),
        5,
    )
    .edges()
    .filter_by(Plane.XY),
    2,
)
right_hole = fillet(
    extrude(Rectangle(8, 42), -6)
    .move(Location((34, 29)))
    .edges()
    .filter_by(Axis.X)
    .group_by(Axis.Z)[0],
    3,
)
bottom_hole = fillet(
    extrude(Rectangle(50, 8), -7)
    .move(Location((0, -74)))
    .edges()
    .filter_by(Axis.Y)
    .group_by(Axis.Z)[0],
    3,
)
top_hole = extrude(Circle(1).rotate(Axis.X, 90), 8).move(Location((13, 80, -3.3)))

part = (
    cover
    - phone
    # - phone.move(Location((0, 0, 1)))
    - right_hole
    - bottom_hole
    - top_hole
).scale(1.01449)
part.color = (0.3, 0.3, 0.3, 1)

phone.color = (0, 0, 0, 1)

show(part, phone)  # pyright: ignore

export_stl(part, os.path.splitext(__file__)[0] + ".stl")
