import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show

WIDTH = 183
HEIGHT = 104
WALL_DEPTH = 2.3  # Some walls are slightly thinner but we ignore that
SMALL_CORNER_RADIUS = 3
BIG_CORNER_RADIUS = 15
FRONT_CORNER_RADIUS = 2
WALL_HEIGHT = 6.1
TOP_WALL_HEIGHT = 5.2
IN_WIDTH = 26
IN_HEIGHT = 16.25
BOTTOM_SIDE_WALLS_WIDTH = 57
BOTTOM_CURVE_RADIUS = 67

STUB_WALL_HEIGHT = 10.4
STUB_WALL_WIDTH = 16
STUB_WALL_TOP_CORNER_RADIUS = 3
STUB_WALL_BOTTOM_CORNER_RADIUS = 4
STUB_STEP_HEIGHT = 3.2 - WALL_DEPTH
STUB_HEIGHT = 9 - STUB_STEP_HEIGHT - WALL_DEPTH
STUB_BOTTOM_RADIUS = 5.7 / 2
STUB_TOP_RADIUS = 2 / 2
STUB_STEP_RADIUS = 9 / 2
STUB_CENTER_FROM_TOP = 5.7
STUB_CENTER_FROM_FRONT = TOP_WALL_HEIGHT + WALL_DEPTH
PEG_RADIUS = (5 - 0.25) / 2
PEG_HEIGHT = 22

