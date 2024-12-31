from build123d import (
    Axis,
    CenterArc,
    Circle,
    Compound,
    Line,
    Location,
    Polyline,
    export_stl,
    extrude,
    make_face,
)

OPEN_DEGREE = 180

INNER_DIAMETER = 37
INNER_RADIUS = INNER_DIAMETER / 2
SIDE_PEG_DIAMETER = 9.5
SIDE_PEG_RADIUS = SIDE_PEG_DIAMETER / 2
SIDE_PEG_HEIGHT = 6

ARC_HALF_HEIGHT = SIDE_PEG_RADIUS + 2
ARC_THICKNESS = 3
INNER_HINGE_RADIUS = 2
HINGE_THICKNESS = 2

TOLERANCE_GAP = 0.25

# Top half-circle
top_arc_inner = CenterArc((0, 0), INNER_RADIUS, 1, 179)
top_arc_outer = CenterArc((0, 0), INNER_RADIUS + ARC_THICKNESS, 0, 170)
top_arc_clip_end = Line((-INNER_RADIUS, 0), (-INNER_RADIUS - ARC_THICKNESS - 3, 0))
top_arc_hinge_end = Line(top_arc_inner @ 0, top_arc_outer @ 0)
top_arc = top_arc_inner + top_arc_outer + top_arc_clip_end + top_arc_hinge_end

# Top part of the clip
top_clip = Polyline(
    [
        top_arc_clip_end @ 1,
        (-INNER_RADIUS - ARC_THICKNESS, -2),
        (-INNER_RADIUS - ARC_THICKNESS - 3, -4),
        (-INNER_RADIUS - ARC_THICKNESS - 5, -4),
        (-INNER_RADIUS - ARC_THICKNESS - 5, 2),
        top_arc_outer @ 1,
    ]
).wire()

# Top part of the hinge
top_hinge_arc_wall = CenterArc((0, 0), INNER_RADIUS + ARC_THICKNESS, 0, 15)
top_hinge_hinge_wall = CenterArc(
    (INNER_RADIUS + ARC_THICKNESS + HINGE_THICKNESS + INNER_HINGE_RADIUS, 0),
    INNER_HINGE_RADIUS - TOLERANCE_GAP,
    60,
    -180,
)
top_hinge_top_wall = Line(top_hinge_arc_wall @ 1, top_hinge_hinge_wall @ 0)
top_hinge_bottom_wall = Line(
    (INNER_RADIUS + ARC_THICKNESS, 0), top_hinge_hinge_wall @ 1
)
top_hinge_connection = (
    top_hinge_arc_wall
    + top_hinge_hinge_wall
    + top_hinge_top_wall
    + top_hinge_bottom_wall
)
inner_hinge = CenterArc(
    (INNER_RADIUS + ARC_THICKNESS + HINGE_THICKNESS + INNER_HINGE_RADIUS, 0),
    INNER_HINGE_RADIUS - TOLERANCE_GAP,
    0,
    360,
)

# Bottom half-cicle
bottom_arc_inner = CenterArc((0, 0), INNER_RADIUS, -1, -179)
bottom_arc_outer = CenterArc((0, 0), INNER_RADIUS + ARC_THICKNESS, 0, -165)
top_arc_clip_end = Line(
    (-INNER_RADIUS, 0), (-INNER_RADIUS - ARC_THICKNESS - 3 + TOLERANCE_GAP, 0)
)
bottom_arc_clip_end = top_arc_clip_end
bottom_arc_hinge_end = Line(bottom_arc_inner @ 0, bottom_arc_outer @ 0)
bottom_arc = (
    bottom_arc_inner + bottom_arc_outer + bottom_arc_clip_end + bottom_arc_hinge_end
)

# Bottom part of the clip
bottom_clip = Polyline(
    [
        bottom_arc_clip_end @ 1,
        (-INNER_RADIUS - ARC_THICKNESS + TOLERANCE_GAP, -2),
        (-INNER_RADIUS - ARC_THICKNESS - 3 + TOLERANCE_GAP, -4),
        bottom_arc_outer @ 1,
    ]
).wire()

