from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore

WATER_BOWL_HOLDER_HEIGHT = 70
FOOD_BOWL_HOLDER_HEIGHT = 90
WATER_BOWL_OUTER_RADIUS = 175.5 / 2
WATER_BOWL_INNER_RADIUS = WATER_BOWL_OUTER_RADIUS - 7.6
WATER_BOWL_HEIGHT = 55
WATER_BOWL_LIP = 1.7 + 0.3
FOOD_BOWL_OUTER_RADIUS = 152 / 2
FOOD_BOWL_INNER_RADIUS = FOOD_BOWL_OUTER_RADIUS - 6.6
FOOD_BOWL_HEIGHT = 33.7
FOOD_BOWL_LIP = 1.7
FOOD_BOWL_ANGLE = 10

water_bowl_holder = Box(
    WATER_BOWL_OUTER_RADIUS * 2 + 10,
    WATER_BOWL_OUTER_RADIUS * 2 + 10,
    WATER_BOWL_HOLDER_HEIGHT,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)
water_bowl_holder = fillet(
    water_bowl_holder.edges()
    .filter_by(Axis.Z)
    .group_by(Axis.Y)[0]
    .group_by(Axis.X)[-1],
    30,
)
water_bowl_holder = fillet(
    water_bowl_holder.edges().filter_by(Axis.Z).group_by(Axis.Y)[-1], 5
)
water_bowl_holder = fillet(
    water_bowl_holder.edges().filter_by(Axis.Z).group_by(Axis.Y)[0].group_by(Axis.X)[0],
    5,
)
water_bowl_holder = (
    water_bowl_holder
    - Cylinder(
        WATER_BOWL_INNER_RADIUS,
        WATER_BOWL_HOLDER_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MAX),
    )
    - Cylinder(
        WATER_BOWL_OUTER_RADIUS, 1, align=(Align.CENTER, Align.CENTER, Align.MAX)
    )
    - (
        Cylinder(
            WATER_BOWL_OUTER_RADIUS, 3, align=(Align.CENTER, Align.CENTER, Align.MAX)
        )
        - Cylinder(
            WATER_BOWL_OUTER_RADIUS - WATER_BOWL_LIP,
            3,
            align=(Align.CENTER, Align.CENTER, Align.MAX),
        )
    )
)
water_bowl_holder = chamfer(
    water_bowl_holder.edges().filter_by(Plane.XY).group_by(Axis.Z)[0], 1
)
water_bowl_holder_side_hole = (
    Rot(X=-90)
    * Pos(Z=WATER_BOWL_INNER_RADIUS - 2)
    * (
        Cylinder(
            12,
            WATER_BOWL_OUTER_RADIUS - WATER_BOWL_INNER_RADIUS + 7,
            align=(Align.CENTER, Align.CENTER, Align.MIN),
        )
        - fillet(
            extrude(
                Circle(15) - Circle(10),
                WATER_BOWL_OUTER_RADIUS - WATER_BOWL_INNER_RADIUS + 7,
            ).edges(),
            1,
        )
    )
)
water_bowl_holder -= water_bowl_holder_side_hole
water_bowl_holder = fillet(
    water_bowl_holder.edges().filter_by(Plane.XY).group_by(Axis.Z)[-1], 1
)
water_bowl_holder = (
    Pos(
        X=-FOOD_BOWL_OUTER_RADIUS - WATER_BOWL_OUTER_RADIUS - 10,
        Y=-WATER_BOWL_OUTER_RADIUS - 5,
        Z=FOOD_BOWL_HEIGHT + WATER_BOWL_HOLDER_HEIGHT - FOOD_BOWL_HOLDER_HEIGHT,
    )
    * water_bowl_holder
)

