import os
from build123d import cast
from numpy import double
from ocp_vscode import *  # pyright: ignore
from build123d import *  # pyright: ignore

# Deepest sound I found was low inner ceiling with low infill
# PETG sounds deeper than PLA, but the PETG surface is rougher

# Less than 3 side walls adds holes to the top and makes it look bad

# Having the seam at a corner can cause the corner to lift
# to fix this either don't have a minimum radius corner or paint the seam yourself

HEIGHT = 9.1
BOTTOM_WIDTH = 18
TOP_WIDTH = 14.1
WALL_BOTTOM_WIDTH = 17
WALL_TOP_WIDTH = 9
WALL_THICKNESS = 1
BOTTOM_CHAMFER_LENGTH = 0.2 + 0.28
TOP_FILLET_RADIUS = 0.5
CORNER_TOP_RADIUS = 4
CORNER_BOTTOM_RADIUS = 0.7  # Change this to change the corner curvature
WALL_RADIUS = HEIGHT * 1.5

TOP_CUT_DEPTH = 2
TOP_CUT_RADIUS = 30
TOP_CUT_CENTER = HEIGHT + TOP_CUT_RADIUS - TOP_CUT_DEPTH

STEM_CHAMFER_LENGTH = 1.2
STEM_Z_OFFSET = 1.5
# Stem info and code from https://github.com/nicola-sorace/custom-keycap-generator
STEM_CROSS_HEIGHT = 4.1
STEM_CROSS_THICK = 1.17
STEM_DEPTH = 3.8
STEM_RAD = 5.5 / 2
STEM_INNER_RAD = 0.3
STEM_TOLERANCE = 0.05
STEM_REINFORCE_W = 6
STEM_REINFORCE_H = 4
STEM_REINFORCE_RAD = 0.4

# If you're printing the text in another color, you can choose double the line
#  height and only have to change the filament twice, which is good for manual printing
TEXT_DEPTH = 0.2
TEXT_HEIGHT = 6

BUMP_THICKNESS = 0.75 / 2
BUMP_LENGTH = 3.3

# Font for regular letters and Nerd Font symbols
OVERPASS_FONT_PATH = (
    os.path.dirname(os.path.realpath(__file__)) + "/OverpassNerdFontPropo-Regular.otf"
)

# Font for regular special symbols like the Shift and Tab
FREESERIF_FONT_PATH = os.path.dirname(os.path.realpath(__file__)) + "/FreeSerif.otf"


