import os
from yacv_server import show
from build123d import *  # pyright: ignore
from build123d import cast
from switch_holder import render_switch_holder, HOLDER_DEPTH, HOLDER_HEIGHT

# Inspired and adapted from https://github.com/klavgen/klavgen

holder = render_switch_holder()
holder = Rot(Z=180) * Rot(X=90) * Pos(Y=HOLDER_DEPTH / 2, Z=-HOLDER_HEIGHT / 2) * holder

part = holder

export_stl(
    part, os.path.dirname(os.path.realpath(__file__)) + "/klavgen_switch_holder.stl"
)

part.color = (0.3, 0.3, 0.3, 1)
show(part, names="Part")  # pyright: ignore
