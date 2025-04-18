cordenadas_ESTOE = [
    (-22, 36),
    (22, 36),
    (-56, 21),
    (-33, 21),
    (-17, 21),
    (-6, 21),
    (6, 21),
    (17, 21),
    (42, 21),
    (-72, 10),
    (-56, 10),
    (-42, 10),
    (-30, 10),
    (-20, 10),
    (-10, 10),
    (-3, 10),
    (3, 10),
    (10, 10),
    (20, 10),
    (30, 10),
    (48, 10),
    (-74, 3),
    (-56, 3),
    (-42, 3),
    (-30, 3),
    (-20, 3),
    (-13, 3),
    (-8, 3),
    (8, 3),
    (13, 3),
    (20, 3),
    (30, 3),
    (49, 3),
    (-75, -3),
    (-56, -3),
    (-42, -3),
    (-30, -3),
    (-20, -3),
    (-13, -3),
    (-8, -3),
    (8, -3),
    (13, -3),
    (20, -3),
    (30, -3),
    (49, -3),
    (-75, -8),
    (-56, -8),
    (-42, -8),
    (-30, -8),
    (-20, -8),
    (-13, -8),
    (-8, -8),
    (-3, -8),
    (3, -8),
    (8, -8),
    (13, -8),
    (20, -8),
    (30, -8),
    (48, -8),
    (-74, -13),
    (-56, -13),
    (-42, -13),
    (-30, -13),
    (-20, -13),
    (-13, -13),
    (-8, -13),
    (-3, -13),
    (3, -13),
    (8, -13),
    (13, -13),
    (20, -13),
    (30, -13),
    (46, -13),
    (-73, -21),
    (-56, -21),
    (-42, -21),
    (-30, -21),
    (-20, -21),
    (-13, -21),
    (-8, -21),
    (-3, -21),
    (3, -21),
    (8, -21),
    (13, -21),
    (20, -21),
    (42, -21),
    (-70, -30),
    (-50, -30),
    (-33, -30),
    (-17, -30),
    (-6, -30),
    (6, -30),
    (17, -30),
    (33, -30),
    (-56, -43),
    (-30, -43),
    (-8, -43),
    (8, -43),
    (-30, -52),
    (-8, -57),
]

x_coords = [coord[0] for coord in cordenadas_ESTOE]
y_coords = [coord[1] for coord in cordenadas_ESTOE]



# Adjust spacing for peripheral coordinates
x_coords = [x * 0.5 if abs(x) > 0 else x for x in x_coords]
y_coords = [y * 0.5 if abs(y) > 0 else y for y in y_coords]



cordenadas_ESTOE = []
for x, y in zip(x_coords, y_coords):
    cordenadas_ESTOE.append((x, y))