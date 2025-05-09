import os
from build123d import *  # pyright: ignore
from yacv_server import show

THICKNESS_SIDE = 1
THICKNESS_BACK = 0.1  # after camera
THICKNESS_FRONT = 0
BUTTONS_SIDE_SPACING = 2

# From the points positions in blender
DEPTH_OFFSET = 4.08092
DEPTH_MIN = -4.08092 + DEPTH_OFFSET
DEPTH_MAX = 4.12907 + DEPTH_OFFSET
DEPTH_MAX_CAMERA = 5.31708 + DEPTH_OFFSET
WIDTH_OFFSET = 0.170975
WIDTH_MIN = -34.927 + WIDTH_OFFSET
WIDTH_MAX = 34.585 + WIDTH_OFFSET
WIDTH_MAX_BUTTON = 35.067 + WIDTH_OFFSET
HEIGHT_MIN = -75.7908
HEIGHT_MAX = 75.6533
CAMERA_WIDTH_MIN = 10.019 + WIDTH_OFFSET
CAMERA_WIDTH_MAX = 27.299 + WIDTH_OFFSET
CAMERA_HEIGHT_MIN = 34.1492 - 0.3
CAMERA_HEIGHT_MAX = 68.7772 + 0.1
BUTTONS_HEIGHT_MIN = 9.09528
BUTTONS_HEIGHT_MAX = 47.9932
TOP_HOLE_DEPTH_MIN = -4.186
TOP_HOLE_DEPTH_MAX = -2.794
TOP_HOLE_MIN_WIDTH = 12.6

# ACTUAL_PHONE_WIDTH = 69.1
# ACTUAL_PHONE_HEIGHT = 151.7
# ACTUAL_PHONE_DEPTH = 10.14 - 1.94  # 8.2 # excluding camera

