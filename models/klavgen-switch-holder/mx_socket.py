from build123d import *  # pyright: ignore

# Kailh socket heights
SOCKET_HEIGHT = 1.8
SOCKET_BUMP_HEIGHT = 1

PIN_TOP_CLEARANCE_HEIGHT = 0.4

# Kailh socket outline, including solder pins
FRONT_FLAT_WIDTH = 9.50

RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN = 0.9
RIGHT_FLAT_DEPTH_SOLDER_PIN = 2.6
RIGHT_FLAT_DEPTH_BEHIND_SOLDER_PIN = 0.5

LEFT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN = 0.4
LEFT_FLAT_DEPTH_BEHIND_SOLDER_PIN = 1.2

BACK_RIGHT_FLAT_WIDTH = 4.00

LARGE_RADIUS = 2
SMALL_RADIUS = 1.8

SOLDER_PIN_WIDTH = 4.00

# Switch pin bumps
SOCKET_BUMP_RADIUS = 1.6

SOCKET_BUMP_1_X = 2.6
SOCKET_BUMP_1_Y = 1.8

SOCKET_BUMP_2_X = 8.95
SOCKET_BUMP_2_Y = 4.3

# Offsets from center
SOCKET_CENTER_X_OFFSET = -5.3
SOCKET_CENTER_Y_OFFSET = -7

# Kailh socket outline, including solder pins
SOCKET_TOTAL_DEPTH = (
    LARGE_RADIUS
    + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN
    + RIGHT_FLAT_DEPTH_SOLDER_PIN
    + RIGHT_FLAT_DEPTH_BEHIND_SOLDER_PIN
)

SOCKET_THIN_PART_DEPTH = SOCKET_TOTAL_DEPTH - SMALL_RADIUS

LEFT_FLAT_DEPTH_SOLDER_PIN = (
    SOCKET_THIN_PART_DEPTH
    - LEFT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN
    - LEFT_FLAT_DEPTH_BEHIND_SOLDER_PIN
)

BACK_FLAT_WIDTH = FRONT_FLAT_WIDTH + LARGE_RADIUS - BACK_RIGHT_FLAT_WIDTH - SMALL_RADIUS

SOCKET_TOTAL_WIDTH = FRONT_FLAT_WIDTH + LARGE_RADIUS

# Final switch pin bump coordinates
SOCKET_BUMP_1_X_FROM_CENTER = SOCKET_BUMP_1_X + SOCKET_CENTER_X_OFFSET
SOCKET_BUMP_1_Y_FROM_CENTER = SOCKET_BUMP_1_Y + SOCKET_CENTER_Y_OFFSET
SOCKET_BUMP_2_X_FROM_CENTER = SOCKET_BUMP_2_X + SOCKET_CENTER_X_OFFSET
SOCKET_BUMP_2_Y_FROM_CENTER = SOCKET_BUMP_2_Y + SOCKET_CENTER_Y_OFFSET

# Final bounding box
SOCKET_LEFT_END_X = SOCKET_CENTER_X_OFFSET  # start X is just the offset, since we start sketching from X = 0
SOCKET_RIGHT_END_X = SOCKET_TOTAL_WIDTH + SOCKET_CENTER_X_OFFSET
SOCKET_FRONT_END_Y = SOCKET_CENTER_Y_OFFSET  # start Y is just the offset, since we start sketching from Y = 0
SOCKET_BACK_RIGHT_END_Y = SOCKET_TOTAL_DEPTH + SOCKET_CENTER_Y_OFFSET

SOCKET_LOCKING_LIP_START_Y = SOCKET_THIN_PART_DEPTH + SOCKET_CENTER_Y_OFFSET
SOCKET_LOCKING_LIP_START_X = SOCKET_LEFT_END_X
SOCKET_LOCKING_LIP_WIDTH = BACK_FLAT_WIDTH


