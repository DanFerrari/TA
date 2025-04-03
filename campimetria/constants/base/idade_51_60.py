base = ['26', '25', '25', '26', '26', '27', '27', '26', '26', '26', '26', '27', '28', '28', '28', '27', '27', '26', '26', '27', '28', '29', '29', '29', '28', '27', '27', '27', '26', '27', '29', '29', '30', '30', '29', '0', '27', '27', '26', '28', '29', '29', '30', '30', '29', '0', '28', '27', '26', '27', '28', '29', '29', '29', '29', '28', '27', '26', '26', '27', '28', '28', '29', '28', '28', '27', '26', '27', '28', '28', '28', '27', '26', '26', '27', '27']

keys = [
    (-9, 27), (-3, 27), (3, 27), (9, 27), (-15, 21), (-9, 21), (-3, 21), (3, 21), (9, 21), (15, 21),
    (-21, 15), (-15, 15), (-9, 15), (-3, 15), (3, 15), (9, 15), (15, 15), (21, 15), (-27, 9), (-21, 9),
    (-15, 9), (-9, 9), (-3, 9), (3, 9), (9, 9), (15, 9), (21, 9), (27, 9), (-27, 3), (-21, 3), (-15, 3),
    (-9, 3), (-3, 3), (3, 3), (9, 3), (15, 3), (21, 3), (27, 3), (-27, -3), (-21, -3), (-15, -3), (-9, -3),
    (-3, -3), (3, -3), (9, -3), (15, -3), (21, -3), (27, -3), (-27, -9), (-21, -9), (-15, -9), (-9, -9),
    (-3, -9), (3, -9), (9, -9), (15, -9), (21, -9), (27, -9), (-21, -15), (-15, -15), (-9, -15), (-3, -15),
    (3, -15), (9, -15), (15, -15), (21, -15), (-15, -21), (-9, -21), (-3, -21), (3, -21), (9, -21), (15, -21),
    (-9, -27), (-3, -27), (3, -27), (9, -27)
]

lista_valores = {key: int(base[i]) for i, key in enumerate(keys)}