food_bowl_hole = extrude(
    cast(
        Face,
        Rot(X=FOOD_BOWL_ANGLE)
        * Pos(Y=-5)
        * Circle(FOOD_BOWL_OUTER_RADIUS, align=(Align.CENTER, Align.MAX)),
    ),
    3,
    dir=(0, 0, -1),
) + extrude(
    cast(
        Face,
        Rot(X=FOOD_BOWL_ANGLE)
        * Pos(Y=-(FOOD_BOWL_OUTER_RADIUS - FOOD_BOWL_INNER_RADIUS + 5))
        * Circle(FOOD_BOWL_INNER_RADIUS, align=(Align.CENTER, Align.MAX)),
    ),
    FOOD_BOWL_HOLDER_HEIGHT,
    dir=(0, 0, -1),
)
food_bowl_hole += Rot(X=90) * Cylinder(
    10, FOOD_BOWL_OUTER_RADIUS + 5, align=(Align.CENTER, Align.CENTER, Align.MIN)
)
food_bowl_hole += Rot(X=90) * (
    Cylinder(
        12,
        FOOD_BOWL_OUTER_RADIUS - FOOD_BOWL_INNER_RADIUS + 5.7,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    - fillet(
        extrude(
            Circle(15) - Circle(10),
            FOOD_BOWL_OUTER_RADIUS - FOOD_BOWL_INNER_RADIUS + 5.7,
        ).edges(),
        1,
    )
)
food_bowl_holder = extrude(
    cast(
        Face,
        Rot(X=FOOD_BOWL_ANGLE)
        * Rectangle(
            FOOD_BOWL_OUTER_RADIUS * 2 + 10,
            FOOD_BOWL_OUTER_RADIUS * 2 + 10,
            align=(Align.CENTER, Align.MAX),
        ),
    ),
    FOOD_BOWL_HOLDER_HEIGHT,
    dir=(0, 0, -1),
)
food_bowl_holder = split(
    food_bowl_holder, Plane.XY * Pos(Z=-FOOD_BOWL_HOLDER_HEIGHT + FOOD_BOWL_HEIGHT)
)
food_bowl_holder_middle = fillet(food_bowl_holder.edges().filter_by(Axis.Z), 5)
food_bowl_holder_middle = fillet(
    [
        edge
        for edge in food_bowl_holder_middle.edges().filter_by(Plane.XY)
        if edge
        not in food_bowl_holder_middle.edges().filter_by(Plane.XY).group_by(Axis.Z)[0]
    ],
    1,
)
food_bowl_holder_middle -= food_bowl_hole
food_bowl_holder_middle = chamfer(
    food_bowl_holder_middle.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
    1,
)

food_bowl_holder_side = fillet(
    food_bowl_holder.edges().filter_by(Axis.Z).group_by(Axis.Y)[-1], 5
)
food_bowl_holder_side = fillet(
    food_bowl_holder_side.edges()
    .filter_by(Axis.Z)
    .group_by(Axis.Y)[0]
    .group_by(Axis.X)[0],
    5,
)
food_bowl_holder_side = fillet(
    food_bowl_holder_side.edges()
    .filter_by(Axis.Z)
    .group_by(Axis.Y)[0]
    .group_by(Axis.X)[-1],
    30,
)
food_bowl_holder_side = fillet(
    [
        edge
        for edge in food_bowl_holder_side.edges().filter_by(Plane.XY)
        if edge
        not in food_bowl_holder_side.edges().filter_by(Plane.XY).group_by(Axis.Z)[0]
    ],
    1,
)
food_bowl_holder_side -= food_bowl_hole
food_bowl_holder_side = chamfer(
    food_bowl_holder_side.edges().filter_by(Plane.XY).group_by(Axis.Z)[0],
    1,
)
food_bowl_holder_side = Pos(X=FOOD_BOWL_OUTER_RADIUS * 2 + 10) * food_bowl_holder_side


export_step(
    water_bowl_holder,
    os.path.dirname(os.path.realpath(__file__)) + "/water-bowl-holder.step",
)
export_step(
    food_bowl_holder_middle,
    os.path.dirname(os.path.realpath(__file__)) + "/food-bowl-holder-middle.step",
)
export_step(
    food_bowl_holder_side,
    os.path.dirname(os.path.realpath(__file__)) + "/food-bowl-holder-side.step",
)

show(food_bowl_holder_middle, food_bowl_holder_side, water_bowl_holder)
