import os
from build123d import *  # pyright: ignore
from yacv_server import show

SVG_HEIGHT = 432.9  # can't find it programatically
TARGET_HEIGHT = 60
#
# svg = import_svg(os.path.dirname(os.path.abspath(__file__)) + "/Chamusca.svg")
# svg = scale(svg, TARGET_HEIGHT / SVG_HEIGHT).move(
#     Location((0, -SVG_HEIGHT + TARGET_HEIGHT))
# )
#
# # show(svg, names=["part"])  # pyright: ignore
# # show(
# #     [extrude(face, 5, Vector(0, 0, 1)) for face in svg.faces()], names=["part"]
# # )  # pyright: ignore
#
# export_stl(svg, os.path.splitext(__file__)[0] + ".stl")


def extrude_svg(path, depth):
    svg = import_svg(os.path.dirname(os.path.abspath(__file__)) + path)
    out = Part()  # pyright: ignore
    for face in svg.faces():
        face = scale(face, TARGET_HEIGHT / SVG_HEIGHT).move(
            Location((0, -SVG_HEIGHT + TARGET_HEIGHT))
        )
        out += extrude(face, depth, Vector(0, 0, 1))  # pyright: ignore
    return out


part = Compound(
    [
        extrude_svg("/svgs/shield_outer.svg", 1),
        extrude_svg("/svgs/shield_inner.svg", 1).move(Location((0, 0, 1))),
        extrude_svg("/svgs/lion.svg", 1).move(Location((0, 0, 2)))
        - extrude_svg("/svgs/lion_inner.svg", 1).move(Location((0, 0, 2))),
        extrude_svg("/svgs/grapes.svg", 1).move(Location((0, 0, 1))),
        extrude_svg("/svgs/text.svg", 1).move(Location((0, 0, 1.5))),
        extrude_svg("/svgs/banner.svg", 1.5),
        extrude_svg("/svgs/banner_bend_1.svg", 1),
        extrude_svg("/svgs/banner_bend_2.svg", 1.3),
        extrude_svg("/svgs/banner_bend_3.svg", 0.8),
        extrude_svg("/svgs/banner_bend_4.svg", 0.6),
        extrude_svg("/svgs/banner_bend_5.svg", 1),
        extrude_svg("/svgs/banner_bend_6.svg", 0.8),
        extrude_svg("/svgs/banner_bend_7.svg", 0.6),
        extrude_svg("/svgs/pomegranates.svg", 1).move(Location((0, 0, 1)))
        - extrude_svg("/svgs/pomegranates_inner.svg", 0.3).move(Location((0, 0, 1.7)))
        - extrude_svg("/svgs/pomegranates_inner_inner.svg", 0.3).move(
            Location((0, 0, 1.4))
        ),
        extrude_svg("/svgs/crown.svg", 1.5),
        extrude_svg("/svgs/crown_middle_top.svg", 1.2),
        extrude_svg("/svgs/crown_middle_bottom.svg", 0.9),
        extrude_svg("/svgs/towers.svg", 1),
        extrude_svg("/svgs/towers_archway.svg", 1.2),
        extrude_svg("/svgs/towers_entrance.svg", 0.9),
        extrude_svg("/svgs/towers_top_bottom.svg", 1.2),
        extrude_svg("/svgs/towers_top_top.svg", 1.5),
        extrude_svg("/svgs/walls_top.svg", 0.8),
        extrude_svg("/svgs/walls_bricks.svg", 0.6),
        extrude_svg("/svgs/walls.svg", 0.4),
    ]
)


def bigBackplate(part):
    return Compound(
        [
            fillet(
                extrude(
                    Rectangle(60, 32.5).move(Location((57.2 / 2, 60.1 * 0.75 + 0.5))), 1
                )
                .edges()
                .filter_by(Axis.Z)
                .group_by(Axis.Y)[-1],
                3,
            )
            + extrude(Circle(30).move(Location((57.2 / 2, 60.1 / 2))), 1)
            - extrude(Circle(1.5).move(Location((57.2 / 2, 60.1 - 1))), 1),
            part.move(Location((0, 0, 1))),
        ]
    )


def smallBackplate(part):
    return Compound(
        [
            extrude_svg("/svgs/shield_outer.svg", 1),
            extrude_svg("/svgs/banner.svg", 1),
            extrude_svg("/svgs/banner_bend_1.svg", 1),
            extrude_svg("/svgs/banner_bend_2.svg", 1),
            extrude_svg("/svgs/banner_bend_3.svg", 1),
            extrude_svg("/svgs/banner_bend_4.svg", 1),
            extrude_svg("/svgs/banner_bend_5.svg", 1),
            extrude_svg("/svgs/banner_bend_6.svg", 1),
            extrude_svg("/svgs/banner_bend_7.svg", 1),
            extrude_svg("/svgs/crown.svg", 1),
            extrude_svg("/svgs/crown_middle_top.svg", 1),
            extrude_svg("/svgs/crown_middle_bottom.svg", 1),
            extrude_svg("/svgs/towers.svg", 1),
            extrude_svg("/svgs/towers_archway.svg", 1),
            extrude_svg("/svgs/towers_entrance.svg", 1),
            extrude_svg("/svgs/towers_top_bottom.svg", 1),
            extrude_svg("/svgs/towers_top_top.svg", 1),
            extrude_svg("/svgs/walls_top.svg", 1),
            extrude_svg("/svgs/backplate.svg", 1),
            extrude(Circle(3.5).move(Location((57.2 / 2, 60.1 - 1))), 1.5)
            + extrude(Rectangle(7, 7).move(Location((57.2 / 2, 60.1 - 4.5))), 1.5)
            - extrude(Circle(1.5).move(Location((57.2 / 2, 60.1 - 1))), 1.5),
            part.move(Location((0, 0, 1))),
        ]
    )


part = smallBackplate(part)

part.color = (0.5, 0.5, 0.5, 1)
show(part)  # pyright: ignore

export_stl(part, os.path.splitext(__file__)[0] + ".stl")