def draw_mx_socket():
    socket_base = [
        Line((0, 0), (FRONT_FLAT_WIDTH, 0)),
        RadiusArc(
            (FRONT_FLAT_WIDTH, 0),
            (FRONT_FLAT_WIDTH + LARGE_RADIUS, LARGE_RADIUS),
            LARGE_RADIUS,
        ),
        Line(
            (FRONT_FLAT_WIDTH + LARGE_RADIUS, LARGE_RADIUS),
            (FRONT_FLAT_WIDTH + LARGE_RADIUS, SOCKET_TOTAL_DEPTH),
        ),
        Line(
            (FRONT_FLAT_WIDTH + LARGE_RADIUS, SOCKET_TOTAL_DEPTH),
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS - BACK_RIGHT_FLAT_WIDTH,
                SOCKET_TOTAL_DEPTH,
            ),
        ),
        RadiusArc(
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS - BACK_RIGHT_FLAT_WIDTH,
                SOCKET_TOTAL_DEPTH,
            ),
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS - BACK_RIGHT_FLAT_WIDTH - SMALL_RADIUS,
                SOCKET_THIN_PART_DEPTH,
            ),
            SMALL_RADIUS,
        ),
        Line(
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS - BACK_RIGHT_FLAT_WIDTH - SMALL_RADIUS,
                SOCKET_THIN_PART_DEPTH,
            ),
            (0, SOCKET_THIN_PART_DEPTH),
        ),
        Line((0, SOCKET_THIN_PART_DEPTH), (0, 0)),
    ]
    socket_base = make_face(socket_base)
    socket_base = extrude(socket_base, SOCKET_HEIGHT)

    socket_left_pin = [
        Line(
            (0, SOCKET_THIN_PART_DEPTH - LEFT_FLAT_DEPTH_BEHIND_SOLDER_PIN),
            (
                -SOLDER_PIN_WIDTH,
                SOCKET_THIN_PART_DEPTH - LEFT_FLAT_DEPTH_BEHIND_SOLDER_PIN,
            ),
        ),
        Line(
            (
                -SOLDER_PIN_WIDTH,
                SOCKET_THIN_PART_DEPTH - LEFT_FLAT_DEPTH_BEHIND_SOLDER_PIN,
            ),
            (-SOLDER_PIN_WIDTH, LEFT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN),
        ),
        Line(
            (-SOLDER_PIN_WIDTH, LEFT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN),
            (0, LEFT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN),
        ),
        Line(
            (0, LEFT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN),
            (0, SOCKET_THIN_PART_DEPTH - LEFT_FLAT_DEPTH_BEHIND_SOLDER_PIN),
        ),
    ]
    socket_left_pin = make_face(socket_left_pin)
    socket_left_pin = extrude(socket_left_pin, SOCKET_HEIGHT + PIN_TOP_CLEARANCE_HEIGHT)

    socket_right_pin = [
        Line(
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS,
                LARGE_RADIUS + RIGHT_FLAT_DEPTH_BEHIND_SOLDER_PIN,
            ),
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS + SOLDER_PIN_WIDTH,
                LARGE_RADIUS + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN,
            ),
        ),
        Line(
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS + SOLDER_PIN_WIDTH,
                LARGE_RADIUS + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN,
            ),
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS + SOLDER_PIN_WIDTH,
                LARGE_RADIUS
                + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN
                + RIGHT_FLAT_DEPTH_SOLDER_PIN,
            ),
        ),
        Line(
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS + SOLDER_PIN_WIDTH,
                LARGE_RADIUS
                + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN
                + RIGHT_FLAT_DEPTH_SOLDER_PIN,
            ),
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS,
                LARGE_RADIUS
                + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN
                + RIGHT_FLAT_DEPTH_SOLDER_PIN,
            ),
        ),
        Line(
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS,
                LARGE_RADIUS
                + RIGHT_FLAT_DEPTH_IN_FRONT_OF_SOLDER_PIN
                + RIGHT_FLAT_DEPTH_SOLDER_PIN,
            ),
            (
                FRONT_FLAT_WIDTH + LARGE_RADIUS,
                LARGE_RADIUS + RIGHT_FLAT_DEPTH_BEHIND_SOLDER_PIN,
            ),
        ),
    ]
    socket_right_pin = make_face(socket_right_pin)
    socket_right_pin = extrude(
        socket_right_pin, SOCKET_HEIGHT + PIN_TOP_CLEARANCE_HEIGHT
    )

    socket_bump_1 = Circle(SOCKET_BUMP_RADIUS)
    socket_bump_1 = extrude(socket_bump_1, SOCKET_BUMP_HEIGHT)
    socket_bump_1 = Pos(SOCKET_BUMP_1_X, SOCKET_BUMP_1_Y, SOCKET_HEIGHT) * socket_bump_1

    socket_bump_2 = Circle(SOCKET_BUMP_RADIUS)
    socket_bump_2 = extrude(socket_bump_2, SOCKET_BUMP_HEIGHT)
    socket_bump_2 = Pos(SOCKET_BUMP_2_X, SOCKET_BUMP_2_Y, SOCKET_HEIGHT) * socket_bump_2

    socket = Part() + [
        socket_base,
        socket_left_pin,
        socket_right_pin,
        socket_bump_1,
        socket_bump_2,
    ]
    socket = Pos(SOCKET_CENTER_X_OFFSET, SOCKET_CENTER_Y_OFFSET) * socket
    return Part() + socket
