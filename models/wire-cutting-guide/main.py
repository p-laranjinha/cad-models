from build123d import *  # pyright: ignore
from ocp_vscode import *  # pyright: ignore

COLUMN_CUT_LENGTHS = [
    41,
    41 - 3 - 2.53,
    18.5 + 3 - 2.53,
]

ROW_CUT_LENGTHS = [
    30,
    45,
    # use the 2nd one from the columns for in between
    5 - 2.53,
]

WIRE_THICKNESS = 0.9  # Trial and error

GUIDE_WIDTH = 15
GUIDE_DEPTH = 5
GUIDE_EXTRA_HEIGHT = 2

CHAMFER_LENGTH = 0.5

guides = []


def make_guide(cut_length):
    guide = Box(
        GUIDE_DEPTH,
        GUIDE_WIDTH,
        cut_length + GUIDE_EXTRA_HEIGHT,
        align=(Align.CENTER, Align.CENTER, Align.MIN),
    )
    guide = chamfer(guide.edges(), CHAMFER_LENGTH)
    guide -= Pos(Z=GUIDE_EXTRA_HEIGHT) * Cylinder(
        WIRE_THICKNESS, cut_length, align=(Align.CENTER, Align.CENTER, Align.MIN)
    )
    return guide


for i in range(len(COLUMN_CUT_LENGTHS)):
    guide = make_guide(COLUMN_CUT_LENGTHS[i])
    guide -= extrude(Rot(180) * Text("C", GUIDE_DEPTH / 2), -1)
    guide = Pos(i * (GUIDE_DEPTH + 1)) * guide
    guides.append(guide)

for i in range(len(ROW_CUT_LENGTHS)):
    guide = make_guide(ROW_CUT_LENGTHS[i])
    guide -= extrude(Rot(180) * Text("R", GUIDE_DEPTH / 2), -1)
    guide = Pos((i + len(COLUMN_CUT_LENGTHS)) * (GUIDE_DEPTH + 1)) * guide
    guides.append(guide)

export_step(
    Compound(children=guides),
    os.path.dirname(os.path.realpath(__file__)) + "/wire-cutting-guides.step",
)
show(guides)
