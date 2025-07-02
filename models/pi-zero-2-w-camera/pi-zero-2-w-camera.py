import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show
from bd_warehouse.thread import IsoThread

TOLERANCE = 0.2

WALL_THICKNESS = 2

# PI_ZERO_2_W = import_step(
#     os.path.dirname(os.path.abspath(__file__)) + "/pi-zero-2-w.STEP"
# )
# Do not measure with yacv-server (very imprecise)
# Pi zero 2 w measurements from the cad model (on its side with the ports to the top):
BOARD_WIDTH = 65
BOARD_HEIGHT = 30
BOARD_DEPTH = 1.6 + 0.2  # +0.2 so it fits better
BOARD_DEPTH_AROUND_SCREW_HOLE = 1.58
BOARD_CORNER_RADIUS = 3
SCREW_HOLE_RADIUS = 2.7 / 2
SCREW_HOLE_X_OFFSET = 4.85 - SCREW_HOLE_RADIUS
SCREW_HOLE_Y_OFFSET = 4.85 - SCREW_HOLE_RADIUS
CAMERA_PORT_Y_OFFSET = 6.9
HDMI_PORT_X_OFFSET = 6.8
USB_PORT_1_X_OFFSET = 7.25
USB_PORT_2_X_OFFSET = 19.85
USB_PORT_WIDTH = 7.5
HDMI_PORT_WIDTH = 11.2
THIN_HEIGHT = 5.27  # The distance from the bottom to the top pin hole
HDMI_PORT_DEPTH = 5.05 - 1.6
USB_PORT_DEPTH = 4.05 - 1.6
CAMERA_PORT_DEPTH = 2.8 - 1.6
SD_CARD_SLOT_DEPTH = 3.05 - 1.6
SD_CARD_SLOT_TOP_Y_OFFSET = 11.07
SD_CARD_SLOT_BOTTOM_Y_OFFSET = 7.1
WIFI_MODULE_DEPTH = 3.2 - 1.6
WIFI_MODULE_TOP_Y_OFFSET = 7.2

# Off-brand IMX219 camera module measurements (port to the side):
CM_BOARD_WIDTH = 24.10
CM_BOARD_HEIGHT = 25.08
CM_BOARD_DEPTH = 0.97
CM_CAMERA_PORT_DEPTH = 3.59 - CM_BOARD_DEPTH
CM_CAMERA_PORT_WIDTH = 6
CM_CAMERA_PORT_Y_DISPLACEMENT = (
    1.25  # The camera port is tilted so we move the module slightly up
)
CM_CAMERA_LENS_WIDTH = 6.6
CM_CAMERA_LENS_X_OFFSET = 5.39
CM_THIN_WIDTH = 1.75
CM_THIN_HEIGHT = 1.25