# Bottom part of the hinge
bottom_hinge_arc_wall = CenterArc((0, 0), INNER_RADIUS + ARC_THICKNESS, 0, -20)
bottom_hinge_hinge_wall = CenterArc(
    (INNER_RADIUS + ARC_THICKNESS + HINGE_THICKNESS + INNER_HINGE_RADIUS, 0),
    INNER_HINGE_RADIUS + HINGE_THICKNESS - TOLERANCE_GAP,
    180,
    -270,
)
bottom_hinge_top_wall = Line(
    (INNER_RADIUS + ARC_THICKNESS, 0), bottom_hinge_hinge_wall @ 0
)
bottom_hinge_bottom_wall = Line(bottom_hinge_arc_wall @ 1, bottom_hinge_hinge_wall @ 1)
bottom_hinge_connection = (
    bottom_hinge_arc_wall
    + bottom_hinge_hinge_wall
    + bottom_hinge_top_wall
    + bottom_hinge_bottom_wall
)
inner_hinge_hole = CenterArc(
    (INNER_RADIUS + ARC_THICKNESS + HINGE_THICKNESS + INNER_HINGE_RADIUS, 0),
    INNER_HINGE_RADIUS,
    0,
    360,
)

# Extrusions
top_full_arc_face = make_face(top_arc + top_clip)
top_full_arc_part = extrude(top_full_arc_face, ARC_HALF_HEIGHT, both=True)

top_hinge_connection_face = make_face(top_hinge_connection)
top_hinge_connection_part = extrude(
    top_hinge_connection_face, ARC_HALF_HEIGHT, both=True
)
top_hinge_connection_part -= extrude(
    top_hinge_connection_face, ARC_HALF_HEIGHT / 2, both=True
)

inner_hinge_face = make_face(inner_hinge)
inner_hinge_part = extrude(inner_hinge_face, ARC_HALF_HEIGHT, both=True)
top_hinge_connection_part -= inner_hinge_part

bottom_full_arc_face = make_face(bottom_arc + bottom_clip)
bottom_full_arc_part = extrude(bottom_full_arc_face, ARC_HALF_HEIGHT, both=True)

bottom_hinge_connection_face = make_face(bottom_hinge_connection)
bottom_hinge_connection_part = extrude(
    bottom_hinge_connection_face, ARC_HALF_HEIGHT / 2 - TOLERANCE_GAP, both=True
)
inner_hinge_hole_face = make_face(inner_hinge_hole)
bottom_hinge_connection_part -= extrude(
    inner_hinge_hole_face, ARC_HALF_HEIGHT, both=True
)

# Side peg
side_peg_circle = Circle(SIDE_PEG_RADIUS)
side_peg_cylinder = extrude(side_peg_circle, SIDE_PEG_HEIGHT)
side_peg_cylinder = side_peg_cylinder.rotate(Axis.X, 90)
side_peg_cylinder = side_peg_cylinder.rotate(Axis.Z, 135)
side_peg_guide = CenterArc((0, 0), INNER_RADIUS, 180, 45)
side_peg_cylinder = side_peg_cylinder.move(Location(side_peg_guide @ 1))

top_part = top_full_arc_part + top_hinge_connection_part + inner_hinge_part
bottom_part = bottom_full_arc_part + bottom_hinge_connection_part + side_peg_cylinder
bottom_part = bottom_part.rotate(
    Location(
        (INNER_RADIUS + ARC_THICKNESS + HINGE_THICKNESS + INNER_HINGE_RADIUS, 0)
    ).to_axis(),
    OPEN_DEGREE,
)
part = Compound([top_part, bottom_part])

# show_object is a CQ-editor thing.
if "show_object" in globals():
    show_object(part, name="Part", options=dict(color="white"))  # pyright: ignore

export_stl(part, "./grandma.stl")