front_plate = Box(
    WIDTH, HEIGHT, WALL_DEPTH, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
front_plate = fillet(
    front_plate.edges().filter_by(Axis.Z).group_by(Axis.X)[-1].group_by(Axis.Y)[0],
    radius=BIG_CORNER_RADIUS,
)
front_plate = fillet(
    front_plate.edges().filter_by(Axis.Z).group_by(Axis.X)[0],
    radius=SMALL_CORNER_RADIUS,
)
front_plate = fillet(
    front_plate.edges().filter_by(Axis.Z).group_by(Axis.X)[-1].group_by(Axis.Y)[-1],
    radius=SMALL_CORNER_RADIUS,
)
front_plate = chamfer(
    front_plate.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
    length=FRONT_CORNER_RADIUS,
)

wall = make_face(
    [
        Line((0, SMALL_CORNER_RADIUS), (0, HEIGHT - SMALL_CORNER_RADIUS)),
        RadiusArc(
            (0, HEIGHT - SMALL_CORNER_RADIUS),
            (WALL_DEPTH, HEIGHT),
            SMALL_CORNER_RADIUS,
        ),
        Line((WALL_DEPTH, HEIGHT), (WALL_DEPTH, WALL_DEPTH)),
        Line((WALL_DEPTH, WALL_DEPTH), (BOTTOM_SIDE_WALLS_WIDTH, WALL_DEPTH)),
        RadiusArc(
            (BOTTOM_SIDE_WALLS_WIDTH, WALL_DEPTH),
            (WIDTH - BOTTOM_SIDE_WALLS_WIDTH, WALL_DEPTH),
            BOTTOM_CURVE_RADIUS,
        ),
        Line(
            (WIDTH - BOTTOM_SIDE_WALLS_WIDTH, WALL_DEPTH),
            (WIDTH - WALL_DEPTH - BIG_CORNER_RADIUS, WALL_DEPTH),
        ),
        RadiusArc(
            (WIDTH - WALL_DEPTH - BIG_CORNER_RADIUS, WALL_DEPTH),
            (WIDTH - WALL_DEPTH, WALL_DEPTH + BIG_CORNER_RADIUS),
            -BIG_CORNER_RADIUS,
        ),
        Line(
            (WIDTH - WALL_DEPTH, WALL_DEPTH + BIG_CORNER_RADIUS),
            (WIDTH - WALL_DEPTH, HEIGHT - IN_HEIGHT - WALL_DEPTH),
        ),
        Line(
            (WIDTH - WALL_DEPTH, HEIGHT - IN_HEIGHT - WALL_DEPTH),
            (WIDTH - IN_WIDTH - WALL_DEPTH, HEIGHT - IN_HEIGHT - WALL_DEPTH),
        ),
        Line(
            (WIDTH - IN_WIDTH - WALL_DEPTH, HEIGHT - IN_HEIGHT - WALL_DEPTH),
            (WIDTH - IN_WIDTH - WALL_DEPTH, HEIGHT),
        ),
        Line((WIDTH - IN_WIDTH - WALL_DEPTH, HEIGHT), (WIDTH - IN_WIDTH, HEIGHT)),
        Line((WIDTH - IN_WIDTH, HEIGHT), (WIDTH - IN_WIDTH, HEIGHT - IN_HEIGHT)),
        Line((WIDTH - IN_WIDTH, HEIGHT - IN_HEIGHT), (WIDTH, HEIGHT - IN_HEIGHT)),
        Line((WIDTH, HEIGHT - IN_HEIGHT), (WIDTH, BIG_CORNER_RADIUS)),
        RadiusArc(
            (WIDTH, BIG_CORNER_RADIUS),
            (WIDTH - BIG_CORNER_RADIUS, 0),
            BIG_CORNER_RADIUS,
        ),
        Line((WIDTH - BIG_CORNER_RADIUS, 0), (WIDTH - BOTTOM_SIDE_WALLS_WIDTH, 0)),
        RadiusArc(
            (WIDTH - BOTTOM_SIDE_WALLS_WIDTH, 0),
            (BOTTOM_SIDE_WALLS_WIDTH, 0),
            -BOTTOM_CURVE_RADIUS,
        ),
        Line((BOTTOM_SIDE_WALLS_WIDTH, 0), (SMALL_CORNER_RADIUS, 0)),
        RadiusArc(
            (SMALL_CORNER_RADIUS, 0),
            (0, SMALL_CORNER_RADIUS),
            SMALL_CORNER_RADIUS,
        ),
    ]
)
wall = extrude(wall, WALL_HEIGHT)
wall = Pos(-WIDTH / 2, -HEIGHT / 2, WALL_DEPTH) * wall

top_wall = Pos(
    WALL_DEPTH,
    HEIGHT - WALL_DEPTH,
) * Box(WIDTH - IN_WIDTH - WALL_DEPTH, WALL_DEPTH, TOP_WALL_HEIGHT, align=Align.MIN)
top_wall = Pos(-WIDTH / 2, -HEIGHT / 2, WALL_DEPTH) * top_wall

stub_wall = Box(WALL_DEPTH, STUB_WALL_WIDTH, STUB_WALL_HEIGHT, align=Align.MIN)
stub_wall = fillet(
    stub_wall.edges().filter_by(Axis.X).group_by(Axis.Y)[-1].group_by(Axis.Z)[-1],
    STUB_WALL_TOP_CORNER_RADIUS,
)
stub_wall &= extrude(
    make_face(
        [
            Line((0, 0), (WALL_DEPTH, 0)),
            Line((WALL_DEPTH, 0), (WALL_DEPTH, STUB_WALL_WIDTH)),
            RadiusArc(
                (WALL_DEPTH, STUB_WALL_WIDTH),
                (0, STUB_WALL_WIDTH - SMALL_CORNER_RADIUS),
                -SMALL_CORNER_RADIUS,
            ),
            Line((0, STUB_WALL_WIDTH - SMALL_CORNER_RADIUS), (0, 0)),
        ]
    ),
    STUB_WALL_HEIGHT,
)
stub_wall = fillet(
    stub_wall.edges().filter_by(Axis.X).group_by(Axis.Y)[0].group_by(Axis.Z)[-1],
    STUB_WALL_BOTTOM_CORNER_RADIUS,
)
stub_wall = Pos(-WIDTH / 2, HEIGHT / 2 - STUB_WALL_WIDTH, WALL_DEPTH) * stub_wall

peg_wall = Box(WALL_DEPTH, STUB_WALL_WIDTH, STUB_WALL_HEIGHT, align=Align.MIN)
peg_wall = fillet(
    peg_wall.edges().filter_by(Axis.X).group_by(Axis.Y)[-1].group_by(Axis.Z)[-1],
    STUB_WALL_TOP_CORNER_RADIUS,
)
peg_wall = fillet(
    peg_wall.edges().filter_by(Axis.X).group_by(Axis.Y)[0].group_by(Axis.Z)[-1],
    STUB_WALL_BOTTOM_CORNER_RADIUS,
)
peg_wall = (
    Pos(WIDTH / 2 - IN_WIDTH - WALL_DEPTH, HEIGHT / 2 - STUB_WALL_WIDTH, WALL_DEPTH)
    * peg_wall
)

stub_step = (
    Pos(
        -WIDTH / 2 - STUB_STEP_HEIGHT,
        HEIGHT / 2 - STUB_CENTER_FROM_TOP - STUB_STEP_RADIUS,
        STUB_CENTER_FROM_FRONT - STUB_STEP_RADIUS,
    )
    * Rot(0, 90, 90)
    * Cylinder(STUB_STEP_RADIUS, STUB_STEP_HEIGHT + WALL_DEPTH, align=Align.MIN)
)

peg_step = (
    Pos(
        WIDTH / 2 - IN_WIDTH,
        HEIGHT / 2 - STUB_CENTER_FROM_TOP - STUB_STEP_RADIUS,
        STUB_CENTER_FROM_FRONT - STUB_STEP_RADIUS,
    )
    * Rot(0, 90, 90)
    * Cylinder(STUB_STEP_RADIUS, STUB_STEP_HEIGHT, align=Align.MIN)
)

stub = (
    Pos(
        -WIDTH / 2 - STUB_STEP_HEIGHT,
        HEIGHT / 2 - STUB_CENTER_FROM_TOP + STUB_BOTTOM_RADIUS,
        STUB_CENTER_FROM_FRONT - STUB_BOTTOM_RADIUS,
    )
    * Rot(0, -90, -90)
    * Cone(STUB_BOTTOM_RADIUS, STUB_TOP_RADIUS, STUB_HEIGHT, align=Align.MIN)
)

peg = (
    Pos(
        WIDTH / 2 - IN_WIDTH - STUB_STEP_HEIGHT,
        HEIGHT / 2 - STUB_CENTER_FROM_TOP - PEG_RADIUS,
        STUB_CENTER_FROM_FRONT - PEG_RADIUS,
    )
    * Rot(0, 90, 90)
    * Cylinder(PEG_RADIUS, PEG_HEIGHT, align=Align.MIN)
)

part = Part() + [
    front_plate,
    wall,
    top_wall,
    stub_wall,
    stub_step,
    stub,
    peg_wall,
    peg_step,
    peg,
]

export_step(part, os.path.splitext(__file__)[0] + ".step")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
