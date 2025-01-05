import os
from build123d import (
    Align,
    Axis,
    CenterArc,
    Circle,
    Ellipse,
    Line,
    Location,
    Rectangle,
    export_step,
    extrude,
    fillet,
    loft,
    make_face,
)
from gridfinity_build123d import (
    BaseEqual,
    Bin,
    Compartment,
    CompartmentsEqual,
    StackingLip,
)

from yacv_server import show


def EartipPeg():
    PEG_TOP_WIDTH = 6
    PEG_TOP_HEIGHT = 7
    PEG_DEPTH = 6
    PEG_BOTTOM_WIDTH = PEG_TOP_WIDTH - 0.4
    PEG_BOTTOM_HEIGHT = PEG_TOP_HEIGHT - 0.4
    PEG_VERTICAL_BAR_WIDTH = 1.38
    PEG_TOP_DEPTH = 1.2

    peg_bottom = extrude(
        Ellipse(PEG_BOTTOM_WIDTH / 2, PEG_BOTTOM_HEIGHT / 2),
        PEG_DEPTH - PEG_TOP_DEPTH,
    )
    peg_top = extrude(
        Ellipse(PEG_TOP_WIDTH / 2, PEG_TOP_HEIGHT / 2), PEG_TOP_DEPTH
    ).move(Location((0, 0, PEG_DEPTH - PEG_TOP_DEPTH)))
    peg_top = fillet(peg_top.edges().group_by(Axis.Z)[-1], 0.5)

    peg_vertical_bar = extrude(
        Ellipse(PEG_TOP_WIDTH / 2, PEG_TOP_HEIGHT / 2)
        - Rectangle(PEG_TOP_WIDTH / 2, PEG_TOP_HEIGHT).move(
            Location((PEG_TOP_WIDTH / 4 + PEG_VERTICAL_BAR_WIDTH / 2, 0))
        )
        - Rectangle(PEG_TOP_WIDTH / 2, PEG_TOP_HEIGHT).move(
            Location((-PEG_TOP_WIDTH / 4 - PEG_VERTICAL_BAR_WIDTH / 2, 0))
        ),
        PEG_DEPTH - PEG_TOP_DEPTH,
    )
    return peg_bottom + peg_top + peg_vertical_bar


def EarwingPeg():

    WING_BASE_DIAMETER = 9.5
    WING_BASE_RADIUS = WING_BASE_DIAMETER / 2

    wing_base = Circle(WING_BASE_RADIUS)

    wing_middle = make_face(
        (
            CenterArc((WING_BASE_RADIUS / 3, 0), WING_BASE_RADIUS, -90, 180)
            + CenterArc((-WING_BASE_RADIUS / 3, 0), WING_BASE_RADIUS, 90, 180)
            + Line(
                (WING_BASE_RADIUS / 3, WING_BASE_RADIUS),
                (-WING_BASE_RADIUS / 3, WING_BASE_RADIUS),
            )
            + Line(
                (WING_BASE_RADIUS / 3, -WING_BASE_RADIUS),
                (-WING_BASE_RADIUS / 3, -WING_BASE_RADIUS),
            )
        ).edges()
    ).move(Location((0, 0, 2.5)))

    wing_top = make_face(
        (
            CenterArc((WING_BASE_RADIUS, 0), WING_BASE_RADIUS, -90, 180)
            + CenterArc((-WING_BASE_RADIUS, 0), WING_BASE_RADIUS, 90, 180)
            + Line(
                (WING_BASE_RADIUS, WING_BASE_RADIUS),
                (-WING_BASE_RADIUS, WING_BASE_RADIUS),
            )
            + Line(
                (WING_BASE_RADIUS, -WING_BASE_RADIUS),
                (-WING_BASE_RADIUS, -WING_BASE_RADIUS),
            )
        ).edges()
    ).move(Location((0, 0, 5)))
    wing = loft([wing_base, wing_middle, wing_top])
    wing = fillet(wing.edges().group_by(Axis.Z)[-1], 1)
    return wing.rotate(Axis.Z, 90)


part = Bin(
    BaseEqual(grid_x=3, grid_y=3, align=(Align.CENTER, Align.CENTER, Align.MAX)),
    height_in_units=3,
    compartments=CompartmentsEqual(compartment_list=[Compartment()]),
    lip=StackingLip(),
)

EARTIP_SPACE_X = 15
EARTIP_SPACE_Y = 20
EARWING_SPACE_X = 20
EARWING_SPACE_Y = 30

eartip_locations = [
    (-EARTIP_SPACE_X * 5 / 2 - 5, EARTIP_SPACE_Y * 3 / 2 + 7.5),
    (-EARTIP_SPACE_X * 3 / 2 - 5, EARTIP_SPACE_Y * 3 / 2 + 7.5),
    (-EARTIP_SPACE_X * 5 / 2 - 5, EARTIP_SPACE_Y * 1 / 2 + 2.5),
    (-EARTIP_SPACE_X * 3 / 2 - 5, EARTIP_SPACE_Y * 1 / 2 + 2.5),
    (-EARTIP_SPACE_X * 5 / 2 - 5, -EARTIP_SPACE_Y * 1 / 2 - 2.5),
    (-EARTIP_SPACE_X * 3 / 2 - 5, -EARTIP_SPACE_Y * 1 / 2 - 2.5),
    (-EARTIP_SPACE_X * 5 / 2 - 5, -EARTIP_SPACE_Y * 3 / 2 - 7.5),
    (-EARTIP_SPACE_X * 3 / 2 - 5, -EARTIP_SPACE_Y * 3 / 2 - 7.5),
    (-EARTIP_SPACE_X * 1 / 2 - 5, EARTIP_SPACE_Y + 5),
    (EARTIP_SPACE_X * 1 / 2 - 5, EARTIP_SPACE_Y + 5),
    (-EARTIP_SPACE_X * 1 / 2 - 5, 0),
    (EARTIP_SPACE_X * 1 / 2 - 5, 0),
    (-EARTIP_SPACE_X * 1 / 2 - 5, -EARTIP_SPACE_Y - 5),
    (EARTIP_SPACE_X * 1 / 2 - 5, -EARTIP_SPACE_Y - 5),
]
pegs = [EartipPeg().move(Location(location)) for location in eartip_locations]
earwing_locations = [
    (EARTIP_SPACE_X + EARWING_SPACE_X * 1 / 2 - 5, EARWING_SPACE_Y + 5),
    (EARTIP_SPACE_X + EARWING_SPACE_X * 3 / 2 - 5, EARWING_SPACE_Y + 5),
    (EARTIP_SPACE_X + EARWING_SPACE_X * 1 / 2 - 5, 0),
    (EARTIP_SPACE_X + EARWING_SPACE_X * 3 / 2 - 5, 0),
    (EARTIP_SPACE_X + EARWING_SPACE_X * 1 / 2 - 5, -EARWING_SPACE_Y - 5),
    (EARTIP_SPACE_X + EARWING_SPACE_X * 3 / 2 - 5, -EARWING_SPACE_Y - 5),
]
pegs += [EarwingPeg().move(Location(location)) for location in earwing_locations]
for peg in pegs:
    part += peg

export_step(part, os.path.splitext(__file__)[0] + ".step")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
