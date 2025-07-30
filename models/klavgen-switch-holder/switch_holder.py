import math
from build123d import *  # pyright: ignore
from build123d import cast
from mx_socket import (
    PIN_TOP_CLEARANCE_HEIGHT,
    SOCKET_BUMP_1_X_FROM_CENTER,
    SOCKET_BUMP_1_Y_FROM_CENTER,
    SOCKET_BUMP_2_X_FROM_CENTER,
    SOCKET_BUMP_2_Y_FROM_CENTER,
    SOCKET_BUMP_HEIGHT,
    SOCKET_HEIGHT,
    SOCKET_LEFT_END_X,
    SOCKET_LOCKING_LIP_START_X,
    SOCKET_LOCKING_LIP_START_Y,
    SOCKET_LOCKING_LIP_WIDTH,
    SOCKET_RIGHT_END_X,
    SOLDER_PIN_WIDTH,
    draw_mx_socket,
)

# Inspired and adapted from https://github.com/klavgen/klavgen

EXTRA_HOLDER_FRONT_WALL_DEPTH = 0  # 0.6

# Key config
SWITCH_WIDTH = 14
SWITCH_DEPTH = 14
SWITCH_HOLE_TOLERANCE = 0.05
SWITCH_HOLE_WIDTH = SWITCH_WIDTH - SWITCH_HOLE_TOLERANCE
SWITCH_HOLE_DEPTH = SWITCH_DEPTH - SWITCH_HOLE_TOLERANCE

# Case config
CASE_THICKNESS = 2  # 2.4

# Switch hole
SWITCH_BOTTOM_HEIGHT = 5
SWITCH_BOTTOM_BUFFER_HEIGHT = 0.2

# Plate holes for holder lips
HOLDER_PLATE_GAP = 0.1

PLATE_SIDE_HOLE_WIDTH = 1.8
PLATE_SIDE_HOLE_DEPTH = 7

PLATE_FRONT_HOLE_WIDTH = 6
PLATE_FRONT_HOLE_DEPTH = 1.1

# Side wall thicknesses (front is calculated)
HOLDER_SIDE_BOTTOM_WALL_WIDTH = 2.3

# Y cutoffs
CUTOFF_BASE_Y_BEHIND_SOCKET_LIP = 0.2
CUTOFF_Y = 8.2

# Socket supports
SOCKET_BASE_HEIGHT = 1

# Front cutout to ease removal
HAS_FRONT_CUTOUT_FOR_REMOVAL = True
FRONT_REMOVAL_CUTOUT_WIDTH = 3

# Holes for switch metal pins to extend in base
SWITCH_METAL_PIN_BASE_HOLE_RADIUS = 1

# Front wire supports
FRONT_WIRE_SUPPORTS_DEPTH = 1.2

# Side angled cutouts
BOTTOM_ANGLED_CUTOUT_LEFT_END_TOP_Y = 0.5
BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y = 0.5
BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y = 2.8
BOTTOM_ANGLED_CUTOUT_RIGHT_END_TOP_Y = 2.8

# Lip to prevent socket from sliding out
SOCKET_LIP_DEPTH = 0.4
SOCKET_LIP_HEIGHT = 0.2

# Reverse position of diode and col wire:
# * False = diode on left, col wire on right when looking from the front wall
# * True = diode on right, col wire on left
REVERSE_DIODE_AND_COL_WIRE = False

#
# Front wire holes
#

# Diode wire front hole
DIODE_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET = 0.6
DIODE_WIRE_FRONT_HOLE_WIDTH = 0.9

# Col wire front wrapping post (=hole in the front wall)
COL_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET = 0.075
COL_WIRE_FRONT_HOLE_NARROW_WIDTH = 1
COL_WIRE_FRONT_HOLE_NARROW_HEIGHT = 1
COL_WIRE_FRONT_HOLE_WIDE_WIDTH = 1.5

#
# Top lips
#

# Top lips
HOLDER_LIPS_START_BELOW_CASE_TOP = 0.2
HOLDER_LIPS_CHAMFER_TOP = 0.7

# Top side lips
HOLDER_SIDE_LIPS_WIDTH = 0.9
HOLDER_SIDE_LIPS_BASE_WIDTH = 1
HOLDER_SIDE_LIPS_TOP_WIDTH = 0.6

# Top front lip
HOLDER_FRONT_LIP_SIDE_PLATE_GAP = 0.2
HOLDER_FRONT_LIP_HEIGHT = 1.8  # + 1.6
HOLDER_FRONT_LIP_HOLE_HEIGHT = 2
HOLDER_FRONT_LIP_HOLE_WIDTH = 4.2
HOLDER_FRONT_LIP_HOLE_DISTANCE_FROM_TOP = 1.3  # + 1.6

#
# Base holes for switch plastic pins
#

SWITCH_CENTER_PIN_Y = 0
SWITCH_CENTER_PIN_RADIUS = 2.2

SWITCH_SIDE_PIN_DISTANCE = 5
SWITCH_SIDE_PIN_Y = 0
SWITCH_SIDE_PIN_RADIUS = 1.1

#
# Back wrapping posts and col/row separator
#

# Row wire back wrapping posts
HAS_ROW_WIRE_WRAPPERS = True
HAS_LEFT_ROW_WIRE_WRAPPER = True

BACK_WRAPPERS_AND_SEPARATOR_DEPTH = 1.6

ROW_WIRE_WRAPPERS_OFFSET_FROM_PLATE = 1.4
ROW_WIRE_WRAPPERS_BASE_HEIGHT = 1
ROW_WIRE_WRAPPERS_TIP_HEIGHT = 2
ROW_WIRE_WRAPPER_EXTRA_WIDTH = 0

# Col and row wires separator
COL_ROW_SEPARATOR_Z = 2
COL_ROW_SEPARATOR_HEIGHT = 1

# Col wire back wrapping post
COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT = 1
COL_WIRE_WRAPPER_BACK_HEAD_EXTRA_DEPTH = 0.6

COL_WIRE_WRAPPER_BACK_NECK_HEIGHT = 1
COL_WIRE_WRAPPER_NECK_WIDTH = 1
COL_WIRE_WRAPPER_NECK_INNER_MARGIN = 0.85
COL_WIRE_WRAPPER_NECK_OUTER_MARGIN = 0.85

COL_WIRE_WRAPPER_BACK_NECK_BACK_CUTOUT_DEPTH = 0.4

#
# Diode holder
#

# Diode hole location
DIODE_CENTER_X_FROM_SIDE_END = 2.6
DIODE_CENTER_Y_IN_FRONT_OF_BACK_WALL = 3.1
DIODE_ROTATION = -45

