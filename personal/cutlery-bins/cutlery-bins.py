import os
from build123d import *  # pyright: ignore

from yacv_server import show

MAX_PRINTABLE_LENGTH = 200

# Drawer height/depth: 104mm
bins = {
    "soup_spoons": {"size": (60, 230, 50), "position": (300, 0)},
    "forks": {"size": (60, 230, 50), "position": (240, 0)},
    "knives": {"size": (60, 230, 50), "position": (180, 0)},
    "cutting_knives": {"size": (100, 230, 50), "position": (80, 0)},
    "butter_knives": {"size": (30, 180, 50), "position": (50, 0)},
    "big_dessert_spoons": {"size": (50, 180, 50), "position": (0, 0)},
    "small_dessert_spoons": {"size": (80, 150, 50), "position": (80, 230)},
    "dessert_forks": {"size": (200, 70, 50), "position": (160, 230)},
    "dessert_knives": {"size": (200, 80, 50), "position": (160, 300)},
    "pincers": {"size": (80, 291, 50), "position": (0, 180)},
    "others": {"size": (280, 91, 50), "position": (80, 380)},
}

WALL_WIDTH = 2
INSIDE_CORNER_RADIUS = 5

for bin_name, bin_props in bins.items():
    bin_size = bin_props["size"]
    width = bin_size[0]
    height = bin_size[1]
    depth = bin_size[2]
    bin_bottom_faces = [Rectangle(width, height)]
    width_inner = width - WALL_WIDTH * 2
    height_inner = height - WALL_WIDTH * 2
    depth_inner = depth - WALL_WIDTH
    if width > MAX_PRINTABLE_LENGTH:
        divider_line = [
            (0, -height / 2),
            (0, -height_inner / 2 * 0.7),
            (-10, -height_inner / 2 * 0.8),
            (-10, -height_inner / 2 * 0.2),
            (0, -height_inner / 2 * 0.3),
            (0, height_inner / 2 * 0.3),
            (10, height_inner / 2 * 0.2),
            (10, height_inner / 2 * 0.8),
            (0, height_inner / 2 * 0.7),
            (0, height / 2),
        ]
        bin_bottom_faces = [
            make_face(
                Polyline(
                    [(-width / 2, height / 2), (-width / 2, -height / 2)]
                    + divider_line
                    + [(-width / 2, height / 2)]
                ).edges()
            ),
            make_face(
                Polyline(
                    [(width / 2, height / 2), (width / 2, -height / 2)]
                    + divider_line
                    + [(width / 2, height / 2)]
                ).edges()
            ),
        ]
    if height > MAX_PRINTABLE_LENGTH:
        divider_line = [
            (-width / 2, 0),
            (-width_inner / 2 * 0.7, 0),
            (-width_inner / 2 * 0.8, -10),
            (-width_inner / 2 * 0.2, -10),
            (-width_inner / 2 * 0.3, 0),
            (width_inner / 2 * 0.3, 0),
            (width_inner / 2 * 0.2, 10),
            (width_inner / 2 * 0.8, 10),
            (width_inner / 2 * 0.7, 0),
            (width / 2, 0),
        ]
        bin_bottom_faces = [
            make_face(
                Polyline(
                    [(width / 2, -height / 2), (-width / 2, -height / 2)]
                    + divider_line
                    + [(width / 2, -height / 2)]
                ).edges()
            ),
            make_face(
                Polyline(
                    [(width / 2, height / 2), (-width / 2, height / 2)]
                    + divider_line
                    + [(width / 2, height / 2)]
                ).edges()
            ),
        ]

    bin_model = Compound(
        [
            extrude(face, -depth)
            - fillet(
                Box(
                    width_inner,
                    height_inner,
                    depth_inner,
                    align=(Align.CENTER, Align.CENTER, Align.MAX),
                )
                .edges()
                .filter_by(Axis.Z),
                5,
            )
            for face in bin_bottom_faces
        ]
    )
    bin_position = bin_props["position"]
    x = bin_position[0]
    y = bin_position[1]
    bin_model = bin_model.move(Location((x + width / 2, y + height / 2)))
    bins[bin_name]["model"] = bin_model

bin_models = [bin["model"] for bin in bins.values()]

part = Compound(bin_models)

show(part)  # pyright: ignore

export_stl(part, os.path.splitext(__file__)[0] + ".stl")
