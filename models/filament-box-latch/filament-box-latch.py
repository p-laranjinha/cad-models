import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show

SEMICIRCLE_RADIUS = 9
SEMICIRCLE_HEIGHT = 4
SEMICIRCLE_WIDTH = 14.5
SEMICIRCLE_INNER_SPACER_WIDTH = 1
SEMICIRCLE_INNER_SPACER_RADIUS = 1
INNER_VERTICAL_LENGTH = 55.2 - 1
TOP_VERTICAL_LENGTH = 12.5
TOP_LENGTH_FROM_IN = 16.5


THICKNESS = SEMICIRCLE_RADIUS + 1.5
VERTICAL_RADIUS = INNER_VERTICAL_LENGTH
OUTER_HORIZONTAL_RADIUS = SEMICIRCLE_RADIUS * 2
EXTRA_LENGTH = 2

WIDE_THICKNESS = 30

part = extrude(
    make_face(
        [
            RadiusArc(
                (-EXTRA_LENGTH, -EXTRA_LENGTH),
                (THICKNESS + SEMICIRCLE_WIDTH, -EXTRA_LENGTH),
                -OUTER_HORIZONTAL_RADIUS,
            ),
            Line(
                (THICKNESS + SEMICIRCLE_WIDTH, -EXTRA_LENGTH),
                (THICKNESS + SEMICIRCLE_WIDTH, 0),
            ),
            RadiusArc(
                (THICKNESS + SEMICIRCLE_WIDTH, 0), (THICKNESS, 0), -SEMICIRCLE_RADIUS
            ),
            RadiusArc(
                (THICKNESS, 0),
                (THICKNESS - SEMICIRCLE_INNER_SPACER_WIDTH, 0),
                SEMICIRCLE_INNER_SPACER_RADIUS,
            ),
            RadiusArc(
                (THICKNESS - SEMICIRCLE_INNER_SPACER_WIDTH, 0),
                (
                    THICKNESS - SEMICIRCLE_INNER_SPACER_WIDTH - TOP_LENGTH_FROM_IN,
                    INNER_VERTICAL_LENGTH - TOP_VERTICAL_LENGTH,
                ),
                VERTICAL_RADIUS,
            ),
            Line(
                (
                    THICKNESS - SEMICIRCLE_INNER_SPACER_WIDTH - TOP_LENGTH_FROM_IN,
                    INNER_VERTICAL_LENGTH - TOP_VERTICAL_LENGTH,
                ),
                (
                    THICKNESS - SEMICIRCLE_INNER_SPACER_WIDTH - TOP_LENGTH_FROM_IN,
                    INNER_VERTICAL_LENGTH,
                ),
            ),
            Line(
                (
                    THICKNESS - SEMICIRCLE_INNER_SPACER_WIDTH - TOP_LENGTH_FROM_IN,
                    INNER_VERTICAL_LENGTH,
                ),
                (
                    THICKNESS * 3,
                    INNER_VERTICAL_LENGTH,
                ),
            ),
            Line(
                (
                    THICKNESS * 3,
                    INNER_VERTICAL_LENGTH,
                ),
                (
                    THICKNESS * 3,
                    INNER_VERTICAL_LENGTH + EXTRA_LENGTH,
                ),
            ),
            RadiusArc(
                (
                    THICKNESS * 3,
                    INNER_VERTICAL_LENGTH + EXTRA_LENGTH,
                ),
                (
                    -SEMICIRCLE_INNER_SPACER_WIDTH
                    - TOP_LENGTH_FROM_IN
                    + EXTRA_LENGTH
                    + EXTRA_LENGTH,
                    INNER_VERTICAL_LENGTH + EXTRA_LENGTH + EXTRA_LENGTH + EXTRA_LENGTH,
                ),
                -OUTER_HORIZONTAL_RADIUS * 2,
            ),
            RadiusArc(
                (
                    -SEMICIRCLE_INNER_SPACER_WIDTH
                    - TOP_LENGTH_FROM_IN
                    + EXTRA_LENGTH
                    + EXTRA_LENGTH,
                    INNER_VERTICAL_LENGTH + EXTRA_LENGTH + EXTRA_LENGTH + EXTRA_LENGTH,
                ),
                (-EXTRA_LENGTH, -EXTRA_LENGTH),
                -VERTICAL_RADIUS,
            ),
        ]
    ),
    WIDE_THICKNESS,
)

part = Part() + part

export_step(part, os.path.splitext(__file__)[0] + ".step")

part.color = (0.3, 0.3, 0.3, 1)
show([part])  # pyright: ignore