def build_keycap(text=None, has_bump=False):
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
        # extrude(front_wall, TOP_WIDTH, (0, 1)),
        # extrude(right_wall, TOP_WIDTH, (-1, 0)),
        # extrude(back_wall, TOP_WIDTH, (0, -1)),
        # extrude(left_wall, TOP_WIDTH, (1, 0)),
        loft((front_wall, back_wall)),
        loft((left_wall, right_wall)),
        loft((front_right_corner, back_left_corner)),
        loft((front_left_corner, back_right_corner)),
    ]

    cut = Sphere(TOP_CUT_RADIUS)
    cut = Pos(Z=TOP_CUT_CENTER) * cut
    keycap_tmp = keycap - cut

    # Getting the edges cut before we cut the text, part 1
    cut_edges = new_edges(keycap, cut, combined=keycap_tmp)

    # Cutting some Nerd Font glyphs doesn't work if its with a full keycap, for some reason
    # and some others still don't work, usually the ones wth more separate parts
    if text != None:
        text = extrude(text, -TOP_CUT_DEPTH - TEXT_DEPTH)
        text = Pos(Z=HEIGHT) * text
        text = text - cut
        keycap_tmp -= text

    if has_bump:
        bump = Sphere(BUMP_THICKNESS)
        bump = split(bump, Plane.ZY)
        bump = Pos(-(BUMP_LENGTH - BUMP_THICKNESS) / 2) * bump
        bump = cast(Part, bump)
        bump += extrude(
            bump.faces().filter_by(Plane.YZ)[0], (BUMP_LENGTH - BUMP_THICKNESS) / 2
        )
        bump += Rot(Z=180) * bump
        # bump += extrude(bump.faces().filter_by(Plane.XY)[0], 2)
        bump = Pos(Y=-5, Z=HEIGHT - TOP_CUT_DEPTH + 0.4) * bump
        keycap_tmp += bump

    # Getting the edges cut before we cut the text, part 2
    keycap_tmp_edges = keycap_tmp.edges()
    same_cut_edges = []
    for i in range(len(keycap_tmp_edges)):
        if keycap_tmp_edges[i] in cut_edges:
            same_cut_edges.append(keycap_tmp_edges[i])

    keycap_tmp = fillet(
        same_cut_edges,
        TOP_FILLET_RADIUS,
    )
    # keycap_tmp = split(
    #     keycap_tmp,
    #     Plane.XY
    #     * Pos(
    #         Z=bounding_box(keycap_tmp).vertices().sort_by(Axis.Z)[-1].Z
    #         - TOP_FILLET_RADIUS
    #     ),
    #     keep=Keep.BOTTOM,
    # )

    LOST_HEIGHT = HEIGHT - bounding_box(keycap_tmp).vertices().sort_by(Axis.Z)[-1].Z
    if LOST_HEIGHT > 0:
        keycap_tmp += extrude(keycap_tmp.faces().sort_by(Axis.Z)[0], LOST_HEIGHT)
        keycap_tmp = Pos(Z=LOST_HEIGHT) * keycap_tmp
        if text != None:
            text = Pos(Z=LOST_HEIGHT) * text

        # I don't get why the extrusion needs more height for the chamfer, but oh well
        keycap_tmp -= extrude(
            keycap_tmp.faces().sort_by(Axis.Z)[0], -BOTTOM_CHAMFER_LENGTH * 2
        ) - chamfer(
            extrude(keycap_tmp.faces().sort_by(Axis.Z)[0], -BOTTOM_CHAMFER_LENGTH * 2)
            .edges()
            .group_by(Axis.Z)[0],
            BOTTOM_CHAMFER_LENGTH,
        )
    else:
        keycap_tmp = chamfer(
            keycap_tmp.edges().group_by(Axis.Z)[0], BOTTOM_CHAMFER_LENGTH
        )

    keycap_tmp = cast(Part, keycap_tmp)

    keycap = keycap_tmp - scale(
        keycap,
        (
            (BOTTOM_WIDTH - WALL_THICKNESS * 2) / BOTTOM_WIDTH,
            (BOTTOM_WIDTH - WALL_THICKNESS * 2) / BOTTOM_WIDTH,
            (HEIGHT + LOST_HEIGHT - TOP_CUT_DEPTH - WALL_THICKNESS - 1) / HEIGHT,
        ),
    )

    cross = Rectangle(
        STEM_CROSS_THICK + STEM_TOLERANCE, STEM_CROSS_HEIGHT + STEM_TOLERANCE
    ) + Rectangle(STEM_CROSS_HEIGHT + STEM_TOLERANCE, STEM_CROSS_THICK + STEM_TOLERANCE)
    cross = fillet(
        cross.vertices().sort_by_distance(Vector(0, 0, 0))[:4],
        STEM_INNER_RAD,
    )
    cross = cast(Face, cross)
    cross = extrude(cross, STEM_DEPTH)

    stem = Circle(STEM_RAD)
    # stem += RectangleRounded(STEM_REINFORCE_W, STEM_REINFORCE_H, STEM_REINFORCE_RAD)
    stem = extrude(stem, HEIGHT - TOP_CUT_DEPTH - STEM_Z_OFFSET - TEXT_DEPTH)
    stem -= cross
    stem = Pos(Z=STEM_Z_OFFSET) * stem
    stem = cast(Part, stem)

    keycap_tmp = keycap + stem
    # keycap = chamfer(new_edges(keycap, stem, combined=keycap_tmp), STEM_CHAMFER_LENGTH)
    keycap = keycap_tmp

    return keycap, text


SINGLE_GLYPHS = [c for c in "ABCDEGHIKLMNOPQRSTUVWXYZ󰝞󰝝󰖁󰐎󰌑󰁮󰹾󱁐󰌒"]

BUMP_SINGLE_GLYPS = ["F", "J"]

# For the keys with 2 glyhs, one on top of the other
DOUBLE_GLYPHS = [
    "`~",
    "1!",
    "2@",
    "3#",
    "4$",
    "5%",
    "6^",
    "7&",
    "8*",
    "9(",
    "0)",
    "-_",
    "=+",
    "[{",
    "]}",
    ";:",
    ["'", "''"],
    ",<",
    ".>",
    "/?",
]

