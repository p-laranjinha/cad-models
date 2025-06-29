import math
import os
from build123d import *  # pyright: ignore
from build123d import cast

# WARNING: Very sharp corners cause the bottom chamfer to fail and error.

INNER_ARC = 60
OUTER_ARC = 90
EXCEPTION_ARCS = {
    2: {"inner": 110},
    3: {"inner": 90},
    4: {"inner": 80},
    5: {"inner": 70},
}

WIDTH = 32
THICKNESS = 2

OTHER_CORNER_FILLET_RADIUS = 2

MIN_RADIUS = 2
MAX_RADIUS = 20

INITIAL_LAYER_HEIGHT = 0.28
LAYER_HEIGHT = 0.2
BOTTOM_CHAMFER_LENGTH = INITIAL_LAYER_HEIGHT + LAYER_HEIGHT

MAX_TEXT_SIZE = 8
TEXT_DEPTH = 0.5

TEXT_BOTTOM_RIGHT = True

OUTPUT_DIR = os.path.dirname(os.path.realpath(__file__)) + "/output"


def get_arc_straight_length(radius, arc):
    # Get the base of an isosceles triangle from the leg length and vertex angle
    return radius * math.sin(math.radians(arc / 2)) * 2


def get_arc_straight_distance_from_center(radius, arc):
    return radius * math.cos(math.radians(arc / 2))


def get_cut_length(radius, arc):
    arc_straight_length = get_arc_straight_length(radius, arc)
    # Use Pithagorean theorem to get equal legs from the hypotenuse
    return math.sqrt(math.pow(arc_straight_length, 2) / 2)


try:
    os.mkdir(OUTPUT_DIR)
except Exception:
    pass

part = None
for radius in range(MIN_RADIUS, MAX_RADIUS + 1):
    inner_arc = INNER_ARC
    outer_arc = OUTER_ARC

    if radius in EXCEPTION_ARCS:
        if "inner" in EXCEPTION_ARCS[radius]:
            inner_arc = EXCEPTION_ARCS[radius]["inner"]
        if "outer" in EXCEPTION_ARCS[radius]:
            outer_arc = EXCEPTION_ARCS[radius]["outer"]

    outer_arc_line = CenterArc((WIDTH - radius, radius), radius, 270, outer_arc)
    inner_arc_line = CenterArc(
        (
            get_arc_straight_length(radius, inner_arc) / 2,
            get_arc_straight_distance_from_center(radius, inner_arc),
        ),
        radius,
        270 - inner_arc / 2,
        inner_arc,
    )
    inner_arc_line = cast(
        CenterArc,
        Pos(
            0,
            (outer_arc_line @ 1).Y
            - (WIDTH - (outer_arc_line @ 1).X)
            + (WIDTH - (inner_arc_line @ 1).X),
        )
        * inner_arc_line,
    )

    part = make_face(
        [
            RadiusArc(
                (0, OTHER_CORNER_FILLET_RADIUS),
                (OTHER_CORNER_FILLET_RADIUS, 0),
                -OTHER_CORNER_FILLET_RADIUS,
            ),
            Line((OTHER_CORNER_FILLET_RADIUS, 0), outer_arc_line @ 0),
            outer_arc_line,
            Line(outer_arc_line @ 1, inner_arc_line @ 1),
            inner_arc_line,
            Line(inner_arc_line @ 0, (0, OTHER_CORNER_FILLET_RADIUS)),
        ]
    )
    part = extrude(part, THICKNESS)
    part = chamfer(
        part.edges().filter_by(Plane.XY).group_by(Axis.Z)[0], BOTTOM_CHAMFER_LENGTH
    )

    text_align = Align.MIN
    text_x_offset = OTHER_CORNER_FILLET_RADIUS
    if TEXT_BOTTOM_RIGHT:
        part = Pos(WIDTH) * mirror(part, Plane.YZ)
        text_align = (Align.MAX, Align.MIN)
        text_x_offset = WIDTH - OTHER_CORNER_FILLET_RADIUS

    text = Text(
        str(radius),
        min(
            MAX_TEXT_SIZE * (8 / 5.8),
            (
                WIDTH
                + get_arc_straight_distance_from_center(radius, inner_arc)
                - radius
                - 2 * OTHER_CORNER_FILLET_RADIUS
            )
            * (8 / 5.8),
        ),
        font="Overpass",
        font_path=os.path.dirname(os.path.realpath(__file__)) + "/overpass-heavy.otf",
        align=text_align,
    )
    text = extrude(text, TEXT_DEPTH)
    text = (
        Pos(
            text_x_offset,
            OTHER_CORNER_FILLET_RADIUS,
            THICKNESS - TEXT_DEPTH,
        )
        * text
    )

    part = Part() + part - text

    export_stl(
        part,
        OUTPUT_DIR
        + "/piece-"
        + str(radius).rjust(len(str(MAX_RADIUS)) - len(str(radius)) + 1, "0")
        + ".stl",
    )