# Diode size
DIODE_DEPTH = 4
DIODE_DIAMETER = 2.1

# Diode hole lips
DIODE_BOTTOM_LIPS_Z_OFFSET = 0.8
DIODE_BOTTOM_LIPS_WIDTH = 0.32
DIODE_BOTTOM_LIPS_HEIGHT = 1
DIODE_TOP_LIPS_SIZE = 0.65

# Diode wire cutout
DIODE_WIRE_DIAMETER = 0.55

# Diode wire front triangular cutout
HAS_DIODE_WIRE_TRIANGULAR_CUTOUT = True
DIODE_WIRE_TRIANGULAR_CUTOUT_WIDTH_DEPTH = 1.5

# Diode back wall
HAS_DIODE_BACK_WALL_CUTOUT = True
DIODE_BACK_WALL_TOP_CUT_HALF_WIDTH = True
DIODE_BACK_WALL_DEPTH = 1
DIODE_BACK_WALL_CUTOUT_WIDTH = 6

#
# Back side cuts
#

BACK_SIDE_CUT_START_BEHIND_LIPS = 1
BACK_SIDE_CUT_LEFT_WIDTH = 1
BACK_SIDE_CUT_RIGHT_WIDTH = 1

HOLDER_FRONT_WALL_DEPTH = (
    PLATE_FRONT_HOLE_DEPTH - HOLDER_PLATE_GAP + EXTRA_HOLDER_FRONT_WALL_DEPTH
)

HOLDER_WIDTH = SWITCH_HOLE_WIDTH + 2 * HOLDER_SIDE_BOTTOM_WALL_WIDTH
HOLDER_DEPTH = SWITCH_HOLE_DEPTH + 2 * HOLDER_FRONT_WALL_DEPTH

HOLDER_BOTTOM_HEIGHT = SOCKET_BASE_HEIGHT + SOCKET_HEIGHT + SOCKET_BUMP_HEIGHT
HOLDER_HEIGHT = (
    HOLDER_BOTTOM_HEIGHT
    + SWITCH_BOTTOM_BUFFER_HEIGHT
    + SWITCH_BOTTOM_HEIGHT
    - CASE_THICKNESS
)

HOLDER_HEIGHT_TO_SOCKET_PIN_TOP = (
    SOCKET_BASE_HEIGHT + SOCKET_HEIGHT + PIN_TOP_CLEARANCE_HEIGHT
)

CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR = (
    CUTOFF_Y - BACK_WRAPPERS_AND_SEPARATOR_DEPTH
)

SWITCH_HOLE_MIN_HEIGHT = HOLDER_HEIGHT + CASE_THICKNESS

PLATE_FRONT_HOLE_START_Y = -SWITCH_HOLE_DEPTH / 2 - PLATE_FRONT_HOLE_DEPTH

CUTOFF_BASE_Y = (
    SOCKET_LOCKING_LIP_START_Y + SOCKET_LIP_DEPTH + CUTOFF_BASE_Y_BEHIND_SOCKET_LIP
)

# Holder top walls
HOLDER_SIDE_TOP_WALL_WIDTH = PLATE_SIDE_HOLE_WIDTH - HOLDER_PLATE_GAP
HOLDER_SIDE_TOP_WALL_X_OFFSET = (
    HOLDER_SIDE_BOTTOM_WALL_WIDTH - HOLDER_SIDE_TOP_WALL_WIDTH
)

HOLDER_LIPS_DEPTH = PLATE_SIDE_HOLE_DEPTH - HOLDER_PLATE_GAP

HOLDER_SIDE_LIPS_TOP_LIP_HEIGHT = (
    HOLDER_SIDE_LIPS_WIDTH + HOLDER_SIDE_LIPS_BASE_WIDTH - HOLDER_SIDE_LIPS_TOP_WIDTH
)

HOLDER_FRONT_LOCK_BUMP_WIDTH = (
    PLATE_FRONT_HOLE_WIDTH - 2 * HOLDER_FRONT_LIP_SIDE_PLATE_GAP
)

HOLDER_TOTAL_HEIGHT = (
    HOLDER_HEIGHT
    + CASE_THICKNESS
    - HOLDER_LIPS_START_BELOW_CASE_TOP
    + HOLDER_SIDE_LIPS_WIDTH
    + HOLDER_SIDE_LIPS_TOP_LIP_HEIGHT
)

COL_WIRE_WRAPPER_HEAD_WIDTH = (
    COL_WIRE_WRAPPER_NECK_INNER_MARGIN
    + COL_WIRE_WRAPPER_NECK_WIDTH
    + COL_WIRE_WRAPPER_NECK_OUTER_MARGIN
)

DIODE_CENTER_Y = (
    CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR - DIODE_CENTER_Y_IN_FRONT_OF_BACK_WALL
)