WORD_GLYPHS = [
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
    "esc",
    "fn",
    "alt",
    "altgr",
    "shift",
    "shift",
    "ctrl",
    "ctrl",
]

BLANK_GLYPHS = 3

keycaps = []

for glyph in SINGLE_GLYPHS + WORD_GLYPHS:
    keycap_body, text = build_keycap(
        Text(glyph, TEXT_HEIGHT, font_path=OVERPASS_FONT_PATH)
    )
    text = cast(Part, text)
    keycap_body.label = "keycap"
    text.label = "text"  # Doesn't work on the export but works on the show
    keycap = Compound(children=[keycap_body, text])
    keycap.label = glyph
    keycaps.append(keycap)

for double_glyph in DOUBLE_GLYPHS:
    bottom_glyph, top_glyph = [c for c in double_glyph]
    bottom_text = Text(bottom_glyph, TEXT_HEIGHT, font_path=OVERPASS_FONT_PATH)
    bottom_text = Pos(Y=-TEXT_HEIGHT / 2) * bottom_text
    top_text = Text(top_glyph, TEXT_HEIGHT, font_path=OVERPASS_FONT_PATH)
    top_text = Pos(Y=TEXT_HEIGHT / 2) * top_text
    keycap_body, text = build_keycap(bottom_text + top_text)
    text = cast(Part, text)
    keycap_body.label = "keycap"
    text.label = "text"  # Doesn't work on the export but works on the show
    keycap = Compound(children=[keycap_body, text])
    keycap.label = bottom_glyph.replace("/", "") + top_glyph
    keycaps.append(keycap)


for glyph in BUMP_SINGLE_GLYPS:
    keycap_body, text = build_keycap(
        Text(glyph, TEXT_HEIGHT, font_path=OVERPASS_FONT_PATH), True
    )
    text = cast(Part, text)
    keycap_body.label = "keycap"
    text.label = "text"  # Doesn't work on the export but works on the show
    keycap = Compound(children=[keycap_body, text])
    keycap.label = glyph
    keycaps.append(keycap)

slash_text = Text("\\", TEXT_HEIGHT, font_path=OVERPASS_FONT_PATH)
slash_text_height = (
    bounding_box(slash_text).vertices().sort_by(Axis.Y)[-1].Y
    - bounding_box(slash_text).vertices().sort_by(Axis.Y)[0].Y
)
pipe_text = Text("|", TEXT_HEIGHT, font_path=OVERPASS_FONT_PATH)
pipe_text_height = (
    bounding_box(pipe_text).vertices().sort_by(Axis.Y)[-1].Y
    - bounding_box(pipe_text).vertices().sort_by(Axis.Y)[0].Y
)
pipe_text = scale(pipe_text, (1, slash_text_height / pipe_text_height, 1))
slash_text = Pos(Y=-TEXT_HEIGHT / 2) * slash_text
pipe_text = Pos(Y=TEXT_HEIGHT / 2) * pipe_text
keycap_body, text = build_keycap(slash_text + pipe_text)
text = cast(Part, text)
keycap_body.label = "keycap"
text.label = "text"  # Doesn't work on the export but works on the show
keycap = Compound(children=[keycap_body, text])
keycap.label = "|"
keycaps.append(keycap)

for _ in range(BLANK_GLYPHS):
    keycap, __ = build_keycap()
    keycap.label = "blank"
    keycaps.append(keycap)


for i in range(len(keycaps)):
    export_step(
        keycaps[i],
        os.path.dirname(os.path.realpath(__file__)) + "/output/" + str(i) + ".step",
    )

print(len(keycaps))
for i in range(len(keycaps)):
    x = i % 14
    y = i // 14
    keycaps[i] = Pos(x * (BOTTOM_WIDTH + 1), -y * (BOTTOM_WIDTH + 1)) * keycaps[i]

# text = split(
#     text,
#     Plane.XY * Pos(Z=text.vertices().sort_by(Axis.Z)[0].Z + TEXT_DEPTH),
#     keep=Keep.BOTTOM,
# )

show(keycaps)
