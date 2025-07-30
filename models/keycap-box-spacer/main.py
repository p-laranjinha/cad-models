import os
from build123d import cast
from ocp_vscode import *  # pyright: ignore
from build123d import *  # pyright: ignore

# I was making this with the intention of having keycaps be more secure in
#  Kalih Box switches but but apparently the keycap stem is already the right size

# Taken and adapted from ../keycaps/main.py
HEIGHT = 9.1
BOTTOM_WIDTH = 18
TOP_WIDTH = 14.1
WALL_BOTTOM_WIDTH = 17
WALL_TOP_WIDTH = 9
WALL_THICKNESS = 1
BOTTOM_CHAMFER_LENGTH = 0.2 + 0.28
TOP_FILLET_RADIUS = 0.5
CORNER_TOP_RADIUS = 4
CORNER_BOTTOM_RADIUS = 0.7
WALL_RADIUS = HEIGHT * 1.5
TOP_CUT_DEPTH = 2
TOP_CUT_RADIUS = 30
TOP_CUT_CENTER = HEIGHT + TOP_CUT_RADIUS - TOP_CUT_DEPTH
STEM_CHAMFER_LENGTH = 1.2
STEM_Z_OFFSET = 1.5
STEM_CROSS_HEIGHT = 4.1
STEM_CROSS_THICK = 1.17
STEM_DEPTH = 3.8
STEM_RAD = 5.5 / 2
STEM_INNER_RAD = 0.3
STEM_TOLERANCE = 0.05
STEM_REINFORCE_W = 6
STEM_REINFORCE_H = 4
STEM_REINFORCE_RAD = 0.4

SPACER_WIDTH = 10
SPACER_TOLERANCE = 0.2
SPACER_RADIUS = 1


def build_spacer():
    # We need to first build a lot of the keycap to get our spacer height
    wall_bottom_line = Line(
        (-WALL_BOTTOM_WIDTH / 2, -BOTTOM_WIDTH / 2),
        (WALL_BOTTOM_WIDTH / 2, -BOTTOM_WIDTH / 2),
    )
    wall_left_line = RadiusArc(
        (-WALL_BOTTOM_WIDTH / 2, -BOTTOM_WIDTH / 2),
        (-WALL_TOP_WIDTH / 2, -TOP_WIDTH / 2, HEIGHT),
        WALL_RADIUS,
    )
    wall_left_line = wall_left_line.rotate(
        Axis(
            (-WALL_BOTTOM_WIDTH / 2, -BOTTOM_WIDTH / 2),
            (
                -WALL_TOP_WIDTH / 2 + WALL_BOTTOM_WIDTH / 2,
                -TOP_WIDTH / 2 + BOTTOM_WIDTH / 2,
                HEIGHT,
            ),
        ),
        90,
    )
    wall_right_line = RadiusArc(
        (WALL_BOTTOM_WIDTH / 2, -BOTTOM_WIDTH / 2),
        (WALL_TOP_WIDTH / 2, -TOP_WIDTH / 2, HEIGHT),
        WALL_RADIUS,
    )
    if WALL_TOP_WIDTH > 0:
        wall_top_line = Line(
            (-WALL_TOP_WIDTH / 2, -TOP_WIDTH / 2), (WALL_TOP_WIDTH / 2, -TOP_WIDTH / 2)
        )
        wall_top_line = Pos(Z=HEIGHT) * wall_top_line
        wall_top_line = cast(Line, wall_top_line)
        wall = [wall_top_line, wall_bottom_line, wall_right_line, wall_left_line]
    else:
        wall = [wall_bottom_line, wall_right_line, wall_left_line]
    wall = Face.make_surface(wall)
    front_wall = wall
    right_wall = cast(Face, Rot(Z=90) * wall)
    back_wall = cast(Face, Rot(Z=180) * wall)
    left_wall = cast(Face, Rot(Z=270) * wall)

    front_wall_right_edge = front_wall.edges().sort_by_distance(
        (-WALL_BOTTOM_WIDTH / 2, -BOTTOM_WIDTH / 2)
    )[-1]
    right_wall_left_edge = right_wall.edges().sort_by_distance(
        (BOTTOM_WIDTH / 2, WALL_BOTTOM_WIDTH / 2)
    )[-1]
    front_right_corner = [
        front_wall_right_edge,
        RadiusArc(
            right_wall_left_edge.vertices().sort_by(Axis.Z)[-1],
            front_wall_right_edge.vertices().sort_by(Axis.Z)[-1],
            CORNER_TOP_RADIUS,
        ),
        right_wall_left_edge,
        RadiusArc(
            right_wall_left_edge.vertices().sort_by(Axis.Z)[0],
            front_wall_right_edge.vertices().sort_by(Axis.Z)[0],
            CORNER_BOTTOM_RADIUS,
        ),
    ]
    front_right_corner = Face.make_surface(front_right_corner)
    front_left_corner = Rot(Z=90) * front_right_corner
    front_left_corner = cast(Face, front_left_corner)
    back_left_corner = Rot(Z=180) * front_right_corner
    back_left_corner = cast(Face, back_left_corner)
    back_right_corner = Rot(Z=270) * front_right_corner
    back_right_corner = cast(Face, back_right_corner)
    keycap = Part() + [
        loft((front_wall, back_wall)),
        loft((left_wall, right_wall)),
        loft((front_right_corner, back_left_corner)),
        loft((front_left_corner, back_right_corner)),
    ]
    cut = Sphere(TOP_CUT_RADIUS)
    cut = Pos(Z=TOP_CUT_CENTER) * cut
    keycap_tmp = keycap - cut
    cut_edges = new_edges(keycap, cut, combined=keycap_tmp)
    keycap_tmp_edges = keycap_tmp.edges()
    same_cut_edges = []
    for i in range(len(keycap_tmp_edges)):
        if keycap_tmp_edges[i] in cut_edges:
            same_cut_edges.append(keycap_tmp_edges[i])
    keycap_tmp = fillet(
        same_cut_edges,
        TOP_FILLET_RADIUS,
    )
    LOST_HEIGHT = HEIGHT - bounding_box(keycap_tmp).vertices().sort_by(Axis.Z)[-1].Z

    spacer = RectangleRounded(SPACER_WIDTH, SPACER_WIDTH, SPACER_RADIUS)
    spacer -= Circle(STEM_RAD + SPACER_TOLERANCE)
    spacer = extrude(
        spacer,
        HEIGHT - STEM_Z_OFFSET - TOP_CUT_DEPTH + LOST_HEIGHT - WALL_THICKNESS - 1,
    )
    spacer = Pos(Z=STEM_Z_OFFSET) * spacer
    spacer = chamfer(spacer.edges().filter_by(Plane.XY), BOTTOM_CHAMFER_LENGTH)

    return spacer


part = build_spacer()

export_step(
    part,
    os.path.dirname(os.path.realpath(__file__)) + "/keycap-box-space.step",
)

show_all()
