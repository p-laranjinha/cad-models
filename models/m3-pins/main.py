from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore

# HOLE_WIDTH = 1.7 * 2 - 0.4
# BOARD_HOLE_DEPTH = 8.3
# PLATE_HOLE_DEPTH = 8
# TIP_STRAIGHT_WIDTH = 0.6
# TIP_OUT_WIDTH = 0.4
# BOARD_TIP_LENGTH = 1
# PLATE_TIP_LENGTH = 1


TOLERANCE = 0.1
SHELL_HOLE_DEPTH = 5
SHELL_HOLE_RADIUS = 2.15
SHELL_HOLE_OUTER_WIDTH = 8.2
HOLE_RADIUS = 1.7  # For the plate and board.
PLATE_CHAMFER_LENGTH = 1.45
PLATE_DEPTH = 3 + 0.2
BOARD_CHAMFER_LENGTH = 1.35
BOARD_DEPTH = 3.3 + 0.2

PIN_HEAD_LENGTH = 2
PIN_HOLE_RADIUS = PLATE_CHAMFER_LENGTH / 2 + TOLERANCE
PIN_HOLE_DEPTH = 3
PIN_HEIGHT = HOLE_RADIUS * 4 / 3


def make_pin(depth, chamfer_length):
    """Make a pin for either the plate or the board.
    depth -- The plate/board hole depth / height.
    chamfer_length -- The chamfer length.
    """
    part = Polyline(
        [
            (0, 0),
            (SHELL_HOLE_OUTER_WIDTH, 0),
            (SHELL_HOLE_OUTER_WIDTH, PIN_HEAD_LENGTH),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 + SHELL_HOLE_RADIUS - TOLERANCE,
                PIN_HEAD_LENGTH,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 + SHELL_HOLE_RADIUS - TOLERANCE,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH - TOLERANCE,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 + HOLE_RADIUS - TOLERANCE,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH - TOLERANCE,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 + HOLE_RADIUS - TOLERANCE,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth - chamfer_length,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 + HOLE_RADIUS + chamfer_length / 2,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth - chamfer_length / 2,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 + HOLE_RADIUS,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 - HOLE_RADIUS,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 - HOLE_RADIUS - chamfer_length / 2,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth - chamfer_length / 2,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 - HOLE_RADIUS + TOLERANCE,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth - chamfer_length,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 - HOLE_RADIUS + TOLERANCE,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH - TOLERANCE,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 - SHELL_HOLE_RADIUS + TOLERANCE,
                PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH - TOLERANCE,
            ),
            (
                SHELL_HOLE_OUTER_WIDTH / 2 - SHELL_HOLE_RADIUS + TOLERANCE,
                PIN_HEAD_LENGTH,
            ),
            (0, PIN_HEAD_LENGTH),
            (0, 0),
        ]
    ).edges()
    part = make_face(part)
    part = extrude(part, PIN_HEIGHT)
    part = Pos(Z=-PIN_HEIGHT / 2) * part

    pin_hole = Box(
        PIN_HOLE_RADIUS * 2,
        PIN_HOLE_DEPTH,
        PIN_HEIGHT,
        align=(Align.CENTER, Align.MIN, Align.CENTER),
    )
    pin_hole = (
        Pos(
            SHELL_HOLE_OUTER_WIDTH / 2,
            PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH + depth - PIN_HOLE_DEPTH,
        )
        * pin_hole
    )
    part -= pin_hole

    shell_hole = Cylinder(
        SHELL_HOLE_RADIUS + 10,
        SHELL_HOLE_DEPTH,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ) - Cylinder(
        SHELL_HOLE_RADIUS - TOLERANCE,
        SHELL_HOLE_DEPTH,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    shell_hole = (
        Pos(SHELL_HOLE_OUTER_WIDTH / 2, PIN_HEAD_LENGTH) * Rot(X=-90) * shell_hole
    )
    part -= shell_hole

    other_hole = Cylinder(
        HOLE_RADIUS + 10,
        depth - chamfer_length + TOLERANCE,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    ) - Cylinder(
        HOLE_RADIUS - TOLERANCE,
        depth - chamfer_length + TOLERANCE,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    other_hole = (
        Pos(SHELL_HOLE_OUTER_WIDTH / 2, PIN_HEAD_LENGTH + SHELL_HOLE_DEPTH - TOLERANCE)
        * Rot(X=-90)
        * other_hole
    )
    part -= other_hole

    part -= Pos(chamfer_length / 2 + TOLERANCE, depth - chamfer_length) * split(
        other_hole, Plane.YZ * Pos(Z=SHELL_HOLE_OUTER_WIDTH / 2)
    )

    part -= Pos(-(chamfer_length / 2 + TOLERANCE), depth - chamfer_length) * split(
        other_hole, Plane.YZ * Pos(Z=SHELL_HOLE_OUTER_WIDTH / 2), keep=Keep.BOTTOM
    )

    return cast(Part, part)


pin_insert = Box(
    PIN_HOLE_RADIUS,
    PIN_HOLE_DEPTH - TOLERANCE,
    PIN_HEIGHT,
    align=(Align.CENTER, Align.MIN, Align.CENTER),
)

export_step(
    pin_insert,
    os.path.dirname(os.path.realpath(__file__)) + "/m3-pin-insert.step",
)


board_pin = make_pin(BOARD_DEPTH, BOARD_CHAMFER_LENGTH)

export_step(
    board_pin,
    os.path.dirname(os.path.realpath(__file__)) + "/board-m3-pin.step",
)

plate_pin = make_pin(PLATE_DEPTH, PLATE_CHAMFER_LENGTH)

export_step(
    plate_pin,
    os.path.dirname(os.path.realpath(__file__)) + "/plate-m3-pin.step",
)

pin_insert.label = "pin_insert"
board_pin = Pos(-SHELL_HOLE_OUTER_WIDTH - 2 * PIN_HOLE_RADIUS) * board_pin
board_pin.label = "board_pin"
plate_pin = Pos(2 * PIN_HOLE_RADIUS) * plate_pin
plate_pin.label = "plate_pin"

show_all()