def get_pi_enclosure():
    back_wall = [
        Line(
            (0, 0),
            (0, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
        ),
        RadiusArc(
            (0, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
            (BOARD_CORNER_RADIUS + WALL_THICKNESS, BOARD_HEIGHT + WALL_THICKNESS),
            BOARD_CORNER_RADIUS + WALL_THICKNESS,
        ),
        Line(
            (BOARD_CORNER_RADIUS + WALL_THICKNESS, BOARD_HEIGHT + WALL_THICKNESS),
            (
                BOARD_WIDTH - BOARD_CORNER_RADIUS + WALL_THICKNESS,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
        ),
        RadiusArc(
            (
                BOARD_WIDTH - BOARD_CORNER_RADIUS + WALL_THICKNESS,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
            BOARD_CORNER_RADIUS + WALL_THICKNESS,
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                0,
            ),
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                0,
            ),
            (BOARD_CORNER_RADIUS / 3 + WALL_THICKNESS, 0),
        ),
        Line(
            (BOARD_CORNER_RADIUS / 3 + WALL_THICKNESS, 0),
            (0, 0),
        ),
    ]
    back_wall = make_face(back_wall)
    back_wall = extrude(back_wall, WALL_THICKNESS)
    back_wall = cast(Part, Plane.XZ * back_wall)

    # WARN: The tolerance makes the side walls smaller than the defined thickness,
    # but its too much work to change that now.
    middle_walls = [
        Line(
            (0, 0),
            (0, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
        ),
        Line(
            (0, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
            (WALL_THICKNESS - TOLERANCE / 2, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
        ),
        Line(
            (WALL_THICKNESS - TOLERANCE / 2, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
            (WALL_THICKNESS - TOLERANCE / 2, WALL_THICKNESS - TOLERANCE),
        ),
        Line(
            (WALL_THICKNESS - TOLERANCE / 2, WALL_THICKNESS - TOLERANCE),
            (
                BOARD_WIDTH + WALL_THICKNESS + TOLERANCE / 2,
                WALL_THICKNESS - TOLERANCE,
            ),
        ),
        Line(
            (
                BOARD_WIDTH + WALL_THICKNESS + TOLERANCE / 2,
                WALL_THICKNESS - TOLERANCE,
            ),
            (
                BOARD_WIDTH + WALL_THICKNESS + TOLERANCE / 2,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
        ),
        Line(
            (
                BOARD_WIDTH + WALL_THICKNESS + TOLERANCE / 2,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                0,
            ),
        ),
        Line(
            (BOARD_WIDTH + 2 * WALL_THICKNESS, 0),
            (0, 0),
        ),
    ]
    middle_walls = make_face(middle_walls)
    middle_walls = extrude(middle_walls, BOARD_DEPTH)
    middle_walls = cast(Part, Plane.XZ * Pos(0, 0, WALL_THICKNESS) * middle_walls)
    # Add inside chamfers to hopefully stop the corners from buldging
    middle_walls = chamfer(
        middle_walls.edges()
        .filter_by(Axis.Z)
        .group_by(Axis.Y)[-1]
        .group_by(Axis.X)[-2],
        BOARD_DEPTH / 2,
    )
    middle_walls = chamfer(
        middle_walls.edges().filter_by(Axis.Z).group_by(Axis.Y)[-1].group_by(Axis.X)[1],
        BOARD_DEPTH / 2,
    )

    front_wall_bottom = [
        Line(
            (0, 0),
            (0, THIN_HEIGHT + WALL_THICKNESS),
        ),
        Line(
            (0, THIN_HEIGHT + WALL_THICKNESS),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                0,
            ),
        ),
        Line(
            (BOARD_WIDTH + 2 * WALL_THICKNESS, 0),
            (0, 0),
        ),
    ]
    front_wall_bottom = make_face(front_wall_bottom)
    front_wall_bottom = extrude(
        front_wall_bottom, WIFI_MODULE_DEPTH + WALL_THICKNESS + TOLERANCE
    )
    front_wall_bottom = cast(
        Part, Plane.XZ * Pos(0, 0, WALL_THICKNESS + BOARD_DEPTH) * front_wall_bottom
    )

    front_wall_left = [
        Line(
            (
                0,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (0, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
        ),
        RadiusArc(
            (0, BOARD_HEIGHT - BOARD_CORNER_RADIUS),
            (BOARD_CORNER_RADIUS + WALL_THICKNESS, BOARD_HEIGHT + WALL_THICKNESS),
            BOARD_CORNER_RADIUS + WALL_THICKNESS,
        ),
        Line(
            (BOARD_CORNER_RADIUS + WALL_THICKNESS, BOARD_HEIGHT + WALL_THICKNESS),
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                0,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
    ]
    front_wall_left = make_face(front_wall_left)
    front_wall_left = extrude(
        front_wall_left, WIFI_MODULE_DEPTH + WALL_THICKNESS - CAMERA_PORT_DEPTH
    )
    front_wall_left = cast(
        Part,
        Plane.XZ
        * Pos(0, 0, WALL_THICKNESS + BOARD_DEPTH + CAMERA_PORT_DEPTH + TOLERANCE)
        * front_wall_left,
    )

    front_wall_left2 = [
        Line(
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT - WIFI_MODULE_TOP_Y_OFFSET + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT - WIFI_MODULE_TOP_Y_OFFSET + WALL_THICKNESS,
            ),
            (
                USB_PORT_1_X_OFFSET + USB_PORT_WIDTH + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT - WIFI_MODULE_TOP_Y_OFFSET + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_1_X_OFFSET + USB_PORT_WIDTH + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT - WIFI_MODULE_TOP_Y_OFFSET + WALL_THICKNESS,
            ),
            (
                USB_PORT_1_X_OFFSET + USB_PORT_WIDTH + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_1_X_OFFSET + USB_PORT_WIDTH + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_1_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
    ]
    front_wall_left2 = make_face(front_wall_left2)
    front_wall_left2 = extrude(
        front_wall_left2, WIFI_MODULE_DEPTH + WALL_THICKNESS - WIFI_MODULE_DEPTH
    )
    front_wall_left2 = cast(
        Part,
        Plane.XZ
        * Pos(0, 0, WALL_THICKNESS + BOARD_DEPTH + WIFI_MODULE_DEPTH + TOLERANCE)
        * front_wall_left2,
    )

    front_wall_right = [
        Line(
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH - BOARD_CORNER_RADIUS + WALL_THICKNESS,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
        ),
        RadiusArc(
            (
                BOARD_WIDTH - BOARD_CORNER_RADIUS + WALL_THICKNESS,
                BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
            BOARD_CORNER_RADIUS + WALL_THICKNESS,
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - BOARD_CORNER_RADIUS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - SD_CARD_SLOT_TOP_Y_OFFSET + WALL_THICKNESS,
            ),
        ),
        RadiusArc(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                BOARD_HEIGHT - SD_CARD_SLOT_TOP_Y_OFFSET + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                SD_CARD_SLOT_BOTTOM_Y_OFFSET + WALL_THICKNESS,
            ),
            -(BOARD_HEIGHT - SD_CARD_SLOT_TOP_Y_OFFSET - SD_CARD_SLOT_BOTTOM_Y_OFFSET)
            / 1.3,
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                SD_CARD_SLOT_BOTTOM_Y_OFFSET + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
        Line(
            (
                BOARD_WIDTH + 2 * WALL_THICKNESS,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
    ]
    front_wall_right = make_face(front_wall_right)
    front_wall_right = extrude(
        front_wall_right, WIFI_MODULE_DEPTH + WALL_THICKNESS - SD_CARD_SLOT_DEPTH
    )
    front_wall_right = cast(
        Part,
        Plane.XZ
        * Pos(0, 0, WALL_THICKNESS + BOARD_DEPTH + SD_CARD_SLOT_DEPTH + TOLERANCE)
        * front_wall_right,
    )

    front_wall_left_curve = [
        Line(
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT / 2 + WALL_THICKNESS,
            ),
        ),
        RadiusArc(
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                BOARD_HEIGHT / 2 + WALL_THICKNESS,
            ),
            (
                USB_PORT_2_X_OFFSET
                + BOARD_HEIGHT / 2
                - THIN_HEIGHT
                + WALL_THICKNESS
                - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            -BOARD_HEIGHT / 3,
        ),
        Line(
            (
                USB_PORT_2_X_OFFSET
                + BOARD_HEIGHT / 2
                - THIN_HEIGHT
                + WALL_THICKNESS
                - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                USB_PORT_2_X_OFFSET + WALL_THICKNESS - TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
    ]
    front_wall_left_curve = make_face(front_wall_left_curve)
    front_wall_left_curve = extrude(
        front_wall_left_curve, WIFI_MODULE_DEPTH + WALL_THICKNESS - WIFI_MODULE_DEPTH
    )
    front_wall_left_curve = cast(
        Part,
        Plane.XZ
        * Pos(0, 0, WALL_THICKNESS + BOARD_DEPTH + WIFI_MODULE_DEPTH + TOLERANCE)
        * front_wall_left_curve,
    )

    front_wall_right_curve = [
        Line(
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT / 2 + WALL_THICKNESS,
            ),
        ),
        RadiusArc(
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                BOARD_HEIGHT / 2 + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH
                - HDMI_PORT_X_OFFSET
                - BOARD_HEIGHT / 2
                + THIN_HEIGHT
                + WALL_THICKNESS
                + TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            BOARD_HEIGHT / 3,
        ),
        Line(
            (
                BOARD_WIDTH
                - HDMI_PORT_X_OFFSET
                - BOARD_HEIGHT / 2
                + THIN_HEIGHT
                + WALL_THICKNESS
                + TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
            (
                BOARD_WIDTH - HDMI_PORT_X_OFFSET + WALL_THICKNESS + TOLERANCE,
                THIN_HEIGHT + WALL_THICKNESS,
            ),
        ),
    ]
    front_wall_right_curve = make_face(front_wall_right_curve)
    front_wall_right_curve = extrude(
        front_wall_right_curve, WIFI_MODULE_DEPTH + WALL_THICKNESS - SD_CARD_SLOT_DEPTH
    )
    front_wall_right_curve = cast(
        Part,
        Plane.XZ
        * Pos(0, 0, WALL_THICKNESS + BOARD_DEPTH + SD_CARD_SLOT_DEPTH + TOLERANCE)
        * front_wall_right_curve,
    )

    return Part() + [
        back_wall,
        middle_walls,
        front_wall_bottom,
        front_wall_left,
        front_wall_left2,
        front_wall_right,
        front_wall_left_curve,
        front_wall_right_curve,
    ]


def get_camera_module_enclosure():
    back_wall = Box(
        CM_BOARD_WIDTH + 2 * WALL_THICKNESS,
        WALL_THICKNESS,
        CM_BOARD_HEIGHT + WALL_THICKNESS,
        align=(Align.MIN, Align.MAX, Align.MIN),
    )

    middle_walls = Polyline(
        [
            (0, 0),
            (0, CM_BOARD_HEIGHT + WALL_THICKNESS),
            (WALL_THICKNESS - TOLERANCE / 2, CM_BOARD_HEIGHT + WALL_THICKNESS),
            (WALL_THICKNESS - TOLERANCE / 2, WALL_THICKNESS - TOLERANCE),
            (
                CM_BOARD_WIDTH + WALL_THICKNESS + TOLERANCE / 2,
                WALL_THICKNESS - TOLERANCE,
            ),
            (
                CM_BOARD_WIDTH + WALL_THICKNESS + TOLERANCE / 2,
                CM_BOARD_HEIGHT + WALL_THICKNESS,
            ),
            (CM_BOARD_WIDTH + 2 * WALL_THICKNESS, CM_BOARD_HEIGHT + WALL_THICKNESS),
            (CM_BOARD_WIDTH + 2 * WALL_THICKNESS, 0),
            (0, 0),
        ]
    )
    middle_walls = make_face(middle_walls.edges())
    middle_walls = extrude(middle_walls, CM_BOARD_DEPTH + TOLERANCE)
    middle_walls = cast(Part, Plane.XZ * Pos(0, 0, WALL_THICKNESS) * middle_walls)
    # Add inside chamfers to hopefully stop the corners from buldging
    middle_walls = chamfer(
        middle_walls.edges()
        .filter_by(Axis.Z)
        .group_by(Axis.Y)[-1]
        .group_by(Axis.X)[-2],
        CM_BOARD_DEPTH / 2,
    )
    middle_walls = chamfer(
        middle_walls.edges().filter_by(Axis.Z).group_by(Axis.Y)[-1].group_by(Axis.X)[1],
        CM_BOARD_DEPTH / 2,
    )
    middle_walls = chamfer(
        middle_walls.edges().filter_by(Axis.Z).group_by(Axis.Y)[0].group_by(Axis.X)[1],
        CM_BOARD_DEPTH / 2,
    )

    front_wall_bottom = Box(
        CM_BOARD_WIDTH + 2 * WALL_THICKNESS,
        CM_CAMERA_PORT_DEPTH + WALL_THICKNESS,
        CM_THIN_HEIGHT + WALL_THICKNESS,
        align=(Align.MIN, Align.MAX, Align.MIN),
    )
    front_wall_bottom = (
        Pos(0, -WALL_THICKNESS - CM_BOARD_DEPTH - TOLERANCE) * front_wall_bottom
    )

    front_wall_left = Box(
        CM_THIN_WIDTH + WALL_THICKNESS,
        CM_CAMERA_PORT_DEPTH + WALL_THICKNESS,
        CM_BOARD_HEIGHT - CM_THIN_HEIGHT,
        align=(Align.MIN, Align.MAX, Align.MIN),
    )
    front_wall_left = (
        Pos(
            0,
            -WALL_THICKNESS - CM_BOARD_DEPTH - TOLERANCE,
            CM_THIN_HEIGHT + WALL_THICKNESS,
        )
        * front_wall_left
    )

    front_wall_right = Box(
        CM_CAMERA_PORT_WIDTH + CM_THIN_WIDTH + WALL_THICKNESS,
        WALL_THICKNESS,
        CM_BOARD_HEIGHT - CM_THIN_HEIGHT,
        align=(Align.MIN, Align.MAX, Align.MIN),
    )
    front_wall_right = (
        Pos(
            CM_BOARD_WIDTH - CM_CAMERA_PORT_WIDTH - CM_THIN_WIDTH + WALL_THICKNESS,
            -WALL_THICKNESS - CM_BOARD_DEPTH - CM_CAMERA_PORT_DEPTH - TOLERANCE,
            CM_THIN_HEIGHT + WALL_THICKNESS,
        )
        * front_wall_right
    )

    return Part() + [
        back_wall,
        middle_walls,
        front_wall_bottom,
        front_wall_left,
        front_wall_right,
    ]


pi_enclosure = get_pi_enclosure()

pi_camera_module_enclosure = get_camera_module_enclosure()
pi_camera_module_enclosure = pi_camera_module_enclosure + Box(
    CM_BOARD_WIDTH + 2 * WALL_THICKNESS,
    CM_BOARD_DEPTH + CM_CAMERA_PORT_DEPTH + 2 * WALL_THICKNESS + TOLERANCE,
    (BOARD_HEIGHT - CM_BOARD_HEIGHT) / 2 + CM_CAMERA_PORT_Y_DISPLACEMENT,
    align=(Align.MIN, Align.MAX, Align.MAX),
)
pi_camera_module_enclosure = (
    Rot(Z=180)
    * Pos(
        -(CM_BOARD_WIDTH + 2 * WALL_THICKNESS)
        - BOARD_WIDTH / 2
        + (CM_BOARD_WIDTH - CM_CAMERA_LENS_X_OFFSET - CM_CAMERA_LENS_WIDTH / 2),
        WALL_THICKNESS,
        (BOARD_HEIGHT - CM_BOARD_HEIGHT) / 2 + CM_CAMERA_PORT_Y_DISPLACEMENT,
    )
    * pi_camera_module_enclosure
)

part = Part() + [pi_enclosure, pi_camera_module_enclosure]

INCH = 25.4

# Camera thread (ISO):
# 1/4 inch diameter
# 20 threads per inch
THREAD_DIAMETER = INCH / 4
THREAD_PITCH = INCH / 20
THREAD_LENGTH = INCH / 3


part += extrude(part.faces().filter_by(Plane.XY).sort_by(Axis.Z)[0], THREAD_LENGTH)
part = chamfer(part.edges().filter_by(Plane.XY).group_by(Axis.Z)[0], 0.48)

thread = IsoThread(
    THREAD_DIAMETER,
    THREAD_PITCH,
    THREAD_LENGTH,
    end_finishes=("chamfer", "chamfer"),
    external=False,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)
hole = Cylinder(
    THREAD_DIAMETER / 2,
    THREAD_LENGTH,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)
hole -= thread
hole = (
    Pos(
        (BOARD_WIDTH + 2 * WALL_THICKNESS) / 2,
        -(
            (2 * WALL_THICKNESS + BOARD_DEPTH + WIFI_MODULE_DEPTH + TOLERANCE)
            - (CM_BOARD_DEPTH + CM_CAMERA_PORT_DEPTH + TOLERANCE + WALL_THICKNESS)
        )
        / 2,
    )
    * hole
)

part -= hole

export_stl(part, os.path.splitext(__file__)[0] + ".stl")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
