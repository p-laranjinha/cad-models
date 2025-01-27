import os
from build123d import *  # pyright: ignore
from yacv_server import show

PHONE_WIDTH = 69.1
MODEL_PHONE_ACTUAL_WIDTH = 68.7
PHONE_HEIGHT = 151.7
MODEL_PHONE_ACTUAL_HEIGHT = 151.92
PHONE_DEPTH = 10.14 - 1.94  # 8.2 # excluding camera
MODEL_PHONE_ACTUAL_DEPTH = 7.94  # excluding camera

MODEL_PHONE_WIDTH = 69.6
MODEL_PHONE_HEIGHT = 151.7
MODEL_PHONE_DEPTH = 9.1  # including camera

phone = scale(
    (Mesher(Unit.M).read(os.path.dirname(os.path.abspath(__file__)) + "/phone.stl")[0]),
    (
        PHONE_WIDTH / MODEL_PHONE_ACTUAL_WIDTH,
        PHONE_HEIGHT / MODEL_PHONE_ACTUAL_HEIGHT,
        PHONE_DEPTH / MODEL_PHONE_ACTUAL_DEPTH,
    ),
).move(
    Location(
        (0, 0, -(MODEL_PHONE_DEPTH * PHONE_DEPTH / MODEL_PHONE_ACTUAL_DEPTH) / 2 + 0.7)
    )
)
cover = chamfer(
    fillet(
        fillet(
            extrude(
                Rectangle(MODEL_PHONE_WIDTH + 1.2, MODEL_PHONE_HEIGHT + 2),
                -MODEL_PHONE_DEPTH - 0.5,
            )
            .move(Location((0, 0, 0.5)))
            .edges()
            .filter_by(Axis.Z),
            7,
        )
        .edges()
        .filter_by(Plane.XY)
        .group_by(Axis.Z)[-1],
        2,
    )
    .edges()
    .filter_by(Plane.XY)
    .group_by(Axis.Z)[0],
    2,
)
right_hole = (
    (extrude(Rectangle(8, 50.5), -5.5).move(Location((34, 28.5, 0.5))))
    - fillet(
        extrude(Rectangle(8, 8), -6)
        .move(Location((34, 3.5, 0.5)))
        .edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.Y)[-1],
        4,
    )
    - fillet(
        extrude(Rectangle(8, 8), -6)
        .move(Location((34, 54, 0.5)))
        .edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.Y)[0],
        4,
    )
    + fillet(
        extrude(Rectangle(8, 42.5), -10)
        .move(Location((38, 28.5)))
        .edges()
        .filter_by(Axis.Z)
        .group_by(Axis.X)[0],
        1,
    )
)
bottom_hole = (
    (extrude(Rectangle(58, 8), -7.5).move(Location((0, -74, 0.5))))
    - fillet(
        extrude(Rectangle(8, 8), -7.5)
        .move(Location((29, -74, 0.5)))
        .edges()
        .filter_by(Axis.Y)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.X)[0],
        5,
    )
    - fillet(
        extrude(Rectangle(8, 8), -7.5)
        .move(Location((-29, -74, 0.5)))
        .edges()
        .filter_by(Axis.Y)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.X)[-1],
        5,
    )
    + fillet(
        extrude(Rectangle(50, 8), -10)
        .move(Location((0, -79.5)))
        .edges()
        .filter_by(Axis.Z)
        .group_by(Axis.Y)[-1],
        1,
    )
    # + chamfer(
    #     extrude(Rectangle(50, 8), -2.4).move(Location((0, -79.5 + 1, -9.4 + 1))).edges()
    #     # .filter_by(Axis.X)
    #     .group_by(Axis.Z)[-1],
    #     1,
    # )
)

top_hole = extrude(Circle(1).rotate(Axis.X, 90), 8).move(Location((13, 80, -3.3)))

screen_hole = fillet(
    extrude(Rectangle(66.8, 147.7), 2, both=True).edges().filter_by(Axis.Z), 7
)

inside_back_flattener = fillet(
    extrude(Rectangle(64.8, 147.7), -8.2).edges().filter_by(Axis.Z), 7
)

part = (
    cover
    - phone
    - right_hole
    - bottom_hole
    - top_hole
    - screen_hole
    - inside_back_flattener
)
part.color = (0.3, 0.3, 0.3, 1)

phone.color = (0, 0, 0, 1)

show(part, phone)  # pyright: ignore

export_stl(part, os.path.splitext(__file__)[0] + ".stl")
