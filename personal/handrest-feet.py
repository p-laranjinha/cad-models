from build123d import (Line,  export_stl, extrude, make_face)

'''
Rubber feet:
                inner_top_length
                    -------
                   |       /
                   |      /
 inner_left_length |     /
                   |    /
                   |   /
                    --
              inner_bottom_length
'''

inner_left_length = 74.5
inner_top_length = 35.5
inner_bottom_length = 23

height = 15

# INFO: Using Polylines would be better than this.

inner_left = Line((0,0), (0,inner_left_length))
inner_top = Line(inner_left @ 1, (inner_top_length, inner_left_length))
inner_bottom = Line(inner_left @ 0, (inner_bottom_length, 0))
inner_right = Line(inner_top @ 1, inner_bottom @ 1)

outer_left = Line((inner_left @ 0).add((-3, -3)), (inner_left @ 1).add((-3,3)))
outer_top = Line(outer_left @ 1, (inner_top @ 1).add((3,3)))
outer_bottom = Line(outer_left @ 0, (inner_bottom @ 1).add((3,-3)))
outer_right = Line(outer_top @ 1, outer_bottom @ 1)

inner_face = make_face([inner_left, inner_top, inner_bottom, inner_right])

outer_face = make_face([outer_left, outer_top, outer_bottom, outer_right])

part = extrude(outer_face, height) - extrude(inner_face, height)

# show_object is a CQ-editor thing.
if 'show_object' in globals():
    show_object(part, name="Part", options=dict(color="white")) # pyright: ignore

export_stl(part, "./handrest-feet.stl")
