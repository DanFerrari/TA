cordenadas_24OE = [
(-9, 21),
(-3, 21),
(3, 21),
(9, 21),
(-15, 15),
(-9, 15),
(-3, 15),
(3, 15),
(9, 15),
(15, 15),
(-21, 9),
(-15, 9),
(-9, 9),
(-3, 9),
(3, 9),
(9, 9),
(15, 9),
(21, 9),
(-21, 3),
(-15, 3),
(-9, 3),
(-3, 3),
(3, 3),
(9, 3),
(15, 3),
(21, 3),
(27, 3),
(-21, -3),
(-15, -3),
(-9, -3),
(-3, -3),
(3, -3),
(9, -3),
(15, -3),
(21, -3),
(27, -3),
(-21, -9),
(-15, -9),
(-9, -9),
(-3, -9),
(3, -9),
(9, -9),
(15, -9),
(21, -9),
(-15, -15),
(-9, -15),
(-3, -15),
(3, -15),
(9, -15),
(15, -15),
(-9, -21),
(-3, -21),
(3, -21),
(9, -21),
]


from cordenadas_30 import cordenadas_30
indices_nulos_24OE = [index for index, coord in enumerate(cordenadas_30) if coord not in cordenadas_24OE]
