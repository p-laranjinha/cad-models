import os
from yacv_server import show
from build123d import *  # pyright: ignore
from switch_holder import (
    HOLDER_DEPTH,
    HOLDER_HEIGHT,
    render_switch_holder,
)
from switch_hole import render_switch_hole

holder = render_switch_holder()

# Rotate and move holder to the correct printing position
holder = Rot(Z=180) * Rot(X=90) * Pos(Y=HOLDER_DEPTH / 2, Z=-HOLDER_HEIGHT / 2) * holder

part = holder

export_stl(
    part, os.path.dirname(os.path.realpath(__file__)) + "/klavgen_switch_holder.stl"
)

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore

switch_hole = render_switch_hole()
export_stl(
    switch_hole,
    os.path.dirname(os.path.realpath(__file__)) + "/klavgen_switch_hole.stl",
)
