# Bunnell-style base for a phone scoliometer, independent of the phone case.
# The phone stands on its long edge on two pads (only they define the measured line), a rubber band
# over the top edge holds it down. Lean toward/away does not matter to the app's angle.
import numpy as np, trimesh
from manifold3d import Manifold, CrossSection

L, D, H = 150.0, 26.0, 16.0          # base length, depth, height
NOTCH_B, NOTCH_T, NOTCH_H = 24.0, 14.0, 10.0   # gap for the spinous processes (bottom width, top width, height)
CH = 17.5                            # channel inner width (cases up to ~17 mm)
PAD_X0, PAD_X1, PAD_H = 46.0, 62.0, 2.0
WALL_X, WALL_H, WALL_T = 22.0, 8.0, 3.0
CHAMF = 3.0

def box(x0, x1, y0, y1, z0, z1):
    return Manifold.cube([x1 - x0, y1 - y0, z1 - z0]).translate([x0, y0, z0])

body = box(-L/2, L/2, -D/2, D/2, 0, H)
# chamfer the bottom long edges and the ends so the contact edges are smooth on skin
for sy in (-1, 1):
    c = Manifold.cube([L + 10, CHAMF * 2, CHAMF * 2], center=True).rotate([45, 0, 0]).translate([0, sy * D/2, 0])
    body = body - c
for sx in (-1, 1):
    c = Manifold.cube([CHAMF * 2, D + 10, CHAMF * 2], center=True).rotate([0, 45, 0]).translate([sx * L/2, 0, 0])
    body = body - c
# notch: trapezoid prism through the depth
notch = CrossSection([[(-NOTCH_B/2, 0), (NOTCH_B/2, 0), (NOTCH_T/2, NOTCH_H), (-NOTCH_T/2, NOTCH_H)]]).extrude(D + 10).rotate([90, 0, 0]).translate([0, (D + 10) / 2, -0.01])
body = body - notch
# lower the end of the notch slightly with a small rounding at its top corners (comfort)
# channel walls (middle only, away from camera bump / buttons)
for sy in (-1, 1):
    y0 = sy * CH/2 if sy > 0 else -CH/2 - WALL_T
    body = body + box(-WALL_X, WALL_X, y0, y0 + WALL_T, H - 0.01, H + WALL_H)
# two pads: the only contact with the phone's edge
for sx in (-1, 1):
    x0, x1 = (PAD_X0, PAD_X1) if sx > 0 else (-PAD_X1, -PAD_X0)
    body = body + box(x0, x1, -CH/2, CH/2, H - 0.01, H + PAD_H)
# band hooks: mushroom knobs on front and back near both ends
for sx in (-1, 1):
    for sy in (-1, 1):
        stem = Manifold.cylinder(6.0, 2.6, 2.6, 32).rotate([-90 * sy, 0, 0]).translate([sx * 64, sy * D/2 - sy * 0.5, 9])
        cap = Manifold.cylinder(1.6, 4.2, 4.2, 32).rotate([-90 * sy, 0, 0]).translate([sx * 64, sy * (D/2 + 5.2), 9])
        body = body + stem + cap
mesh = body.to_mesh()
tm = trimesh.Trimesh(vertices=mesh.vert_properties[:, :3], faces=mesh.tri_verts)
print('watertight', tm.is_watertight, 'volume cm3', round(tm.volume / 1000, 1), 'bounds', np.round(tm.bounds, 1).tolist())
tm.export('skoliometr-nastavec.stl')
