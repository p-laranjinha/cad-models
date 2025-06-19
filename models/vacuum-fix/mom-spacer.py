import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show

INNER_RADIUS = 32 / 2
INNER_SPACE_BETWEEN_SEMICIRCLES = 36 - INNER_RADIUS * 2
SIDE_PEG_RADIUS = 7.65 / 2
SIDE_PEG_HEIGHT = 4
OUTER_RADIUS = 39 / 2 - 0.8

outer_face = Circle(OUTER_RADIUS)

inner_face = Pos(-INNER_RADIUS, -INNER_SPACE_BETWEEN_SEMICIRCLES / 2) * make_face(
    [
        Line((0, 0), (0, INNER_SPACE_BETWEEN_SEMICIRCLES)),
        RadiusArc(
            (0, INNER_SPACE_BETWEEN_SEMICIRCLES),
            (INNER_RADIUS * 2, INNER_SPACE_BETWEEN_SEMICIRCLES),
            INNER_RADIUS,
        ),
        Line(
            (INNER_RADIUS * 2, INNER_SPACE_BETWEEN_SEMICIRCLES), (INNER_RADIUS * 2, 0)
        ),
        RadiusArc((INNER_RADIUS * 2, 0), (0, 0), INNER_RADIUS),
    ]
)

ring = extrude(cast(Face, outer_face - inner_face), SIDE_PEG_RADIUS * 2)

peg = Cylinder(SIDE_PEG_RADIUS, SIDE_PEG_HEIGHT, align=Align.MIN)
peg = (
    Pos(-SIDE_PEG_RADIUS, INNER_RADIUS + INNER_SPACE_BETWEEN_SEMICIRCLES / 2)
    * Rot(90)
    * peg
)

part = Part() + [ring, peg]

export_step(part, os.path.splitext(__file__)[0] + ".step")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
