from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore

HOLE_WIDTH = 1.7 * 2 - 0.4
BOARD_CHAMFER_LENGTH = 1.35
PLATE_CHAMFER_LENGTH = 1.45
BOARD_HOLE_DEPTH = 8.3
PLATE_HOLE_DEPTH = 8
TIP_STRAIGHT_WIDTH = 0.6
TIP_OUT_WIDTH = 0.4
BOARD_TIP_LENGTH = 1
PLATE_TIP_LENGTH = 1


def make_pin(chamfer_length, hole_depth, tip_length):
    part = Polyline(
        [
            (0, 0),
            (chamfer_length, chamfer_length),
            (chamfer_length, hole_depth),
            (
                chamfer_length - TIP_OUT_WIDTH,
                hole_depth + TIP_OUT_WIDTH / 2,
            ),
            (chamfer_length, hole_depth + TIP_OUT_WIDTH * 2),
            (chamfer_length + TIP_STRAIGHT_WIDTH, hole_depth + TIP_OUT_WIDTH * 2),
            (
                chamfer_length + TIP_STRAIGHT_WIDTH,
                hole_depth - tip_length + TIP_OUT_WIDTH * 2,
            ),
            (
                chamfer_length + HOLE_WIDTH - TIP_STRAIGHT_WIDTH,
                hole_depth - tip_length + TIP_OUT_WIDTH * 2,
            ),
            (
                chamfer_length + HOLE_WIDTH - TIP_STRAIGHT_WIDTH,
                hole_depth + TIP_OUT_WIDTH * 2,
            ),
            (
                chamfer_length + HOLE_WIDTH,
                hole_depth + TIP_OUT_WIDTH * 2,
            ),
            (
                chamfer_length + TIP_OUT_WIDTH + HOLE_WIDTH,
                hole_depth + TIP_OUT_WIDTH / 2,
            ),
            (
                chamfer_length + HOLE_WIDTH,
                hole_depth,
            ),
            (
                chamfer_length + HOLE_WIDTH,
                chamfer_length,
            ),
            (
                chamfer_length * 2 + HOLE_WIDTH,
                0,
            ),
            (0, 0),
        ]
    ).edges()
    part = make_face(part)
    part = extrude(part, HOLE_WIDTH * 2 / 3)
    part = Pos(Z=-HOLE_WIDTH * (2 / 3) / 2) * part
    part = part & Cylinder(
        HOLE_WIDTH / 2 + chamfer_length,
        hole_depth + TIP_OUT_WIDTH * 2,
        align=(Align.MIN, Align.CENTER, Align.MIN),
        rotation=(270, 0, 0),
    )
    part = cast(Part, part)
    cut = Pos(Y=chamfer_length) * Cylinder(
        HOLE_WIDTH / 2 + chamfer_length,
        hole_depth - chamfer_length,
        align=(Align.MIN, Align.CENTER, Align.MIN),
        rotation=(270, 0, 0),
    ) - Pos(chamfer_length, chamfer_length) * Cylinder(
        HOLE_WIDTH / 2,
        hole_depth - chamfer_length,
        align=(Align.MIN, Align.CENTER, Align.MIN),
        rotation=(270, 0, 0),
    )
    part -= cut
    part = part - Pos(TIP_OUT_WIDTH, TIP_OUT_WIDTH * 2) * split(
        cut, Plane.YZ * Pos(Z=HOLE_WIDTH / 2 + chamfer_length)
    )
    part = part - Pos(-TIP_OUT_WIDTH, TIP_OUT_WIDTH * 2) * split(
        cut, Plane.YZ * Pos(Z=HOLE_WIDTH / 2 + chamfer_length), keep=Keep.BOTTOM
    )
    return part


board_pin = make_pin(BOARD_CHAMFER_LENGTH, BOARD_HOLE_DEPTH, BOARD_TIP_LENGTH)

export_step(
    board_pin,
    os.path.dirname(os.path.realpath(__file__)) + "/board-m3-pin.step",
)

plate_pin = make_pin(PLATE_CHAMFER_LENGTH, PLATE_HOLE_DEPTH, PLATE_TIP_LENGTH)

export_step(
    plate_pin,
    os.path.dirname(os.path.realpath(__file__)) + "/plate-m3-pin.step",
)

board_pin = Pos(-HOLE_WIDTH) * board_pin
board_pin.label = "board_pin"
plate_pin = Pos(HOLE_WIDTH) * plate_pin
plate_pin.label = "plate_pin"
show([board_pin, plate_pin])