phone = Mesher(Unit.M).read(os.path.dirname(os.path.abspath(__file__)) + "/phone.stl")[
    0
]
cover = make_face(
    Polyline(
        [
            (WIDTH_MIN - THICKNESS_SIDE, HEIGHT_MIN - THICKNESS_SIDE),
            (WIDTH_MAX + THICKNESS_SIDE, HEIGHT_MIN - THICKNESS_SIDE),
            (WIDTH_MAX + THICKNESS_SIDE, HEIGHT_MAX + THICKNESS_SIDE),
            (WIDTH_MIN - THICKNESS_SIDE, HEIGHT_MAX + THICKNESS_SIDE),
            (WIDTH_MIN - THICKNESS_SIDE, HEIGHT_MIN - THICKNESS_SIDE),
        ]
    ).edges()
)
cover = extrude(
    cover, -(DEPTH_MAX_CAMERA - DEPTH_MIN + THICKNESS_BACK + THICKNESS_FRONT)
).move(Location((0, 0, THICKNESS_FRONT)))
cover = fillet(
    chamfer(
        fillet(
            fillet(
                cover.edges().filter_by(Axis.Z),
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
        1.3,
        2,
    )
    .edges()
    .filter_by(Plane.XY)
    .group_by(Axis.Z)[1],
    1.3,
)

right_hole = (
    extrude(
        Rectangle(
            8,
            BUTTONS_HEIGHT_MAX - BUTTONS_HEIGHT_MIN + BUTTONS_SIDE_SPACING * 2 + 8,
            align=(Align.MAX, Align.MIN),
        ),
        -5 - THICKNESS_FRONT,
    ).move(
        Location(
            (
                WIDTH_MAX + THICKNESS_SIDE,
                BUTTONS_HEIGHT_MIN - BUTTONS_SIDE_SPACING - 4,
                THICKNESS_FRONT,
            )
        )
    )
    + extrude(
        Rectangle(
            8,
            BUTTONS_HEIGHT_MAX - BUTTONS_HEIGHT_MIN + BUTTONS_SIDE_SPACING * 2,
            align=(Align.MAX, Align.MIN),
        ),
        -5.5 - THICKNESS_FRONT,
    ).move(
        Location(
            (
                WIDTH_MAX + THICKNESS_SIDE,
                BUTTONS_HEIGHT_MIN - BUTTONS_SIDE_SPACING,
                THICKNESS_FRONT,
            )
        )
    )
    - fillet(
        extrude(Rectangle(8, 8, align=(Align.MAX, Align.MIN)), -6)
        .move(
            Location(
                (
                    WIDTH_MAX + THICKNESS_SIDE,
                    BUTTONS_HEIGHT_MAX + BUTTONS_SIDE_SPACING,
                    THICKNESS_FRONT,
                )
            )
        )
        .edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.Y)[0],
        4,
    )
    + fillet(
        extrude(
            Rectangle(
                8,
                BUTTONS_HEIGHT_MAX - BUTTONS_HEIGHT_MIN + BUTTONS_SIDE_SPACING * 2,
                align=(Align.MIN, Align.MIN),
            ),
            -(DEPTH_MAX_CAMERA - DEPTH_MIN + THICKNESS_FRONT + THICKNESS_BACK),
        )
        .move(
            Location(
                (
                    WIDTH_MAX + THICKNESS_SIDE - 1.4,
                    BUTTONS_HEIGHT_MIN - BUTTONS_SIDE_SPACING,
                    THICKNESS_FRONT,
                )
            )
        )
        .edges()
        .filter_by(Axis.Z)
        .group_by(Axis.X)[0],
        1,
    )
)

bottom_hole = (
    (
        extrude(
            Rectangle(58, 8, align=(Align.CENTER, Align.MIN)), -7 - THICKNESS_FRONT
        ).move(Location((0, HEIGHT_MIN - THICKNESS_SIDE, THICKNESS_FRONT)))
    )
    - fillet(
        extrude(Rectangle(8, 8), -7 - THICKNESS_FRONT)
        .move(Location((29, HEIGHT_MIN - THICKNESS_SIDE, THICKNESS_FRONT)))
        .edges()
        .filter_by(Axis.Y)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.X)[0],
        5,
    )
    - fillet(
        extrude(Rectangle(8, 8, align=(Align.CENTER, Align.MIN)), -7 - THICKNESS_FRONT)
        .move(Location((-29, HEIGHT_MIN - THICKNESS_SIDE, THICKNESS_FRONT)))
        .edges()
        .filter_by(Axis.Y)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.X)[-1],
        5,
    )
    + fillet(
        extrude(
            Rectangle(50, 8, align=(Align.CENTER, Align.MAX)),
            -(DEPTH_MAX_CAMERA - DEPTH_MIN + THICKNESS_FRONT + THICKNESS_BACK),
        )
        .move(Location((0, HEIGHT_MIN - THICKNESS_SIDE + 1.4)))
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

top_hole = extrude(Circle(1).rotate(Axis.X, 90), 8).move(
    Location(
        (
            TOP_HOLE_MIN_WIDTH + (TOP_HOLE_DEPTH_MAX - TOP_HOLE_DEPTH_MIN) / 2,
            HEIGHT_MAX + THICKNESS_SIDE,
            TOP_HOLE_DEPTH_MAX - (TOP_HOLE_DEPTH_MAX - TOP_HOLE_DEPTH_MIN) / 2,
        )
    )
)

screen_hole = fillet(
    extrude(Rectangle(67.3, 147.7), 2, both=True).edges().filter_by(Axis.Z), 7
)

inside_back_flattener = fillet(
    extrude(Rectangle(64.8, 147.7), -DEPTH_MAX).edges().filter_by(Axis.Z), 7
)

camera_hole = fillet(
    extrude(
        make_face(
            Polyline(
                [
                    (CAMERA_WIDTH_MIN, CAMERA_HEIGHT_MIN),
                    (CAMERA_WIDTH_MAX, CAMERA_HEIGHT_MIN),
                    (CAMERA_WIDTH_MAX, CAMERA_HEIGHT_MAX),
                    (CAMERA_WIDTH_MIN, CAMERA_HEIGHT_MAX),
                    (CAMERA_WIDTH_MIN, CAMERA_HEIGHT_MIN),
                ]
            ).edges()
        ).move(Location((0, 0, -DEPTH_MAX))),
        -(DEPTH_MAX_CAMERA - DEPTH_MAX + THICKNESS_BACK),
    )
    .edges()
    .filter_by(Axis.Z),
    4.5,
)

weird_button_hole_rounded_corner_that_doesnt_work = (
    fillet(
        extrude(Rectangle(8, 8), -6)
        .move(
            Location(
                (
                    WIDTH_MAX + THICKNESS_SIDE - 4,
                    BUTTONS_HEIGHT_MIN - BUTTONS_SIDE_SPACING - 4,
                    THICKNESS_FRONT,
                )
            )
        )
        .edges()
        .filter_by(Axis.X)
        .group_by(Axis.Z)[-1]
        .group_by(Axis.Y)[-1],
        4,
    )
    & cover
) - phone.move(Location((0, 60)))
phone.move(Location((0, -60)))

part = (
    cover
    - right_hole
    + weird_button_hole_rounded_corner_that_doesnt_work
    - phone
    - bottom_hole
    - screen_hole
    # - inside_back_flattener
    - camera_hole
    - top_hole
)

part.color = (0.3, 0.3, 0.3, 1)
phone.color = (0, 0, 0, 1)
show(part)  # pyright: ignore

export_stl(part, os.path.splitext(__file__)[0] + ".stl")
