import os
from build123d import *  # pyright: ignore
from build123d import cast
from yacv_server import show

TOLERANCE = 1

WALL_THICKNESS = 2
SPACER_WIDTH = 11 + 2 * WALL_THICKNESS
HEIGHT = 57 - TOLERANCE
WIDTH1 = 48 - SPACER_WIDTH / 2 - TOLERANCE
WIDTH2 = 50.8 - SPACER_WIDTH / 2 - TOLERANCE


y_stick = Box(WALL_THICKNESS, HEIGHT, WALL_THICKNESS, align=Align.MIN)
y_stick = chamfer(y_stick.edges().filter_by(Axis.Y), WALL_THICKNESS / 4)
x1_stick = Box(WIDTH1, WALL_THICKNESS, WALL_THICKNESS, align=Align.MIN)
x1_stick = chamfer(x1_stick.edges().filter_by(Axis.X), WALL_THICKNESS / 4)
x2_stick = Box(WIDTH2, WALL_THICKNESS, WALL_THICKNESS, align=Align.MIN)
x2_stick = chamfer(x2_stick.edges().filter_by(Axis.X), WALL_THICKNESS / 4)

y1_grate = Part()
for x in range(1, int(WIDTH1), WALL_THICKNESS * 3):
    y1_grate += Pos(x) * y_stick

x1_grate = Part()
for y in range(0, int(HEIGHT), WALL_THICKNESS * 3):
    x1_grate += Pos(Y=y) * x1_stick

y2_grate = Part()
for x in range(2, int(WIDTH2), WALL_THICKNESS * 3):
    y2_grate += Pos(x) * y_stick

x2_grate = Part()
for y in range(0, int(HEIGHT), WALL_THICKNESS * 3):
    x2_grate += Pos(Y=y) * x2_stick

grate1 = Part() + [x1_grate, y1_grate]
grate2 = Pos(Y=HEIGHT + TOLERANCE) * (Part() + [x2_grate, y2_grate])


part = Part() + [grate1, grate2]

export_stl(part, os.path.splitext(__file__)[0] + ".stl")

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