def render_switch_holder():
    # Create holder block, trimming it at the back
    holder = Box(
        HOLDER_WIDTH,
        HOLDER_DEPTH / 2 + CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR,
        HOLDER_HEIGHT,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    holder = cast(Part, Pos(Y=-HOLDER_DEPTH / 2) * holder)

    # Cut hole on front for easy socket removal
    if HAS_FRONT_CUTOUT_FOR_REMOVAL:
        removal_cutout = Box(
            FRONT_REMOVAL_CUTOUT_WIDTH,
            HOLDER_FRONT_WALL_DEPTH,
            SOCKET_HEIGHT,
            align=(Align.CENTER, Align.MIN, Align.MIN),
        )
        removal_cutout = (
            Pos(
                (SOCKET_BUMP_2_X_FROM_CENTER + SOCKET_BUMP_1_X_FROM_CENTER) / 2,
                -HOLDER_DEPTH / 2,
                SOCKET_BASE_HEIGHT,
            )
            * removal_cutout
        )
        holder -= removal_cutout

    # Cut out holes in the base for the switch metal pins
    template_socket_metal_pin_hole = Circle(SWITCH_METAL_PIN_BASE_HOLE_RADIUS)
    template_socket_metal_pin_hole = extrude(
        template_socket_metal_pin_hole, SOCKET_BASE_HEIGHT
    )

    socket_metal_pin_extension_hole_1 = (
        Pos(SOCKET_BUMP_1_X_FROM_CENTER, SOCKET_BUMP_1_Y_FROM_CENTER)
        * template_socket_metal_pin_hole
    )
    holder -= socket_metal_pin_extension_hole_1

    socket_metal_pin_extension_hole_2 = (
        Pos(SOCKET_BUMP_2_X_FROM_CENTER, SOCKET_BUMP_2_Y_FROM_CENTER)
        * template_socket_metal_pin_hole
    )
    holder -= socket_metal_pin_extension_hole_2

    socket = draw_mx_socket()
    socket = Pos(Z=SOCKET_BASE_HEIGHT) * socket

    # Sweep socket and cut from holder
    def sweep_socket():
        HOLE_1_SEEP_UNTIL_Y = (
            BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y
        )
        HOLE_1_SWEEP_DISTANCE = HOLE_1_SEEP_UNTIL_Y - SOCKET_BUMP_1_Y_FROM_CENTER

        hole_1_extrusions = split(socket, Plane.YZ * Pos(Z=1), Keep.BOTTOM)
        hole_1_extrusions = split(
            hole_1_extrusions, Plane.XZ * Pos(Z=-SOCKET_BUMP_1_Y_FROM_CENTER)
        )
        hole_1_extrusions += extrude(
            hole_1_extrusions.faces().sort_by(Axis.Y)[-1], HOLE_1_SWEEP_DISTANCE
        )
        socket_swept = socket + hole_1_extrusions

        HOLE_2_SEEP_UNTIL_Y = (
            BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y
        )
        HOLE_2_SWEEP_DISTANCE = HOLE_2_SEEP_UNTIL_Y - SOCKET_BUMP_2_Y_FROM_CENTER

        hole_2_extrusions = split(socket, Plane.YZ * Pos(Z=-1))
        hole_2_extrusions = split(
            hole_2_extrusions, Plane.XZ * Pos(Z=-SOCKET_BUMP_2_Y_FROM_CENTER)
        )
        hole_2_extrusions += extrude(
            hole_2_extrusions.faces().sort_by(Axis.Y)[-1], HOLE_2_SWEEP_DISTANCE
        )

        socket_swept += hole_2_extrusions

        return socket_swept

    socket_sweep = sweep_socket()
    holder -= socket_sweep

    #
    # Bottom angled cutouts
    #
    SOCKET_BUMPS_MIDPOINT_X = (
        SOCKET_BUMP_1_X_FROM_CENTER + SOCKET_BUMP_2_X_FROM_CENTER
    ) / 2
    END_PIN_CUTOUTS_START_Y = -HOLDER_DEPTH / 2 + FRONT_WIRE_SUPPORTS_DEPTH
    SOCKET_CUTOUTS_START_Y = CUTOFF_BASE_Y

    def draw_angled_side_cutout(
        left_x: float,
        right_x: float,
        front_y: float,
        back_angled_top_y: float,
        to_pin_top: bool = True,
    ):
        width = right_x - left_x
        if width <= 0 or front_y >= back_angled_top_y:
            return None
        top_z = (
            HOLDER_HEIGHT_TO_SOCKET_PIN_TOP
            if to_pin_top
            else (SOCKET_BASE_HEIGHT + SOCKET_HEIGHT)
        )
        y_adjustment = 0 if to_pin_top else PIN_TOP_CLEARANCE_HEIGHT

        angled_cutout = [
            Line((back_angled_top_y + y_adjustment, top_z), (front_y, top_z)),
            Line((front_y, top_z), (front_y, 0)),
            Line((front_y, 0), (back_angled_top_y + y_adjustment + top_z, 0)),
            Line(
                (back_angled_top_y + y_adjustment + top_z, 0),
                (back_angled_top_y + y_adjustment, top_z),
            ),
        ]
        angled_cutout = make_face(angled_cutout)
        angled_cutout = extrude(angled_cutout, width)
        angled_cutout = Plane.YZ * Pos(Z=left_x) * angled_cutout
        angled_cutout = cast(Part, angled_cutout)

        return angled_cutout

    # Left, end
    left_side_end_angled_cutout = draw_angled_side_cutout(
        left_x=-HOLDER_WIDTH / 2,
        right_x=SOCKET_LEFT_END_X - SOLDER_PIN_WIDTH,
        front_y=END_PIN_CUTOUTS_START_Y,
        back_angled_top_y=(
            BOTTOM_ANGLED_CUTOUT_RIGHT_END_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_LEFT_END_TOP_Y
        ),
    )
    # Left, pin
    left_side_pin_angled_cutout = draw_angled_side_cutout(
        left_x=SOCKET_LEFT_END_X - SOLDER_PIN_WIDTH,
        right_x=SOCKET_LEFT_END_X,
        front_y=END_PIN_CUTOUTS_START_Y,
        back_angled_top_y=(
            BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y
        ),
    )
    # Left, socket
    left_socket_pin_angled_cutout = draw_angled_side_cutout(
        left_x=SOCKET_LEFT_END_X,
        right_x=SOCKET_BUMPS_MIDPOINT_X,
        front_y=SOCKET_CUTOUTS_START_Y,
        back_angled_top_y=(
            BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y
        ),
        to_pin_top=False,
    )
    # Right, socket
    right_socket_pin_angled_cutout = draw_angled_side_cutout(
        left_x=SOCKET_BUMPS_MIDPOINT_X,
        right_x=SOCKET_RIGHT_END_X,
        front_y=SOCKET_CUTOUTS_START_Y,
        back_angled_top_y=(
            BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y
        ),
        to_pin_top=False,
    )
    # Right, pin
    right_side_pin_angled_cutout = draw_angled_side_cutout(
        left_x=SOCKET_RIGHT_END_X,
        right_x=SOCKET_RIGHT_END_X + SOLDER_PIN_WIDTH,
        front_y=END_PIN_CUTOUTS_START_Y,
        back_angled_top_y=(
            BOTTOM_ANGLED_CUTOUT_LEFT_SOCKET_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_RIGHT_SOCKET_TOP_Y
        ),
    )
    # Right, end
    right_side_end_angled_cutout = draw_angled_side_cutout(
        left_x=SOCKET_RIGHT_END_X + SOLDER_PIN_WIDTH,
        right_x=HOLDER_WIDTH / 2,
        front_y=END_PIN_CUTOUTS_START_Y,
        back_angled_top_y=(
            BOTTOM_ANGLED_CUTOUT_LEFT_END_TOP_Y
            if REVERSE_DIODE_AND_COL_WIRE
            else BOTTOM_ANGLED_CUTOUT_RIGHT_END_TOP_Y
        ),
    )

    holder -= left_side_end_angled_cutout
    holder -= left_side_pin_angled_cutout
    holder -= left_socket_pin_angled_cutout
    holder -= right_socket_pin_angled_cutout
    holder -= right_side_pin_angled_cutout
    holder -= right_side_end_angled_cutout

    # Socket locking lip
    socket_locking_lip = Box(
        SOCKET_LIP_DEPTH, SOCKET_LIP_HEIGHT, SOCKET_LOCKING_LIP_WIDTH, align=Align.MIN
    )
    socket_locking_lip = (
        Plane.YZ
        * Pos(
            SOCKET_LOCKING_LIP_START_Y, SOCKET_BASE_HEIGHT, SOCKET_LOCKING_LIP_START_X
        )
        * socket_locking_lip
    )
    socket_locking_lip = cast(Part, socket_locking_lip)
    holder += socket_locking_lip

    # Diode wire front hole
    DIODE_WIRE_FRONT_HOLE_START_X = (
        (SOCKET_RIGHT_END_X + DIODE_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET)
        if REVERSE_DIODE_AND_COL_WIRE
        else (
            SOCKET_LEFT_END_X
            - DIODE_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET
            - DIODE_WIRE_FRONT_HOLE_WIDTH
        )
    )
    diode_wire_front_hole = Box(
        DIODE_WIRE_FRONT_HOLE_WIDTH,
        FRONT_WIRE_SUPPORTS_DEPTH,
        SOCKET_BASE_HEIGHT + SOCKET_HEIGHT,
        align=Align.MIN,
    )
    diode_wire_front_hole = (
        Pos(DIODE_WIRE_FRONT_HOLE_START_X, -HOLDER_DEPTH / 2) * diode_wire_front_hole
    )
    holder -= diode_wire_front_hole

    # Col wire front wrapping post
    DIODE_WIRE_FRONT_HOLE_NARROW_START_X = (
        (
            SOCKET_LEFT_END_X
            - COL_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET
            - COL_WIRE_FRONT_HOLE_NARROW_WIDTH
        )
        if REVERSE_DIODE_AND_COL_WIRE
        else (SOCKET_RIGHT_END_X + COL_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET)
    )
    DIODE_WIRE_FRONT_HOLE_WIDE_START_X = (
        (
            SOCKET_LEFT_END_X
            - COL_WIRE_FRONT_HOLE_DISTANCE_FROM_SOCKET
            - COL_WIRE_FRONT_HOLE_WIDE_WIDTH
        )
        if REVERSE_DIODE_AND_COL_WIRE
        else (DIODE_WIRE_FRONT_HOLE_NARROW_START_X)
    )
    col_wire_front_wrapper_cutout_narrow = Box(
        COL_WIRE_FRONT_HOLE_NARROW_WIDTH,
        FRONT_WIRE_SUPPORTS_DEPTH,
        SOCKET_BASE_HEIGHT + SOCKET_HEIGHT,
        align=Align.MIN,
    )
    col_wire_front_wrapper_cutout_narrow = (
        Pos(DIODE_WIRE_FRONT_HOLE_NARROW_START_X, -HOLDER_DEPTH / 2)
        * col_wire_front_wrapper_cutout_narrow
    )
    holder -= col_wire_front_wrapper_cutout_narrow
    col_wire_front_wrapper_cutout_wide = Box(
        COL_WIRE_FRONT_HOLE_WIDE_WIDTH,
        FRONT_WIRE_SUPPORTS_DEPTH,
        SOCKET_BASE_HEIGHT + SOCKET_HEIGHT - COL_WIRE_FRONT_HOLE_NARROW_HEIGHT,
        align=Align.MIN,
    )
    col_wire_front_wrapper_cutout_wide = (
        Pos(
            DIODE_WIRE_FRONT_HOLE_WIDE_START_X,
            -HOLDER_DEPTH / 2,
            COL_WIRE_FRONT_HOLE_NARROW_HEIGHT,
        )
        * col_wire_front_wrapper_cutout_wide
    )
    holder -= col_wire_front_wrapper_cutout_wide

    # Top lips
    def draw_top_lips():
        # Top side lips
        HOLDER_LIPS_BASE_HEIGHT = CASE_THICKNESS - HOLDER_LIPS_START_BELOW_CASE_TOP
        HOLDER_SIDE_LIPS_TOTAL_HEIGHT = (
            HOLDER_LIPS_BASE_HEIGHT
            + HOLDER_SIDE_LIPS_WIDTH
            + HOLDER_SIDE_LIPS_TOP_LIP_HEIGHT
        )
        # Left lip
        lips = Polyline(
            [
                (0, 0),
                (0, HOLDER_LIPS_BASE_HEIGHT),
                (
                    -HOLDER_SIDE_LIPS_WIDTH,
                    HOLDER_LIPS_BASE_HEIGHT + HOLDER_SIDE_LIPS_WIDTH,
                ),
                (
                    -HOLDER_SIDE_LIPS_WIDTH + HOLDER_SIDE_LIPS_TOP_LIP_HEIGHT,
                    HOLDER_SIDE_LIPS_TOTAL_HEIGHT,
                ),
                (HOLDER_SIDE_LIPS_BASE_WIDTH, HOLDER_SIDE_LIPS_TOTAL_HEIGHT),
                (HOLDER_SIDE_LIPS_BASE_WIDTH, 0),
                (0, 0),
            ]
        ).edges()
        lips = make_face(lips)
        lips = extrude(lips, -HOLDER_LIPS_DEPTH)
        lips = (
            Plane.XZ
            * Pos(
                -HOLDER_WIDTH / 2 + HOLDER_SIDE_TOP_WALL_X_OFFSET,
                HOLDER_HEIGHT,
                SWITCH_HOLE_DEPTH / 2 + EXTRA_HOLDER_FRONT_WALL_DEPTH - 0.1,
            )
            * lips
        )
        lips = cast(Part, lips)
        # Cut lip so it slopes on the front
        top_left_lip_side_cut = Polyline(
            [
                (0, 0),
                (5, 5),
                (0, 5),
                (0, 0),
            ]
        ).edges()
        top_left_lip_side_cut = make_face(top_left_lip_side_cut)
        top_left_lip_side_cut = extrude(top_left_lip_side_cut, HOLDER_WIDTH)
        top_left_lip_side_cut = (
            Plane.YZ
            * Pos(
                -SWITCH_HOLE_DEPTH / 2 - EXTRA_HOLDER_FRONT_WALL_DEPTH + 0.1,
                HOLDER_HEIGHT,
                -HOLDER_WIDTH / 2 - 2,
            )
            * top_left_lip_side_cut
        )
        top_left_lip_side_cut = cast(Part, top_left_lip_side_cut)
        lips -= top_left_lip_side_cut
        # Chamfer lip at the back for easier insertion
        lips = chamfer(
            lips.edges().group_by(Axis.Y)[-1].group_by(Axis.Z)[-1].filter_by(Axis.X),
            HOLDER_LIPS_CHAMFER_TOP,
        )
        # Right lip is a mirror image of the left
        top_right_lip = mirror(lips, Plane.YZ)
        lips += top_right_lip
        # Draw front lip
        front_lip = Box(
            HOLDER_FRONT_LOCK_BUMP_WIDTH,
            HOLDER_FRONT_WALL_DEPTH,
            HOLDER_FRONT_LIP_HEIGHT,
            align=(Align.CENTER, Align.MIN, Align.MIN),
        )
        front_lip = Pos(0, -HOLDER_DEPTH / 2, HOLDER_HEIGHT) * front_lip
        # Chamfer front lip
        front_lip = chamfer(
            front_lip.edges()
            .group_by(Axis.Y)[0]
            .group_by(Axis.Z)[-1]
            .filter_by(Axis.X),
            HOLDER_LIPS_CHAMFER_TOP,
        )
        lips += front_lip
        return lips

    top_lips = draw_top_lips()
    holder += top_lips
    # Add a hole so the switch grabs to the holder
    front_hole = Box(
        HOLDER_FRONT_LIP_HOLE_WIDTH,
        HOLDER_FRONT_WALL_DEPTH,
        HOLDER_FRONT_LIP_HOLE_HEIGHT,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    front_hole = (
        Pos(
            0,
            -HOLDER_DEPTH / 2,
            HOLDER_HEIGHT
            + HOLDER_FRONT_LIP_HEIGHT
            - HOLDER_FRONT_LIP_HOLE_HEIGHT
            - HOLDER_FRONT_LIP_HOLE_DISTANCE_FROM_TOP,
        )
        * front_hole
    )
    holder -= cast(Part, front_hole)

    # Switch bottom hole
    switch_bottom_hole = Box(
        SWITCH_HOLE_WIDTH,
        HOLDER_DEPTH * 2,
        HOLDER_HEIGHT,
        align=(Align.CENTER, Align.MIN, Align.MIN),
    )
    switch_bottom_hole = (
        Pos(0, -SWITCH_HOLE_DEPTH / 2, HOLDER_BOTTOM_HEIGHT) * switch_bottom_hole
    )
    holder -= switch_bottom_hole

    # Holes for switch plastic pins
    switch_plastic_pin_hole_left = Circle(SWITCH_SIDE_PIN_RADIUS)
    switch_plastic_pin_hole_left = extrude(switch_plastic_pin_hole_left, 20)
    switch_plastic_pin_hole_left = (
        Pos(-SWITCH_SIDE_PIN_DISTANCE, SWITCH_SIDE_PIN_Y) * switch_plastic_pin_hole_left
    )
    holder -= switch_plastic_pin_hole_left
    switch_plastic_pin_hole_center = Circle(SWITCH_CENTER_PIN_RADIUS)
    switch_plastic_pin_hole_center = extrude(switch_plastic_pin_hole_center, 20)
    switch_plastic_pin_hole_center = (
        Pos(0, SWITCH_CENTER_PIN_Y) * switch_plastic_pin_hole_center
    )
    holder -= switch_plastic_pin_hole_center
    switch_plastic_pin_hole_right = Circle(SWITCH_SIDE_PIN_RADIUS)
    switch_plastic_pin_hole_right = extrude(switch_plastic_pin_hole_right, 20)
    switch_plastic_pin_hole_right = (
        Pos(SWITCH_SIDE_PIN_DISTANCE, SWITCH_SIDE_PIN_Y) * switch_plastic_pin_hole_right
    )
    holder -= switch_plastic_pin_hole_right

    #
    # Back wrapping posts and col/row separator
    #

    # Row wire wrapping posts
    if HAS_ROW_WIRE_WRAPPERS:
        row_wire_left_wrapper = Polyline(
            [
                (0, 0),
                (BACK_WRAPPERS_AND_SEPARATOR_DEPTH, 0),
                (BACK_WRAPPERS_AND_SEPARATOR_DEPTH, -ROW_WIRE_WRAPPERS_TIP_HEIGHT),
                (0, -ROW_WIRE_WRAPPERS_BASE_HEIGHT),
                (0, 0),
            ]
        ).edges()
        row_wire_left_wrapper = make_face(row_wire_left_wrapper)
        row_wire_left_wrapper = extrude(
            row_wire_left_wrapper,
            HOLDER_SIDE_BOTTOM_WALL_WIDTH + ROW_WIRE_WRAPPER_EXTRA_WIDTH,
        )
        row_wire_left_wrapper = (
            Plane.YZ
            * Pos(
                CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR,
                HOLDER_HEIGHT - ROW_WIRE_WRAPPERS_OFFSET_FROM_PLATE,
                -HOLDER_WIDTH / 2,
            )
            * row_wire_left_wrapper
        )
        row_wire_left_wrapper = cast(Part, row_wire_left_wrapper)
        if HAS_LEFT_ROW_WIRE_WRAPPER:
            holder += row_wire_left_wrapper
        row_wire_right_wrapper = mirror(row_wire_left_wrapper, Plane.YZ)
        holder += row_wire_right_wrapper

    # Separator between column and row wires
    SEPARATOR_START_X = (
        (-HOLDER_WIDTH / 2 + BACK_SIDE_CUT_LEFT_WIDTH)
        if REVERSE_DIODE_AND_COL_WIRE
        else (
            HOLDER_WIDTH / 2 - BACK_SIDE_CUT_RIGHT_WIDTH - COL_WIRE_WRAPPER_HEAD_WIDTH
        )
    )
    col_row_separator = Box(
        COL_WIRE_WRAPPER_HEAD_WIDTH,
        BACK_WRAPPERS_AND_SEPARATOR_DEPTH,
        COL_ROW_SEPARATOR_HEIGHT,
        align=Align.MIN,
    )
    col_row_separator = (
        Pos(
            SEPARATOR_START_X,
            CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR,
            COL_ROW_SEPARATOR_Z,
        )
        * col_row_separator
    )
    holder += col_row_separator

    # Col wire back wrapping post
    def render_col_wire_back_wrapper():
        START_X = (
            (-HOLDER_WIDTH / 2 + BACK_SIDE_CUT_LEFT_WIDTH)
            if REVERSE_DIODE_AND_COL_WIRE
            else (
                HOLDER_WIDTH / 2
                - BACK_SIDE_CUT_RIGHT_WIDTH
                - COL_WIRE_WRAPPER_HEAD_WIDTH
            )
        )
        NECK_LEFT_MARGIN = (
            (COL_WIRE_WRAPPER_NECK_OUTER_MARGIN)
            if REVERSE_DIODE_AND_COL_WIRE
            else (COL_WIRE_WRAPPER_NECK_INNER_MARGIN)
        )
        NECK_RIGHT_MARGIN = (
            (COL_WIRE_WRAPPER_NECK_INNER_MARGIN)
            if REVERSE_DIODE_AND_COL_WIRE
            else (COL_WIRE_WRAPPER_NECK_OUTER_MARGIN)
        )

        # Neck left cutout (so neck is narrower than head)
        neck_left_cutout = Box(
            NECK_LEFT_MARGIN,
            HOLDER_DEPTH / 2,
            COL_WIRE_WRAPPER_BACK_NECK_HEIGHT,
            align=Align.MIN,
        )
        neck_left_cutout = (
            Pos(START_X, 0, COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT) * neck_left_cutout
        )

        # Neck right cutout (so neck is narrower than head)
        neck_right_cutout = Box(
            NECK_RIGHT_MARGIN,
            HOLDER_DEPTH / 2,
            COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT,
            align=Align.MIN,
        )
        neck_right_cutout = (
            Pos(
                START_X + NECK_LEFT_MARGIN + COL_WIRE_WRAPPER_NECK_WIDTH,
                0,
                COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT,
            )
            * neck_right_cutout
        )

        # Neck cutout at the back (so the neck is much less deep than head and the wire has more space for wrapping)
        neck_back_cutout = Box(
            COL_WIRE_WRAPPER_NECK_WIDTH,
            COL_WIRE_WRAPPER_BACK_NECK_BACK_CUTOUT_DEPTH,
            COL_WIRE_WRAPPER_BACK_NECK_HEIGHT,
            align=Align.MIN,
        )
        neck_back_cutout = (
            Pos(
                START_X + NECK_LEFT_MARGIN,
                CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR
                - COL_WIRE_WRAPPER_BACK_NECK_BACK_CUTOUT_DEPTH,
                COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT,
            )
            * neck_back_cutout
        )

        ANGLED_CUTS_START_Y = (
            BOTTOM_ANGLED_CUTOUT_RIGHT_END_TOP_Y
            + HOLDER_HEIGHT_TO_SOCKET_PIN_TOP
            - COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT
        )

        # Head front 45 degrees cutout on the left (for 3D printing without supports)
        head_angled_cutout_left = Polyline(
            [
                (0, 0),
                (NECK_LEFT_MARGIN, 0),
                (0, NECK_LEFT_MARGIN),
                (0, 0),
            ]
        ).edges()
        head_angled_cutout_left = make_face(head_angled_cutout_left)
        head_angled_cutout_left = extrude(
            head_angled_cutout_left, COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT
        )
        head_angled_cutout_left = (
            Pos(START_X, ANGLED_CUTS_START_Y) * head_angled_cutout_left
        )

        # Head front 45 degrees cutout on the right (for 3D printing without supports)
        head_angled_cutout_right = Polyline(
            [
                (0, 0),
                (NECK_RIGHT_MARGIN, 0),
                (NECK_RIGHT_MARGIN, NECK_RIGHT_MARGIN),
                (0, 0),
            ]
        ).edges()
        head_angled_cutout_right = make_face(head_angled_cutout_right)
        head_angled_cutout_right = extrude(
            head_angled_cutout_right, COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT
        )
        head_angled_cutout_right = (
            Pos(
                START_X + NECK_LEFT_MARGIN + COL_WIRE_WRAPPER_NECK_WIDTH,
                ANGLED_CUTS_START_Y,
            )
            * head_angled_cutout_right
        )

        # Head extra depth (to make wrapping easier)
        head_extra_depth = Box(
            COL_WIRE_WRAPPER_HEAD_WIDTH,
            COL_WIRE_WRAPPER_BACK_HEAD_EXTRA_DEPTH,
            COL_WIRE_WRAPPER_BACK_HEAD_HEIGHT,
            align=Align.MIN,
        )
        head_extra_depth = (
            Pos(START_X, CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR) * head_extra_depth
        )

        cutouts = Part() + [
            neck_left_cutout,
            neck_right_cutout,
            neck_back_cutout,
            head_angled_cutout_left,
            head_angled_cutout_right,
        ]

        return head_extra_depth, cutouts

    col_wire_back_wrapper_additions, col_wire_back_wrapper_cutouts = (
        render_col_wire_back_wrapper()
    )
    holder += col_wire_back_wrapper_additions
    holder -= col_wire_back_wrapper_cutouts

    #
    # Diode holder
    #
    def render_diode_holder_cutout():
        BACK_SIDE_CUT_WIDTH = (
            BACK_SIDE_CUT_RIGHT_WIDTH
            if REVERSE_DIODE_AND_COL_WIRE
            else BACK_SIDE_CUT_LEFT_WIDTH
        )
        DIODE_CENTER_X = (
            -HOLDER_WIDTH / 2 + BACK_SIDE_CUT_WIDTH + DIODE_CENTER_X_FROM_SIDE_END
        )

        #
        # Diode holder and wire cutout
        #

        # Diode holder hole
        diode_holder_cutout = Polyline(
            [
                (0, 0),
                (0, DIODE_BOTTOM_LIPS_Z_OFFSET),
                (
                    DIODE_BOTTOM_LIPS_WIDTH,
                    DIODE_BOTTOM_LIPS_Z_OFFSET + DIODE_BOTTOM_LIPS_WIDTH,
                ),
                (
                    DIODE_BOTTOM_LIPS_WIDTH,
                    DIODE_BOTTOM_LIPS_Z_OFFSET
                    + DIODE_BOTTOM_LIPS_WIDTH
                    + DIODE_BOTTOM_LIPS_HEIGHT,
                ),
                (
                    0,
                    DIODE_BOTTOM_LIPS_Z_OFFSET
                    + DIODE_BOTTOM_LIPS_WIDTH
                    + DIODE_BOTTOM_LIPS_HEIGHT
                    + DIODE_BOTTOM_LIPS_WIDTH,
                ),
                (0, HOLDER_BOTTOM_HEIGHT - DIODE_TOP_LIPS_SIZE),
                (DIODE_TOP_LIPS_SIZE, HOLDER_BOTTOM_HEIGHT),
                (DIODE_DIAMETER - DIODE_TOP_LIPS_SIZE, HOLDER_BOTTOM_HEIGHT),
                (DIODE_DIAMETER, HOLDER_BOTTOM_HEIGHT - DIODE_TOP_LIPS_SIZE),
                (
                    DIODE_DIAMETER,
                    DIODE_BOTTOM_LIPS_Z_OFFSET
                    + DIODE_BOTTOM_LIPS_WIDTH
                    + DIODE_BOTTOM_LIPS_HEIGHT
                    + DIODE_BOTTOM_LIPS_WIDTH,
                ),
                (
                    DIODE_DIAMETER - DIODE_BOTTOM_LIPS_WIDTH,
                    DIODE_BOTTOM_LIPS_Z_OFFSET
                    + DIODE_BOTTOM_LIPS_WIDTH
                    + DIODE_BOTTOM_LIPS_HEIGHT,
                ),
                (
                    DIODE_DIAMETER - DIODE_BOTTOM_LIPS_WIDTH,
                    DIODE_BOTTOM_LIPS_Z_OFFSET + DIODE_BOTTOM_LIPS_WIDTH,
                ),
                (DIODE_DIAMETER, DIODE_BOTTOM_LIPS_Z_OFFSET),
                (DIODE_DIAMETER, 0),
                (0, 0),
            ]
        ).edges()
        diode_holder_cutout = make_face(diode_holder_cutout)
        diode_holder_cutout = extrude(diode_holder_cutout, -DIODE_DEPTH)
        diode_holder_cutout = (
            Pos(DIODE_CENTER_X, 0, -DIODE_CENTER_Y)
            * Rot(Y=DIODE_ROTATION)
            * Pos(-DIODE_DIAMETER / 2, 0, DIODE_DEPTH / 2)
            * diode_holder_cutout
        )
        diode_holder_cutout = Plane.XZ * cast(Part, diode_holder_cutout)
        diode_holder_cutout = cast(Part, diode_holder_cutout)

        # Diode wire straight cutout
        diode_wire_cutout = Box(
            DIODE_WIRE_DIAMETER,
            15,
            HOLDER_BOTTOM_HEIGHT - (DIODE_DIAMETER - DIODE_WIRE_DIAMETER) / 2,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        diode_wire_cutout = (
            Pos(DIODE_CENTER_X, DIODE_CENTER_Y)
            * Rot(Z=DIODE_ROTATION)
            * diode_wire_cutout
        )
        diode_wire_cutout = cast(Part, diode_wire_cutout)
        diode_holder_cutout += diode_wire_cutout

        #
        # Diode wire channel front triangular cutout
        #

        # Determine the wire size in the Y direction (it's the hypotenuse since it's at a 45 degree angle)
        DIODE_WIRE_Y_DEPTH = math.sqrt(2 * DIODE_WIRE_DIAMETER**2)

        # Determine the Y where the inside wall of the wire channel intersects the holder left end. Move by 0.01 so the 45
        # degree channel wall will not overlap with the 45 degree line of the triangular cutout.
        # We use cf.diode_center_x_from_side_end and cf.back_side_cut_width since the wire is at 45 degrees, therefore it
        # forms a square between the center of the diode and the crossing of the holder left end.
        DIODE_WIRE_Y_INTERSECT_WITH_HOLDER_LEFT_END = (
            DIODE_CENTER_Y
            - DIODE_CENTER_X_FROM_SIDE_END
            - BACK_SIDE_CUT_WIDTH
            - DIODE_WIRE_Y_DEPTH / 2
            + 0.01
        )

        # Determine the triangle to cut out, starting from the intersection point of the wire channel inner wall and the
        # holder left end
        if HAS_DIODE_WIRE_TRIANGULAR_CUTOUT:
            diode_wire_front_triangular_cutout = Polyline(
                [
                    (0, 0),
                    (DIODE_WIRE_TRIANGULAR_CUTOUT_WIDTH_DEPTH, 0),
                    (
                        DIODE_WIRE_TRIANGULAR_CUTOUT_WIDTH_DEPTH,
                        DIODE_WIRE_TRIANGULAR_CUTOUT_WIDTH_DEPTH,
                    ),
                    (0, 0),
                ]
            ).edges()
            diode_wire_front_triangular_cutout = make_face(
                diode_wire_front_triangular_cutout
            )
            diode_wire_front_triangular_cutout = extrude(
                diode_wire_front_triangular_cutout, -5
            )
            diode_wire_front_triangular_cutout = (
                Pos(
                    -HOLDER_WIDTH / 2,
                    DIODE_WIRE_Y_INTERSECT_WITH_HOLDER_LEFT_END,
                    HOLDER_BOTTOM_HEIGHT - DIODE_DIAMETER / 2 + DIODE_WIRE_DIAMETER / 2,
                )
                * diode_wire_front_triangular_cutout
            )
            diode_wire_front_triangular_cutout = cast(
                Part, diode_wire_front_triangular_cutout
            )
            diode_holder_cutout += diode_wire_front_triangular_cutout
        #
        #
        # Diode back cutouts
        #

        if HAS_DIODE_BACK_WALL_CUTOUT:
            diode_back_wall_cutout = Box(
                DIODE_BACK_WALL_CUTOUT_WIDTH,
                HOLDER_DEPTH,
                HOLDER_HEIGHT,
                align=(Align.CENTER, Align.MIN, Align.MIN),
            )
            diode_back_wall_cutout = (
                Pos(DIODE_CENTER_X, DIODE_CENTER_Y)
                * Rot(Z=DIODE_ROTATION)
                * Pos(Y=DIODE_DEPTH / 2 + DIODE_BACK_WALL_DEPTH)
                * diode_back_wall_cutout
            )
            diode_back_wall_cutout = cast(Part, diode_back_wall_cutout)
            diode_holder_cutout += diode_back_wall_cutout

        # Diode back wall top left cutout, since it's unsupported for 3D-printing
        diode_back_wall_top_left_cutout = Box(
            (
                (DIODE_DIAMETER / 2)
                if DIODE_BACK_WALL_TOP_CUT_HALF_WIDTH
                else DIODE_DIAMETER
            ),
            DIODE_BACK_WALL_DEPTH,
            HOLDER_BOTTOM_HEIGHT - DIODE_DIAMETER / 2 + DIODE_WIRE_DIAMETER / 2,
            align=Align.MIN,
        )
        diode_back_wall_top_left_cutout = (
            Pos(DIODE_CENTER_X, DIODE_CENTER_Y)
            * Rot(Z=DIODE_ROTATION)
            * Pos(-DIODE_DIAMETER / 2, DIODE_DEPTH / 2)
            * diode_back_wall_top_left_cutout
        )
        diode_back_wall_top_left_cutout = cast(Part, diode_back_wall_top_left_cutout)
        diode_holder_cutout += diode_back_wall_top_left_cutout

        if REVERSE_DIODE_AND_COL_WIRE:
            diode_holder_cutout = mirror(diode_holder_cutout, Plane.YZ)

        return diode_holder_cutout

    diode_holder_cutout = render_diode_holder_cutout()
    holder -= diode_holder_cutout

    #
    # Central vertical cut
    #

    # Calculate side (x and y) of the 45 degree point of a unit circle (hypotenuse is 1), 0.5 = (1 ** 2) / 2
    UNIT_CIRCLE_45_DEG_SIDE = math.sqrt(0.5)

    if not REVERSE_DIODE_AND_COL_WIRE:
        # Start of the col wire back wrapper
        COL_WIRE_BACK_WRAPPER_START_X = (
            HOLDER_WIDTH / 2 - BACK_SIDE_CUT_RIGHT_WIDTH - COL_WIRE_WRAPPER_HEAD_WIDTH
        )

        # Determine 45 degree side of left switch hole
        SWITCH_LEFT_HOLE_45_DEG_SIDE = UNIT_CIRCLE_45_DEG_SIDE * SWITCH_SIDE_PIN_RADIUS

        # Determine the left hole left 45 degree point X
        SWITCH_LEFT_HOLE_45_DEG_X = (
            -SWITCH_SIDE_PIN_DISTANCE - SWITCH_LEFT_HOLE_45_DEG_SIDE
        )

        # Determine the side of the triangle we're cutting starting from the left hole
        LEFT_TRIANGLE_CUT_SIDE = (
            CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR - SWITCH_LEFT_HOLE_45_DEG_SIDE
        )

        # Cut, starting from front center of left hole, going counter-clockwise
        vertical_cut = Polyline(
            [
                (-SWITCH_SIDE_PIN_DISTANCE, -SWITCH_SIDE_PIN_RADIUS),
                (SWITCH_LEFT_HOLE_45_DEG_X, SWITCH_LEFT_HOLE_45_DEG_SIDE),
                (
                    SWITCH_LEFT_HOLE_45_DEG_X + LEFT_TRIANGLE_CUT_SIDE,
                    CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR,
                ),
                (
                    COL_WIRE_BACK_WRAPPER_START_X,
                    CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR,
                ),
                (COL_WIRE_BACK_WRAPPER_START_X, 0),
                (SWITCH_SIDE_PIN_DISTANCE, -SWITCH_SIDE_PIN_RADIUS),
                (-SWITCH_SIDE_PIN_DISTANCE, -SWITCH_SIDE_PIN_RADIUS),
            ]
        ).edges()
        vertical_cut = make_face(vertical_cut)
        vertical_cut = extrude(vertical_cut, HOLDER_TOTAL_HEIGHT)
    else:
        # Start of the col wire back wrapper
        LEFT_WALL_END_X = -HOLDER_WIDTH / 2 + HOLDER_SIDE_BOTTOM_WALL_WIDTH
        COL_WIRE_BACK_WRAPPER_END_X = (
            -HOLDER_WIDTH / 2 + BACK_SIDE_CUT_LEFT_WIDTH + COL_WIRE_WRAPPER_HEAD_WIDTH
        )
        LEFT_TRIANGLE_SIDE = COL_WIRE_BACK_WRAPPER_END_X - LEFT_WALL_END_X

        SWITCH_CENTER_HOLE_45_DEG_SIDE = (
            UNIT_CIRCLE_45_DEG_SIDE * SWITCH_CENTER_PIN_RADIUS
        )

        RIGHT_CUTOUT_END_X = 1

        vertical_cut = Polyline(
            [
                (LEFT_WALL_END_X, -SWITCH_SIDE_PIN_RADIUS),
                (LEFT_WALL_END_X, BOTTOM_ANGLED_CUTOUT_RIGHT_END_TOP_Y),
                (
                    LEFT_WALL_END_X + LEFT_TRIANGLE_SIDE,
                    BOTTOM_ANGLED_CUTOUT_RIGHT_END_TOP_Y + LEFT_TRIANGLE_SIDE,
                ),
                (
                    LEFT_WALL_END_X + LEFT_TRIANGLE_SIDE,
                    CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR,
                ),
                (RIGHT_CUTOUT_END_X, CUTOFF_Y_BEFORE_BACK_WRAPPERS_AND_SEPARATOR),
                (
                    RIGHT_CUTOUT_END_X,
                    SWITCH_CENTER_HOLE_45_DEG_SIDE
                    + (SWITCH_CENTER_HOLE_45_DEG_SIDE - RIGHT_CUTOUT_END_X),
                ),
                (SWITCH_CENTER_HOLE_45_DEG_SIDE, SWITCH_CENTER_HOLE_45_DEG_SIDE),
                (RIGHT_CUTOUT_END_X, -SWITCH_SIDE_PIN_RADIUS),
                (LEFT_WALL_END_X, -SWITCH_SIDE_PIN_RADIUS),
            ]
        ).edges()
        vertical_cut = make_face(vertical_cut)
        vertical_cut = extrude(vertical_cut, HOLDER_TOTAL_HEIGHT)

    holder -= vertical_cut

    #
    # Bottom back side cuts
    #

    # Left cut
    bottom_back_cut_left = Box(
        BACK_SIDE_CUT_LEFT_WIDTH, HOLDER_DEPTH, HOLDER_HEIGHT, align=Align.MIN
    )
    bottom_back_cut_left = (
        Pos(
            -HOLDER_WIDTH / 2,
            -SWITCH_HOLE_DEPTH / 2
            + HOLDER_LIPS_DEPTH
            + BACK_SIDE_CUT_START_BEHIND_LIPS,
        )
        * bottom_back_cut_left
    )
    holder -= bottom_back_cut_left

    # Right cut
    bottom_back_cut_right = Box(
        BACK_SIDE_CUT_RIGHT_WIDTH, HOLDER_DEPTH, HOLDER_HEIGHT, align=Align.MIN
    )
    bottom_back_cut_right = (
        Pos(
            HOLDER_WIDTH / 2 - BACK_SIDE_CUT_RIGHT_WIDTH,
            -SWITCH_HOLE_DEPTH / 2
            + HOLDER_LIPS_DEPTH
            + BACK_SIDE_CUT_START_BEHIND_LIPS,
        )
        * bottom_back_cut_right
    )
    holder -= bottom_back_cut_right

    return holder
