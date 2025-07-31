from build123d import *  # pyright: ignore
from ocp_vscode import *  # pyright: ignore

BATTERY_WIDTH = 49.4
BATTERY_DEPTH = 33.5
BATTERY_HEIGHT = 5.85

left_part = import_step(
    os.path.dirname(os.path.realpath(__file__))
    + "/cosmos-keyboard/cosmos-keyboard-full-left.step"
)

for child in left_part.children:
    if child.label == "Microcontroller_Holder":
        left_part = child
        break

left_part = Pos(-left_part.center()) * left_part

# Deepen groves for the board hole wires
left_part -= extrude(
    left_part.faces().filter_by(Plane.XY).group_by(Axis.Z)[1], 1, (0, 0, -1)
)

# Chamfer the hole that didn't come chamfered by some reason
left_part = chamfer(left_part.edges().filter_by(Plane.XY).group_by(Axis.Z)[0][-2], 1.35)

# Offset doesn't work because of the split below
left_battery_slot = Pos(Y=-1) * Box(
    BATTERY_DEPTH + 4, BATTERY_WIDTH + 2, BATTERY_HEIGHT + 4
)
left_battery_slot = Pos(14, -14, 15) * Rot(X=30) * left_battery_slot
left_battery_slot = split(
    left_battery_slot, Plane.XY * Pos(Z=left_part.vertices().sort_by(Axis.Z)[0].Z)
)

left_battery_arm = Box(30, 16, 17, align=(Align.MIN, Align.MAX, Align.MIN))
left_battery_arm = Pos(1.4, -6.5, -1.79) * left_battery_arm
left_battery_slot += left_battery_arm

left_part += left_battery_slot
left_part -= (
    Pos(14, -14, 15) * Rot(X=30) * Box(BATTERY_DEPTH, BATTERY_WIDTH, BATTERY_HEIGHT)
)
left_part -= (
    Pos(14, -14, 18) * Rot(X=30) * Box(BATTERY_DEPTH - 2, BATTERY_WIDTH, BATTERY_HEIGHT)
)

# Stengthen arm
left_part += extrude(
    Part() + [left_part.faces()[12], left_part.faces()[13], left_part.faces()[14]],
    4,
    (0, -1, 0),
)

export_step(
    left_part,
    os.path.dirname(os.path.realpath(__file__))
    + "/cosmos-keyboard-board-holder-left-mod.step",
)


right_part = import_step(
    os.path.dirname(os.path.realpath(__file__))
    + "/cosmos-keyboard/cosmos-keyboard-full-right.step"
)

for child in right_part.children:
    if child.label == "Microcontroller_Holder":
        right_part = child
        break

right_part = Pos(-right_part.center()) * right_part

# Deepen groves for the board hole wires
right_part -= extrude(
    right_part.faces().filter_by(Plane.XY).group_by(Axis.Z)[1], 1, (0, 0, -1)
)

# Chamfer the hole that didn't come chamfered by some reason
right_part = chamfer(
    right_part.edges().filter_by(Plane.XY).group_by(Axis.Z)[0][-2], 1.35
)

# Offset doesn't work because of the split below
right_battery_slot = Pos(Y=-1) * Box(
    BATTERY_DEPTH + 4, BATTERY_WIDTH + 2, BATTERY_HEIGHT + 4
)
right_battery_slot = Pos(-14, -14, 15) * Rot(X=30) * right_battery_slot
right_battery_slot = split(
    right_battery_slot, Plane.XY * Pos(Z=right_part.vertices().sort_by(Axis.Z)[0].Z)
)

right_battery_arm = Box(30, 16, 17, align=(Align.MAX, Align.MAX, Align.MIN))
right_battery_arm = Pos(-1.4, -6.5, -1.79) * right_battery_arm
right_battery_slot += right_battery_arm

right_part += right_battery_slot
right_part -= (
    Pos(-14, -14, 15) * Rot(X=30) * Box(BATTERY_DEPTH, BATTERY_WIDTH, BATTERY_HEIGHT)
)
right_part -= (
    Pos(-14, -14, 18)
    * Rot(X=30)
    * Box(BATTERY_DEPTH - 2, BATTERY_WIDTH, BATTERY_HEIGHT)
)

# Stengthen arm
right_part += extrude(
    Part() + [right_part.faces()[12], right_part.faces()[13], right_part.faces()[14]],
    4,
    (0, -1, 0),
)

export_step(
    right_part,
    os.path.dirname(os.path.realpath(__file__))
    + "/cosmos-keyboard-board-holder-right-mod.step",
)

right_part = Pos(50) * right_part
right_part.label = "right"
left_part = Pos(-50) * left_part
left_part.label = "left"
show([right_part, left_part])
