from build123d import *  # pyright: ignore
from build123d import cast
from ocp_vscode import *  # pyright: ignore

WIDTH = 140
LENGTH = 80
HEIGHT = 10
BOTTOM_CHAMFER = 1
CORNER_FILLET = 10
TOP_FILLET = 3

MAIN_TEXT_SIZE = 30
MAIN_TEXT_DEPTH = 10
MAIN_TEXT_Y_POS = -(LENGTH / 2 - TOP_FILLET)
MAIN_TEXT_Z_POS = HEIGHT - 1

SUB_TEXT_SIZE = HEIGHT - BOTTOM_CHAMFER - TOP_FILLET
SUB_TEXT_DEPTH = 1
SUB_TEXT_X_POS = -(WIDTH / 2 - CORNER_FILLET) + 5
SUB_TEXT_Y_POS = -LENGTH / 2
SUB_TEXT_Z_POS = BOTTOM_CHAMFER * 2


base = Box(WIDTH, LENGTH, HEIGHT, align=(Align.CENTER, Align.CENTER, Align.MIN))
base = fillet(base.edges().filter_by(Axis.Z), CORNER_FILLET)
base = fillet(base.edges().group_by(Axis.Z)[-1], TOP_FILLET)
base = chamfer(base.edges().group_by(Axis.Z)[0], BOTTOM_CHAMFER)


main_text = Text(
    "Marrocos",
    MAIN_TEXT_SIZE,
    font="Akaya Kanadaka",
    font_path=os.path.dirname(os.path.realpath(__file__))
    + "/AkayaKanadaka-Regular.ttf",
    align=(Align.CENTER, Align.MIN),
)
main_text = extrude(main_text, -MAIN_TEXT_DEPTH)
main_text = Rot(X=90) * main_text
main_text = Pos(Y=MAIN_TEXT_Y_POS, Z=MAIN_TEXT_Z_POS) * main_text

sub_text = Text(
    "Janeiro 2026",
    SUB_TEXT_SIZE,
    font="Akaya Kanadaka",
    font_path=os.path.dirname(os.path.realpath(__file__))
    + "/AkayaKanadaka-Regular.ttf",
    align=(Align.MIN, Align.MIN),
)
sub_text = extrude(sub_text, -SUB_TEXT_DEPTH)
sub_text = Rot(X=90) * sub_text
sub_text = Pos(X=SUB_TEXT_X_POS, Y=SUB_TEXT_Y_POS, Z=SUB_TEXT_Z_POS) * sub_text

part = Part() + [base - sub_text, main_text]

export_step(
    part,
    os.path.dirname(os.path.realpath(__file__)) + "/marrocos-baseplate.step",
)


show(part)
